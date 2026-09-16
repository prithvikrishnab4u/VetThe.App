/**
 * POST /api/suggest
 *
 * Turns a suggestion from the website form into a pull request, so visitors can
 * contribute without a GitHub account. Nothing reaches the site until a maintainer
 * merges the PR, and the usual validation workflow runs on it.
 *
 * Cloudflare Pages settings (Settings → Variables and secrets):
 *   GITHUB_TOKEN      secret. Fine-grained token for this repo only, with
 *                     Contents: read/write and Pull requests: read/write
 *                     (Issues: read/write too if you want the PR labelled)
 *   TURNSTILE_SECRET  secret. Turnstile widget secret key
 *   GITHUB_REPO       optional, defaults to prithvikrishnab4u/VetThe.App
 *   HUGO_PARAMS_TURNSTILESITEKEY  plain variable, the widget's site key (read by Hugo at build)
 *
 * Request body (JSON):
 *   { kind: "fix", app, capability, value: {support, tier, plan, notes, source, protocols, retention},
 *     contributor, comment, turnstileToken }
 *   { kind: "new_app", name, website, category, description,
 *     capabilities: { <id>: value, ... }, contributor, comment, turnstileToken }
 */

const DEFAULT_REPO = 'prithvikrishnab4u/VetThe.App';
const LABEL = 'community-suggestion';
const MAX_BODY_BYTES = 32 * 1024;
const LIMITS = { name: 80, description: 200, plan: 60, notes: 400, url: 500, retention: 40, contributor: 60, comment: 1000 };

// Support levels a visitor can suggest. not_researched is the default, never a suggestion.
const SUGGESTABLE = ['supported', 'partial', 'not_supported', 'undocumented'];
const TIERED = ['supported', 'partial'];

class InputError extends Error {}

export async function onRequestPost({ request, env }) {
    if (!env.GITHUB_TOKEN || !env.TURNSTILE_SECRET) {
        return json({ ok: false, error: 'Suggestions are not switched on yet. Please use GitHub for now.' }, 503);
    }

    let body;
    try {
        const text = await request.text();
        if (text.length > MAX_BODY_BYTES) throw new InputError('That suggestion is too long.');
        body = JSON.parse(text);
        if (!body || typeof body !== 'object') throw new InputError('Invalid request.');
    } catch (e) {
        return json({ ok: false, error: e instanceof InputError ? e.message : 'Invalid request.' }, 400);
    }

    // Bots fill in the hidden field; people never see it
    if (body.company_url) return json({ ok: false, error: 'Spam check failed.' }, 400);

    const human = await verifyTurnstile(env, body.turnstileToken, request.headers.get('CF-Connecting-IP'));
    if (!human) return json({ ok: false, error: 'The spam check expired or failed. Please try again.' }, 403);

    try {
        const schema = await loadAsset(env, request, '/data/schema.json');
        const github = new GitHub(env);
        const result = body.kind === 'new_app'
            ? await suggestNewApp(github, schema, await loadAsset(env, request, '/data/apps.json'), body)
            : await suggestFix(github, schema, body);
        return json({ ok: true, ...result });
    } catch (e) {
        if (e instanceof InputError) return json({ ok: false, error: e.message }, 400);
        console.error(e);
        return json({ ok: false, error: 'Something went wrong on our side. Please try again, or use GitHub.' }, 500);
    }
}

export function onRequest() {
    return json({ ok: false, error: 'Use POST.' }, 405);
}

// ---------- Suggestion types ----------

