Success metrics and governance
=============================

Suggested KPIs:
- Coverage: number of apps with complete root fields / total apps.
- Verification rate: percent of apps with `provenance.verified_by` populated.
- Freshness: median days since `meta.last_verified`.
- PR throughput: PRs merged per month and validation failures per PR.

Governance (suggested):
- Contributors submit PRs with `provenance.source` and `source_url`.
- Maintainers verify evidence before merging; CI flags missing provenance.
- Periodic re-validation job triggers reminders for apps with old `last_verified`.
