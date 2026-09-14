#!/usr/bin/env python3
"""
Generate JSON and CSV exports from `data/apps/*.yaml` into `site/static/data/`.

Run: python scripts/generate_data.py
"""
from pathlib import Path
import yaml
import json
import csv
import sys


def load_app(path: Path):
    with open(path, 'r') as f:
        return yaml.safe_load(f) or {}


def main():
    repo = Path(__file__).resolve().parent.parent
    data_dir = repo / 'data' / 'apps'
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    apps = []
    for p in sorted(data_dir.glob('*.yaml')):
        data = load_app(p)
        data['_id'] = p.stem
        apps.append(data)

    # Write JSON
    with open(out_dir / 'apps.json', 'w') as f:
        json.dump(apps, f, indent=2, sort_keys=True, default=str)

    # Write CSV (flatten some common fields)
    csv_path = out_dir / 'apps.csv'
    fieldnames = [
        'id', 'name', 'category', 'website', 'sso_supported', 'sso_protocols',
        'scim_supported', 'mfa_supported', 'mfa_types', 'compliance_soc2',
        'compliance_iso27001', 'meta_last_verified', 'meta_ready_to_publish'
    ]

    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for app in apps:
            row = {
                'id': app.get('_id'),
                'name': app.get('name'),
                'category': app.get('category'),
                'website': app.get('website'),
                'sso_supported': app.get('sso', {}).get('supported') if isinstance(app.get('sso'), dict) else '',
                'sso_protocols': ','.join(app.get('sso', {}).get('protocols', [])) if isinstance(app.get('sso'), dict) else '',
                'scim_supported': app.get('scim', {}).get('supported') if isinstance(app.get('scim'), dict) else '',
                'mfa_supported': app.get('mfa', {}).get('supported') if isinstance(app.get('mfa'), dict) else '',
                'mfa_types': ','.join(app.get('mfa', {}).get('types', [])) if isinstance(app.get('mfa'), dict) else '',
                'compliance_soc2': app.get('compliance', {}).get('soc2') if isinstance(app.get('compliance'), dict) else '',
                'compliance_iso27001': app.get('compliance', {}).get('iso27001') if isinstance(app.get('compliance'), dict) else '',
                'meta_last_verified': app.get('meta', {}).get('last_verified') if isinstance(app.get('meta'), dict) else '',
                'meta_ready_to_publish': app.get('meta', {}).get('ready_to_publish') if isinstance(app.get('meta'), dict) else '',
            }
            writer.writerow(row)

    print(f"Wrote {len(apps)} apps to {out_dir / 'apps.json'} and {csv_path}")


if __name__ == '__main__':
    main()
