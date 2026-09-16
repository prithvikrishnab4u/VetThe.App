# Roadmap

Running log of what's done and what's next. **Update this file at the end of every work session**: tick items off, add what you found, and refresh the numbers with `.venv/bin/python scripts/validate.py`.

_Last updated: 2026-09-16_

## Remind the user

- **Website suggestions aren't switched on yet.** Ask whether the Cloudflare setup below is done (GitHub token, Turnstile widget, three variables, redeploy). Step-by-step instructions were given on 2026-09-16; repeat them if asked.

## In progress

- Nothing running.

## Where the data stands

107 apps, all `draft`. 1,284 data points:

| | Count |
|---|---|
| Verified (has `source` + `checked`) | 583 |
| Unverified (a value with no source, carried over from the old dataset) | 0 |
| Not documented (checked, the vendor says nothing) | 308 |
| Not researched | 393 |

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
- [x] **BACKLOG.md:** 299 widely used apps not yet in the data, ranked P1/P2/P3. The agent wrote the websites from memory, so confirm them while researching.

## To do: setup (one-off, needed before website suggestions work; user will do this)

- [ ] Fine-grained GitHub token for this repo only: Contents read/write, Pull requests read/write, Issues read/write (for the label)
- [ ] Cloudflare Turnstile widget for `vetthe.app`
- [ ] Cloudflare Pages → Settings → Variables: `GITHUB_TOKEN` (secret), `TURNSTILE_SECRET` (secret), `HUGO_PARAMS_TURNSTILESITEKEY` (plain)
- [ ] Confirm the Pages project's root directory is `site`, so `site/functions/` is deployed
- [ ] Create the `community-suggestion`, `data-fix` and `app-request` labels
- [ ] Pin the Hugo version in Cloudflare (`HUGO_VERSION`) to match local builds. Cloudflare currently uses 0.147.7, which is why templates use `site.Data`

## To do: data (in priority order)

1. [ ] **Publish apps**: flip `status` to `published` for each app whose core is complete (the validator enforces the rules)
2. [ ] **Non-core capabilities**, most still not researched:
   | Capability | Not researched |
   |---|---|
   | JIT provisioning | 10 (apps without SSO) |
   | Domain verification | 13 |
   | Group → role mapping | 92 |
   | Custom roles | 95 |
   | Session controls | 85 |
   | API token controls | 98 |
   Suggested order (run as parallel agents, about 10 apps per agent, report-only, the main session edits): JIT and domain verification first (usually on the same SSO docs page), then roles, then sessions and tokens.
3. [ ] Recheck values older than about 6 months (vendors change plans); `checked` dates make this a simple query
4. [ ] Add more apps from [BACKLOG.md](BACKLOG.md), P1 first (core capabilities for each). Requests will also arrive through the website's "Add an app"

## To do: site

- [ ] A page per app (`/apps/<id>/`) with all 12 capabilities, sources and notes. Add a "Help wanted" list there of not-researched values
- [ ] Site-wide "Help wanted" view: filter the table to not-researched values
- [ ] Show "last checked" on cells, and flag stale values
- [ ] Remove the `.Site.Data` deprecation warning (switch to `hugo.Data`) once Cloudflare's Hugo is ≥ 0.156

## Research rules (don't skip)

Only the vendor's own pricing page, docs or trust center count. No auto-scanning, Reddit, review sites or blogs. If a value can't be confirmed, use `undocumented`; never carry an old value forward without a source.