async function suggestFix(github, schema, body) {
    const appId = String(body.app || '');
    if (!/^[a-z0-9][a-z0-9-]{0,80}$/.test(appId)) throw new InputError('Unknown app.');
    const definition = schema.capabilities.find(c => c.id === body.capability);
    if (!definition) throw new InputError('Unknown capability.');

    const cap = cleanCapability(definition, body.value, schema);
    const path = `data/apps/${appId}.yaml`;
    const file = await github.getFile(path);
    if (!file) throw new InputError('Unknown app.');

    const updated = replaceCapability(file.text, definition.id, renderCapability(definition.id, cap));
    if (updated === null) throw new InputError("This app's file has an unusual layout, so it can't be updated automatically. Please use GitHub.");
    if (updated === file.text) throw new InputError('That matches what is already recorded.');

    const appName = (file.text.match(/^name:\s*"(.*)"\s*$/m) || [])[1] || appId;
    const summary = describe(cap, schema);
    return github.openPullRequest({
        branch: `suggest/${appId}-${definition.id}-${Date.now().toString(36)}`,
        path,
        content: updated,
        sha: file.sha,
        title: `${appName}: ${definition.label} → ${summary}`,
        body: pullRequestBody({
            intro: `Suggested change to **${appName} · ${definition.label}**.`,
            rows: [[definition.label, summary, cap.source || '(none, vendor pages are silent)']],
            notes: cap.notes,
            body,
        }),
    });
}

async function suggestNewApp(github, schema, apps, body) {
    const name = cleanText(body.name, LIMITS.name, 'App name', true);
    const website = cleanUrl(body.website, 'Website', true);
    const description = cleanText(body.description, LIMITS.description, 'Description', true);
    if (!schema.categories.includes(body.category)) throw new InputError('Pick a category.');

    const id = slugify(name);
    if (!id) throw new InputError('App name needs at least one letter or number.');
    const host = hostname(website);
    const existing = apps.find(a => a._id === id || hostname(a.website) === host);
    if (existing) throw new InputError(`${existing.name} is already listed. Use "Suggest a fix" on its row instead.`);

    const provided = body.capabilities && typeof body.capabilities === 'object' ? body.capabilities : {};
    const blocks = [];
    const rows = [];
    for (const definition of schema.capabilities) {
        const raw = provided[definition.id];
        if (raw && raw.support && raw.support !== 'not_researched') {
            const cap = cleanCapability(definition, raw, schema);
            blocks.push(renderCapability(definition.id, cap));
            rows.push([definition.label, describe(cap, schema), cap.source || '(none, vendor pages are silent)']);
        } else {
            blocks.push(renderCapability(definition.id, { support: 'not_researched' }));
        }
    }

    const content = [
        `name: ${quote(name)}`,
        `category: ${quote(body.category)}`,
        `website: ${quote(website)}`,
        `description: ${quote(description)}`,
        'status: "draft"',
        '',
        '# One block per capability. Field meanings and allowed values: CONTRIBUTING.md',
        'capabilities:',
        ...blocks,
        '',
    ].join('\n');

    const path = `data/apps/${id}.yaml`;
    if (await github.getFile(path)) throw new InputError(`${name} is already listed.`);

    return github.openPullRequest({
        branch: `suggest/new-${id}-${Date.now().toString(36)}`,
        path,
        content,
        title: `Add ${name}`,
        body: pullRequestBody({
            intro: `New app: **${name}** (${website})\n\n> ${description}`,
            rows,
            body,
        }),
    });
}

// ---------- Validation (mirrors scripts/validate.py) ----------

