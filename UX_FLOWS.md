Key UX flows and pages
======================

1) Catalog (home)
- Grid or table of apps with quick filters (category, SSO protocol, SCIM support, MFA types, compliance).
- Actions: select app for details, add to comparison.

2) App detail page
- Full YAML-derived details, provenance/evidence, and links to vendor docs.
- Show badges: `verified`, `community-sourced`, `needs-review`.

3) Comparison view
- Multi-select apps, show side-by-side matrix of fields, export to CSV.

4) Data export/API
- Provide `site/static/data/apps.json` and `apps.csv` for integrations.

5) Contributor flow
- Edit via GitHub PRs, validation runs on CI, maintainers verify provenance before merging.
