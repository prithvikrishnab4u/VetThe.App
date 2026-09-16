# Roadmap

Running log of what's done and what's next. **Update this file at the end of every work session**: tick items off, add what you found, and refresh the numbers with `.venv/bin/python scripts/validate.py`.

_Last updated: 2026-09-16_

## Where the data stands

107 apps, all `draft`. 1,284 data points:

| | Count |
|---|---|
| Verified (has `source` + `checked`) | 467 |
| Unverified (a value with no source, carried over from the old dataset) | 17 |
| Not documented (checked, the vendor says nothing) | 185 |
| Not researched | 615 |

## Done

- [x] Data model: 12 IAM capabilities, each with support, minimum tier, plan, notes, source, checked (`data/schema.yaml`)
- [x] Split `unknown` into `undocumented` and `not_researched`
- [x] **Core capabilities** (SSO, Enforce SSO, SCIM, Enforce MFA, Passkeys, Audit logs) checked against vendor docs for all 107 apps, apart from Snyk (see below)
- [x] Landing page redesign: hero, dark mode, compact layout so the table shows on the first screen
- [x] Deployed on Cloudflare Pages at vetthe.app
- [x] Contribute from the website: ✎ on every cell and "Add an app" open a form, and `site/functions/api/suggest.js` opens a pull request (Turnstile spam check, server-side validation)
- [x] GitHub issue forms (correct a value, request an app)
- [x] PR validation posts one comment showing the actual errors, updated on each push

## To do: setup (one-off, needed before website suggestions work)

- [ ] Fine-grained GitHub token for this repo only: Contents read/write, Pull requests read/write, Issues read/write (for the label)
- [ ] Cloudflare Turnstile widget for `vetthe.app`
- [ ] Cloudflare Pages → Settings → Variables: `GITHUB_TOKEN` (secret), `TURNSTILE_SECRET` (secret), `HUGO_PARAMS_TURNSTILESITEKEY` (plain)
- [ ] Confirm the Pages project's root directory is `site`, so `site/functions/` is deployed
- [ ] Create the `community-suggestion`, `data-fix` and `app-request` labels
- [ ] Pin the Hugo version in Cloudflare (`HUGO_VERSION`) to match local builds. Cloudflare currently uses 0.147.7, which is why templates use `site.Data`

## To do: data (in priority order)

1. [ ] **Snyk core values have no source**: `sso`, `mfa_enforcement`, `phishing_resistant_mfa`. Verify them or set `undocumented`.
2. [ ] **Unverified non-core leftovers**, verify or reset to `not_researched`:
   - `session_controls`: atlassianconfluence, atlassianjira, github, hubspot, linear, notion, slack
   - `domain_verification`: 1password, datadog, pagerduty, snowflake, snyk
   - `jit_provisioning`: snowflake, snyk
3. [ ] **Publish apps**: flip `status` to `published` for each app whose core is complete (the validator enforces the rules)
4. [ ] **Non-core capabilities**, most still not researched:
   | Capability | Not researched |
   |---|---|
   | JIT provisioning | 70 |
   | Domain verification | 81 |
   | Group → role mapping | 95 |
   | Custom roles | 97 |
   | Session controls | 89 |
   | API token controls | 99 |
   Suggested order: JIT and domain verification first (usually on the same SSO docs page), then roles, then sessions and tokens.
5. [ ] Recheck values older than about 6 months (vendors change plans); `checked` dates make this a simple query
6. [ ] Add more apps. Many requests will arrive through the website's "Add an app"

## To do: site

- [ ] A page per app (`/apps/<id>/`) with all 12 capabilities, sources and notes. Add a "Help wanted" list there of not-researched values
- [ ] Site-wide "Help wanted" view: filter the table to not-researched values
- [ ] Show "last checked" on cells, and flag stale values
- [ ] Remove the `.Site.Data` deprecation warning (switch to `hugo.Data`) once Cloudflare's Hugo is ≥ 0.156

## Research rules (don't skip)

Only the vendor's own pricing page, docs or trust center count. No auto-scanning, Reddit, review sites or blogs. If a value can't be confirmed, use `undocumented`; never carry an old value forward without a source.
