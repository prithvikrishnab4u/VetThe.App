Content model & taxonomy
=========================

Primary record: App (one YAML file per app under `data/apps/`).

Key fields (already in schema):
- `name`, `category`, `website`, `description` (root)
- `sso`: `supported` (bool), `protocols` (list), `tier`, `sp_initiated`, `jit_provisioning`
- `scim`: `supported`, `tier`, `version`
- `mfa`: `supported`, `types` (list), `enforcement`, `tier`
- `compliance`: `soc2`, `iso27001` (booleans)
- `meta`: `last_verified` (YYYY-MM-DD), `ready_to_publish` (bool)
- `provenance` (optional): `source`, `source_url`, `verified_by`, `verified_date`, `evidence`

Taxonomy (categories): Use values defined in `schemas/app-schema.yaml` to tag apps.

Notes:
- Keep `provenance` populated when adding or changing an app to improve trust.
- Use `meta.last_verified` to drive staleness warnings and re-verification workflows.
