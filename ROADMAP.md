# Roadmap

Running log of what's done and what's next. **Update this file at the end of every work session**: tick items off, add what you found, and refresh the numbers with `.venv/bin/python scripts/validate.py`.

_Last updated: 2026-09-24_

## Remind the user

- **Website suggestions still aren't switched on.** Labels and the Turnstile widget are done. What's left is the two secrets in Cloudflare (`GITHUB_TOKEN`, `TURNSTILE_SECRET`) on Production, plus a redeploy. Probe `POST /api/suggest` to check.

## In progress

- Nothing running.

## Where the data stands

172 apps: 79 `published`, 93 `draft`. 2,064 data points:

| | Count |
|---|---|
| Verified (has `source` + `checked`) | 823 |
| Unverified (a value with no source, carried over from the old dataset) | 0 |
| Not documented (checked, the vendor says nothing) | 473 |
| Not researched | 768 |

## Done

- [x] Data model: 12 IAM capabilities, each with support, minimum tier, plan, notes, source, checked (`data/schema.yaml`)
- [x] Split `unknown` into `undocumented` and `not_researched`
- [x] **Core capabilities** (SSO, Enforce SSO, SCIM, Enforce MFA, Passkeys, Audit logs) checked against vendor docs for all 107 apps, including Snyk
- [x] Landing page redesign: hero, dark mode, compact layout so the table shows on the first screen
- [x] Deployed on Cloudflare Pages at vetthe.app
- [x] Contribute from the website: ✎ on every cell and "Add an app" open a form, and `site/functions/api/suggest.js` opens a pull request (Turnstile spam check, server-side validation)
- [x] GitHub issue forms (correct a value, request an app)
- [x] PR validation posts one comment showing the actual errors, updated on each push
- [x] **Batch 1 (2026-09-16):** all 17 values with no source checked against vendor docs, so every value now has a source or is marked not documented/not researched. Research ran with parallel agents that only report findings, and the main session made the edits.
  - Snyk: SSO and JIT are Enterprise (SAML/OIDC). MFA enforcement, passkeys and domain verification are not documented; 2FA enforcement and domain checks exist only for Snyk API & Web.
  - Session controls: Slack and Atlassian (Confluence, Jira) are free; Atlassian Guard adds more. HubSpot is free (idle timeout). GitHub and Notion are Enterprise. Linear is not documented.
  - Domain verification: 1Password Teams. Datadog, PagerDuty and Snowflake are not documented. Snowflake JIT is not documented.
- [x] **Batches 2–4 (2026-09-16):** first pass on core capabilities for the 14 apps that still had none: Airtable, Basecamp, Box, Canva, CrowdStrike, Dropbox, Gusto, Lark, Rippling, Splunk, TeamViewer, Udemy Business, ZoomInfo and Zscaler. Also checked JIT provisioning and domain verification for every app that supports SSO. About 20 parallel agents wrote JSON, and the main session applied and committed each result.
  - Many values are "not documented" because the help pages need JavaScript or a login, or returned errors: Salesforce, SAP Concur, BambooHR, BILL, LastPass, Hootsuite, Sprout Social and CrowdStrike. A manual check in a browser could turn these into real values.
  - Some supported values from ZoomInfo, Zscaler, CrowdStrike and Dropbox have no tier yet. They need one before publishing.
- [x] **65 new apps from BACKLOG.md P1 (2026-09-22):** core capabilities researched for the first 65 P1 apps (ChatGPT Enterprise, Claude Enterprise, Cursor, Vercel, Sentry, Power BI, Looker, Klaviyo, Salesloft, SAP SuccessFactors, Okta, JumpCloud, Jamf, Tailscale and others). Parallel Sonnet agents wrote JSON, the main session created `data/apps/<id>.yaml` as drafts and committed each result.
  - Agent token use was cut roughly in half partway through by capping tool calls per app and stripping HTML before it reaches context (`scratchpad/new/f.sh`). Capping too hard made agents give up early, so WebFetch stays the default tool and one retry per URL is allowed.
  - Seven P1 apps could not be researched at all because their sites block automated fetches: bitwarden, cyberark, mimecast, ping-identity, sap-ariba, sentinelone, zip. They were deliberately NOT added as empty rows — they need a manual browser check.
