# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

VetThe.App is a static Hugo site that catalogues the **IAM capabilities** of SaaS apps. For each app it records whether a capability is supported, the minimum plan needed, and the source it was checked against. Covered: SSO, enforcing SSO, SCIM, enforcing MFA, passkeys, audit logs, JIT provisioning, domain verification, custom roles, group → role mapping, session controls, and API token controls. It deliberately goes beyond sso.tax, which only covers SSO pricing. Target users are identity engineers, procurement, and security auditors, so a sourced value is worth more than wide coverage. No backend; the site deploys to Cloudflare Pages (no deploy config in the repo).

## Commands

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt   # PyYAML only

.venv/bin/python scripts/validate.py        # schema check of data/apps/*.yaml; prints only failures + coverage summary; exits 1 on error (CI gate)
.venv/bin/python scripts/generate_data.py   # writes site/static/data/apps.json + apps.csv (committed; rerun after editing YAML)

# Site (run in site/). npm deps are required: Hugo's css.TailwindCSS calls the Tailwind v4 CLI
npm ci
hugo server     # http://localhost:1313
hugo --minify   # production build -> site/public/
```

No test suite or linter. CI (`.github/workflows/ci.yml`) runs generate_data → validate → `npm ci` → `hugo --minify`. `validate-pr.yml` runs the validator on data/schema changes and comments on the PR.

## Architecture

**`data/schema.yaml` drives everything.** It lists the capabilities in column order, with each one's label, question, `core` flag and extra `fields`. It also defines categories, statuses, support levels, tiers and SSO protocols. Because Hugo's `dataDir` is `../data`, the same file is read by:
- `scripts/validate.py` (rules)
- `scripts/generate_data.py` (CSV columns)
- Hugo as `site.Data.schema`: `partials/table.html` builds columns, cells and filters from it, and `partials/guide.html` builds the legend

Adding a capability to the schema therefore adds it to the site, the CSV and validation. Existing app files then fail validation until each gets the new block.

**App files** (`data/apps/<id>.yaml`, the filename stem is the ID) have root `name, category, website, description, status, capabilities`. Each capability is `support` plus optional `tier, plan, notes, source, checked`, plus schema-listed extras (`sso.protocols`, `audit_logs.retention`). Validator rules:
- `tier` only on `supported`/`partial`.
- `source` and `checked` must appear together; `checked` must be a quoted `YYYY-MM-DD`.
- `undocumented` (checked, vendor silent) and `not_researched` (never looked) can't have a source.
- Unknown root, capability or field keys are errors.
- `status: published` also requires every core capability ≠ not_researched, a source on every value other than undocumented/not_researched, and a tier on every supported/partial value.

**Rendering:** `table.html` turns each cell into a `data-value` label (tier label, "Supported", "Partial", "No", "Not documented", "Not researched"). `scripts.html` filters and sorts on those labels using `VALUE_ORDER`, so if you add a tier, update that list too. Styling:
- Values without a `source` get the `.unverified` class (faded).
- Non-core columns get `.cap-extended`, hidden until the "Show all capabilities" toggle adds `.show-extended` to the table.
- All custom CSS lives in `site/assets/css/main.css` (Tailwind v4, no config file).

## Data state and working rules

- All 107 apps are `draft`. Their values were carried over from an earlier dataset (probably generated in bulk, not researched) and have **no sources**, so treat every existing value as unverified.
- Accuracy work means checking each value against the vendor's own pricing page, docs, or trust center, and adding `source` + `checked`. Don't use auto-scanning, homepage keyword matches, Reddit, review sites, or blogs. When a value can't be confirmed, set it to `undocumented` instead of guessing, and don't carry old values forward.
- Keep the double-quoted YAML style from the `CONTRIBUTING.md` template; contributors edit these files in the GitHub web UI.