function cleanCapability(definition, value, schema) {
    const label = definition.label;
    if (!value || typeof value !== 'object') throw new InputError(`${label}: choose a value.`);
    if (!SUGGESTABLE.includes(value.support)) throw new InputError(`${label}: choose a value.`);

    const cap = { support: value.support };
    const tiered = TIERED.includes(cap.support);
    const fields = definition.fields || [];

    if (tiered && value.tier) {
        if (!schema.tiers.some(t => t.id === value.tier)) throw new InputError(`${label}: unknown plan.`);
        cap.tier = value.tier;
    }
    if (tiered) {
        const plan = cleanText(value.plan, LIMITS.plan, `${label} plan name`);
        if (plan) cap.plan = plan;
    }
    const notes = cleanText(value.notes, LIMITS.notes, `${label} notes`);
    if (notes) cap.notes = notes;
    if (cap.support === 'partial' && !notes) throw new InputError(`${label}: explain the limitation in the notes.`);

    if (fields.includes('protocols') && tiered && Array.isArray(value.protocols) && value.protocols.length) {
        const protocols = [...new Set(value.protocols)];
        if (!protocols.every(p => schema.sso_protocols.includes(p))) throw new InputError(`${label}: unknown protocol.`);
        cap.protocols = schema.sso_protocols.filter(p => protocols.includes(p));
    }
    if (fields.includes('retention') && tiered) {
        const retention = cleanText(value.retention, LIMITS.retention, `${label} retention`);
        if (retention) cap.retention = retention;
    }

    if (cap.support === 'undocumented') {
        if (value.source) throw new InputError(`${label}: "Not documented" can't have a source. Mention the pages you checked in the notes.`);
    } else {
        cap.source = cleanUrl(value.source, `${label} source`, true);
        cap.checked = new Date().toISOString().slice(0, 10);
    }
    return cap;
}

function cleanText(value, max, label, required = false) {
    const text = String(value ?? '').replace(/[ -]+/g, ' ').replace(/\s+/g, ' ').trim();
    if (required && !text) throw new InputError(`${label} is required.`);
    if (text.length > max) throw new InputError(`${label} must be ${max} characters or fewer.`);
    return text;
}

function cleanUrl(value, label, required) {
    const text = cleanText(value, LIMITS.url, label, required);
    if (!text) return '';
    let url;
    try { url = new URL(text); } catch { throw new InputError(`${label} must be a full link starting with https://`); }
    if (!['http:', 'https:'].includes(url.protocol) || /\s/.test(text)) {
        throw new InputError(`${label} must be a full link starting with https://`);
    }
    return text;
}

// ---------- YAML ----------