- [x] **Site pass (2026-09-22):** coverage stats now count core and extended separately, so the headline is defensible (99% of 1,032 core values checked, 644 sourced, 382 vendor silent, 6 left, 171/172 apps fully checked). CSV and JSON export removed. Author links (LinkedIn, iam.ninja) moved into a tight footer. The five-card coverage bento became one strip with a hover helper, and the standalone "know a value that's wrong" block was folded into it. Dark mode repalette. Quality of life: `/` to search, `Esc` to clear, rows per page, share the filtered view as a URL. Logo marquee and hero bulk removed so the table sits higher.
- [x] **One design language (2026-09-22):** `.btn-primary` (brand gradient) for every primary action, `.panel` for boxed sections, `.ink-band` for the dark bands. Footer is now a dark band matching the header, and the suggest panel got the same dark header so it reads as part of the site.
- [x] **Honest colour and placement (2026-09-23):** "Not documented" moved from grey to a muted sage (`--silent-*`), so a checked-but-silent value reads as a finding rather than a gap; grey now means only "nobody has opened this yet". Contribute moved from the header nav to the footer, byline with LinkedIn and iam.ninja moved into the hero. Drifting aurora removed from the footer and suggest panel, so the hero is the only place with motion.
- [x] **Suggest panel pickers (2026-09-23):** app picker is a datalist type-ahead over a hidden select that still holds the id; capability picker grouped core vs extended.
- [x] **Page laid out around the job (2026-09-23):** order is now signpost → "can I trust this" → table → reference. The hero lost its search box, its preview card and its byline, and is four entry chips plus a line of copy. The legend moved onto the table's own chrome, outside the scroll box, so it stays put while rows scroll. "How to read" moved below the table. "Something wrong? Click ✎" sits at the end of the data, where you have just seen a value you disagree with.
- [x] **Light mode (2026-09-23):** a fixed brand wash behind the body, a tinted lift on `.panel` instead of a grey shadow, and a tinted table header row, so the content area reads as part of the same design instead of a grey sheet between two dark bands. Header carries the LinkedIn and iam.ninja icons only; the name reads as publicity up there and the footer already has it.
- [x] **CI goes green (2026-09-23):** it had never passed. Two causes. The workflow called `hugo` on a runner that never had it, now installed via `peaceiris/actions-hugo@v3` pinned to 0.147.7, the version Cloudflare Pages runs. And it ran Node 18, but Tailwind v4's `@tailwindcss/oxide` binary needs Node 20+, and Hugo shells out to the Tailwind CLI mid-build, so the build step died. Node is now pinned in `.node-version` (22), which both `actions/setup-node` and Cloudflare Pages read, so CI and the deploy can't drift. A `NODE_VERSION` env var set in Cloudflare would override that file, so don't set one.
- [x] **BACKLOG.md:** 299 widely used apps not yet in the data, ranked P1/P2/P3. The agent wrote the websites from memory, so confirm them while researching.

## To do: setup (one-off, needed before website suggestions work; user will do this)

- [x] The `community-suggestion`, `data-fix` and `app-request` labels exist (2026-09-24)
- [x] Turnstile widget created; the site key is committed in `site/hugo.toml`, since it is public and ships in the HTML. No `HUGO_PARAMS_TURNSTILESITEKEY` variable needed (2026-09-24)
- [ ] Fine-grained GitHub token for this repo only: Contents read/write, Pull requests read/write, Issues read/write (for the label)
- [ ] Cloudflare Pages → Settings → Variables: `GITHUB_TOKEN` (secret), `TURNSTILE_SECRET` (secret). Env vars bind at deploy time, so redeploy after adding them, and put them on Production, not just Preview
- [ ] Confirm the Pages project's root directory is `site`, so `site/functions/` is deployed
- [ ] **Still returning 503 as of 2026-09-24.** `POST /api/suggest` with a junk Turnstile token is a safe probe: 503 means the Function cannot see `GITHUB_TOKEN` or `TURNSTILE_SECRET`; anything else means they are bound.
- [ ] Pin the Hugo version in Cloudflare (`HUGO_VERSION`) to match local builds. Cloudflare currently uses 0.147.7, which is why templates use `site.Data`

## To do: data (in priority order)

1. [ ] **Publish the rest**: 79 are published (2026-09-16). The 28 drafts are mostly missing plan tiers on supported values, often because vendor pages were blocked (403/503) or don't say which plan is needed. Every draft has had one agent attempt at its tiers, so what's left needs a manual browser check: 1password, adobe-creative-cloud, amplitude, atlassianjira, auth0, bamboohr, brex, cisco-webex, crowdstrike, databricks, datadog, deel, dropbox, expensify, hootsuite, navan, netsuite, outreach, ringcentral, salesforce, servicenow, shopify, sprout-social, twilio, uber-for-business, udemy-business, zoho-crm, zoominfo.
2. [ ] **Paylocity is the last app with unchecked core values**, all six. Everything public returns a JS shell to automated fetches, and the real docs live in PEAK (Help → Knowledge Base), which needs a client login. Their SSO PDF on `docs.paylocity.com` is a blank intake form, not documentation. Needs a person with an account. Left as `not_researched` rather than `undocumented`, because nobody has actually looked; flipping it would round the headline to 100% on an app no one has verified.
3. [ ] **Non-core capabilities**, most still not researched:
   | Capability | Not researched |
   |---|---|
   | JIT provisioning | 10 (apps without SSO) |
   | Domain verification | 13 |
   | Group → role mapping | 92 |
   | Custom roles | 95 |
   | Session controls | 85 |
   | API token controls | 98 |
   Suggested order (run as parallel agents, about 10 apps per agent, report-only, the main session edits): JIT and domain verification first (usually on the same SSO docs page), then roles, then sessions and tokens.
4. [ ] Recheck values older than about 6 months (vendors change plans); `checked` dates make this a simple query
5. [ ] Add more apps from [BACKLOG.md](BACKLOG.md): the first 72 P1 rows are done, so continue from P1 row 73, then P2/P3. Use `scratchpad/new/BRIEF.md` + `mk.py` as the pattern. Requests will also arrive through the website's "Add an app"
6. [ ] The 65 apps added on 2026-09-22 are all `draft` — they need plan tiers before they can be published

## To do: site

- [ ] A page per app (`/apps/<id>/`) with all 12 capabilities, sources and notes. Add a "Help wanted" list there of not-researched values
- [ ] Site-wide "Help wanted" view: filter the table to not-researched values
- [ ] Show "last checked" on cells, and flag stale values
- [ ] Remove the `.Site.Data` deprecation warning (switch to `hugo.Data`) once Cloudflare's Hugo is ≥ 0.156

## Research rules (don't skip)

Only the vendor's own pricing page, docs or trust center count. No auto-scanning, Reddit, review sites or blogs. If a value can't be confirmed, use `undocumented`; never carry an old value forward without a source.
