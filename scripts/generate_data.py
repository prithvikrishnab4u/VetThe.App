#!/usr/bin/env python3
"""
Generate JSON and CSV exports from `data/apps/*.yaml` into `site/static/data/`.

apps.json keeps the full records plus `_id` (the filename). apps.csv has one row per app
with support/tier/source/checked columns for every capability in data/schema.yaml.

Run: python scripts/generate_data.py
"""
import csv
import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
CAPABILITY_COLUMNS = ['support', 'tier', 'source', 'checked']


def main():
    schema = yaml.safe_load((REPO / 'data' / 'schema.yaml').read_text())
    capability_ids = [c['id'] for c in schema['capabilities']]
    out_dir = REPO / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    apps = []
    for path in sorted((REPO / 'data' / 'apps').glob('*.yaml')):
        data = yaml.safe_load(path.read_text()) or {}
        data['_id'] = path.stem
        apps.append(data)

    with open(out_dir / 'apps.json', 'w') as f:
        json.dump(apps, f, indent=2, sort_keys=True, default=str)

    fieldnames = ['id', 'name', 'category', 'website', 'status']
    fieldnames += [f'{cid}_{column}' for cid in capability_ids for column in CAPABILITY_COLUMNS]

    csv_path = out_dir / 'apps.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for app in apps:
            row = {
                'id': app['_id'],
                'name': app.get('name'),
                'category': app.get('category'),
                'website': app.get('website'),
                'status': app.get('status'),
            }
            capabilities = app.get('capabilities') if isinstance(app.get('capabilities'), dict) else {}
            for cid in capability_ids:
                cap = capabilities.get(cid) if isinstance(capabilities.get(cid), dict) else {}
                for column in CAPABILITY_COLUMNS:
                    row[f'{cid}_{column}'] = cap.get(column, '')
            writer.writerow(row)

    print(f"Wrote {len(apps)} apps to {out_dir / 'apps.json'} and {csv_path}")


if __name__ == '__main__':
    main()