function quote(text) {
    return `"${String(text).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

// Same field order and quoting as the CONTRIBUTING.md template
function renderCapability(id, cap) {
    const lines = [`  ${id}:`, `    support: ${quote(cap.support)}`];
    for (const key of ['tier', 'plan', 'notes']) if (cap[key]) lines.push(`    ${key}: ${quote(cap[key])}`);
    if (cap.protocols) lines.push(`    protocols: [${cap.protocols.map(quote).join(', ')}]`);
    for (const key of ['retention', 'source', 'checked']) if (cap[key]) lines.push(`    ${key}: ${quote(cap[key])}`);
    return lines.join('\n');
}

// Swap one capability block (its key line plus the indented lines under it).
// Returns null if the block isn't in the expected two-space block style.
function replaceCapability(text, id, block) {
    const lines = text.split('\n');
    const start = lines.findIndex(line => new RegExp(`^  ${id}:\\s*(#.*)?$`).test(line));
    if (start < 0) return null;
    let end = start + 1;
    while (end < lines.length && /^ {3,}\S/.test(lines[end])) end++;
    lines.splice(start, end - start, ...block.split('\n'));
    return lines.join('\n');
}

// ---------- GitHub ----------

class GitHub {
    constructor(env) {
        this.token = env.GITHUB_TOKEN;
        this.repo = env.GITHUB_REPO || DEFAULT_REPO;
    }

    async call(method, path, payload) {
        const res = await fetch(`https://api.github.com/repos/${this.repo}${path}`, {
            method,
            headers: {
                Authorization: `Bearer ${this.token}`,
                Accept: 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
                'User-Agent': 'vetthe-app-suggestions',
                ...(payload ? { 'Content-Type': 'application/json' } : {}),
            },
            body: payload ? JSON.stringify(payload) : undefined,
        });
        const data = await res.json().catch(() => null);
        return { ok: res.ok, status: res.status, data };
    }

    async must(method, path, payload) {
        const res = await this.call(method, path, payload);
        if (!res.ok) throw new Error(`GitHub ${method} ${path} → ${res.status}: ${JSON.stringify(res.data)}`);
        return res.data;
    }

    async getFile(path) {
        const res = await this.call('GET', `/contents/${path}?ref=main`);
        if (res.status === 404) return null;
        if (!res.ok) throw new Error(`GitHub GET ${path} → ${res.status}`);
        return { sha: res.data.sha, text: fromBase64(res.data.content) };
    }

    async openPullRequest({ branch, path, content, sha, title, body }) {
        const main = await this.must('GET', '/git/ref/heads/main');
        await this.must('POST', '/git/refs', { ref: `refs/heads/${branch}`, sha: main.object.sha });
        await this.must('PUT', `/contents/${path}`, {
            message: title,
            content: toBase64(content),
            branch,
            ...(sha ? { sha } : {}),
        });
        const pr = await this.must('POST', '/pulls', { title, head: branch, base: 'main', body, maintainer_can_modify: true });
        // Labelling needs Issues permission; the PR is still useful without it
        await this.call('POST', `/issues/${pr.number}/labels`, { labels: [LABEL] });
        return { url: pr.html_url, number: pr.number };
    }
}

function pullRequestBody({ intro, rows, notes, body }) {
    const contributor = cleanText(body.contributor, LIMITS.contributor, 'Name');
    const comment = cleanText(body.comment, LIMITS.comment, 'Comment');
    const cell = text => String(text).replace(/\|/g, '\\|');
    const parts = [
        `${intro}\n\nSubmitted through the website by **${contributor ? cell(contributor) : 'an anonymous visitor'}**.`,
    ];
    if (rows.length) {
        parts.push(['| Capability | Suggested | Source |', '|---|---|---|', ...rows.map(r => `| ${r.map(cell).join(' | ')} |`)].join('\n'));
    }
    if (notes) parts.push(`**Notes:** ${notes}`);
    if (comment) parts.push(`**From the contributor:**\n> ${comment}`);
    parts.push(
        '### Before merging\n' +
        '- [ ] Open each source and confirm it says this, on the vendor\'s own site\n' +
        '- [ ] The tier is the *minimum* plan that includes it\n' +
        '- [ ] Validation passed'
    );
    return parts.join('\n\n');
}

// ---------- Helpers ----------

async function verifyTurnstile(env, token, ip) {
    if (!token || typeof token !== 'string') return false;
    const form = new FormData();
    form.append('secret', env.TURNSTILE_SECRET);
    form.append('response', token);
    if (ip) form.append('remoteip', ip);
    const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const data = await res.json().catch(() => ({}));
    return data.success === true;
}

async function loadAsset(env, request, path) {
    const res = await env.ASSETS.fetch(new URL(path, request.url));
    if (!res.ok) throw new Error(`Missing ${path}`);
    return res.json();
}

function describe(cap, schema) {
    const level = schema.support_levels.find(s => s.id === cap.support)?.label || cap.support;
    const tier = schema.tiers.find(t => t.id === cap.tier)?.label;
    return tier ? `${level} (${tier})` : level;
}

function slugify(name) {
    return name.toLowerCase().normalize('NFKD').replace(/[̀-ͯ]/g, '')
        .replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60);
}

function hostname(url) {
    try { return new URL(url).hostname.replace(/^www\./, ''); } catch { return ''; }
}

function toBase64(text) {
    let binary = '';
    for (const byte of new TextEncoder().encode(text)) binary += String.fromCharCode(byte);
    return btoa(binary);
}

function fromBase64(encoded) {
    const binary = atob(encoded.replace(/\s/g, ''));
    return new TextDecoder().decode(Uint8Array.from(binary, c => c.charCodeAt(0)));
}

function json(data, status = 200) {
    return new Response(JSON.stringify(data), {
        status,
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' },
    });
}
