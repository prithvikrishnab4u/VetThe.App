#!/usr/bin/env python3
"""
Conservative auto-backfill of `provenance` in `data/apps/*.yaml`.

Rules:
- Only add `provenance` when `site/static/data/auto_verify.json` shows one
  or more positive keyword hits (sso/scim/mfa/soc2/iso27001) or the site is
  reachable (http 200).
- Do not overwrite existing `provenance` blocks.
- Mark `verified_by: auto-scan` and set `checked` to today's date.

This is intentionally conservative and intended as a draft that humans will
review later.
"""
from pathlib import Path
import json
import datetime
import yaml


def load_apps_json(repo_root: Path):
    return json.loads((repo_root / 'site' / 'static' / 'data' / 'apps.json').read_text())


def load_auto_verify(repo_root: Path):
    return {r['id']: r for r in json.loads((repo_root / 'site' / 'static' / 'data' / 'auto_verify.json').read_text())}


def main():
    repo = Path(__file__).resolve().parent.parent
    apps = load_apps_json(repo)
    auto = load_auto_verify(repo)

    data_dir = repo / 'data' / 'apps'
    modified = 0
    failures = 0
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')

    for a in apps:
        aid = a.get('_id')
        auto_r = auto.get(aid, {})
        yaml_path = data_dir / f'{aid}.yaml'
        if not yaml_path.exists():
            failures += 1
            continue

        try:
            doc = yaml.safe_load(yaml_path.read_text()) or {}
        except Exception:
            failures += 1
            continue

        if 'provenance' in doc:
            continue

        # Conservative check: require at least one positive keyword or 200 status
        positives = []
        for k in ('sso','scim','mfa','soc2','iso27001'):
            if auto_r.get(k):
                positives.append(k)

        status_ok = auto_r.get('http_status') and int(auto_r.get('http_status', 0)) == 200

        if not positives and not status_ok:
            continue

        prov = {
            'source': 'auto-scan',
            'source_url': a.get('website') or '',
            'verified_by': 'auto-scan',
            'checked': today,
            'evidence': ','.join(positives) if positives else 'site-reachable'
        }

        doc['provenance'] = prov

        # Write back YAML
        try:
            yaml_text = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True)
            yaml_path.write_text(yaml_text)
            modified += 1
        except Exception:
            failures += 1

    summary = {'modified': modified, 'failures': failures}
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'auto_backfill_report.json').write_text(json.dumps(summary, indent=2))
    print('Auto-backfill summary:', summary)


if __name__ == '__main__':
    main()
