#!/usr/bin/env python3
"""
Finalize automated verification: mark apps with no detected issues as `provenance.verified_by: auto-verified`,
and produce a `needs_review.csv` for apps with issues.

Run: python scripts/finalize_verification.py
"""
from pathlib import Path
import json
import csv
import yaml
from datetime import datetime
import sys


def load_json(p: Path):
    return json.loads(p.read_text())


def main():
    repo = Path(__file__).resolve().parent.parent
    data_dir = repo / 'data' / 'apps'
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    vr = load_json(out_dir / 'verification_report.json')
    auto = load_json(out_dir / 'auto_verify.json')

    needs_review = []
    auto_verified = []

    for rec in vr:
        aid = rec['id']
        issues = rec.get('issues', [])
        auto_rec = next((a for a in auto if a.get('id') == aid), {})
        http_status = auto_rec.get('http_status')

        app_path = data_dir / f"{aid}.yaml"
        if not app_path.exists():
            needs_review.append((aid, rec.get('name'), 'missing_yaml'))
            continue

        if rec['issue_count'] == 0 and http_status and int(http_status) >= 200 and int(http_status) < 400:
            # safe to auto-verify
            data = yaml.safe_load(app_path.read_text()) or {}
            prov = data.get('provenance', {})
            if not prov.get('verified_by'):
                prov.update({
                    'source': 'auto-verified',
                    'source_url': auto_rec.get('website') or prov.get('source_url') or '',
                    'verified_by': 'auto-verified',
                    'verified_date': datetime.utcnow().strftime('%Y-%m-%d'),
                    'evidence': ','.join([k for k in ['sso','scim','mfa','soc2','iso27001'] if auto_rec.get(k)])
                })
                data['provenance'] = prov
                app_path.write_text(yaml.safe_dump(data, sort_keys=False))
                auto_verified.append(aid)
        else:
            needs_review.append((aid, rec.get('name'), ';'.join(issues) if issues else 'http_error' ))

    # write needs_review.csv
    with open(out_dir / 'needs_review.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id','name','reason'])
        for r in needs_review:
            writer.writerow(r)

    # summary
    summary = {
        'auto_verified_count': len(auto_verified),
        'needs_review_count': len(needs_review),
        'auto_verified_ids': auto_verified,
    }
    with open(out_dir / 'final_verification_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)

    print('Finalize complete:', summary)


if __name__ == '__main__':
    main()
