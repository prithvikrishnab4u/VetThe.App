#!/usr/bin/env python3
"""
Compare declared app data with automated verification results and produce a prioritized report.

Run: python scripts/compare_verification.py
Outputs: site/static/data/verification_report.json and verification_report.csv
"""
from pathlib import Path
import json
import csv
import sys


def load_json(p: Path):
    return json.loads(p.read_text())


def main():
    repo = Path(__file__).resolve().parent.parent
    apps_path = repo / 'site' / 'static' / 'data' / 'apps.json'
    auto_path = repo / 'site' / 'static' / 'data' / 'auto_verify.json'
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    if not apps_path.exists() or not auto_path.exists():
        print('Run generate_data.py and auto_verify.py first')
        sys.exit(1)

    apps = load_json(apps_path)
    auto = {r['id']: r for r in load_json(auto_path)}

    rows = []

    for a in apps:
        aid = a.get('_id')
        avr = auto.get(aid, {})
        issues = []

        # SSO mismatch: declared supported but no sso keyword found
        declared_sso = bool(a.get('sso') and a.get('sso').get('supported'))
        found_sso = bool(avr.get('sso'))
        if declared_sso and not found_sso:
            issues.append('sso_not_found')

        # SCIM mismatch
        declared_scim = bool(a.get('scim') and a.get('scim').get('supported'))
        found_scim = bool(avr.get('scim'))
        if declared_scim and not found_scim:
            issues.append('scim_not_found')

        # MFA mismatch
        declared_mfa = bool(a.get('mfa') and a.get('mfa').get('supported'))
        found_mfa = bool(avr.get('mfa'))
        if declared_mfa and not found_mfa:
            issues.append('mfa_not_found')

        # Compliance mismatches
        if a.get('compliance', {}).get('soc2') and not avr.get('soc2'):
            issues.append('soc2_not_found')
        if a.get('compliance', {}).get('iso27001') and not avr.get('iso27001'):
            issues.append('iso27001_not_found')

        # Site unreachable
        if avr.get('http_status') is None:
            issues.append('site_unreachable')

        row = {
            'id': aid,
            'name': a.get('name'),
            'issues': issues,
            'issue_count': len(issues),
            'website': a.get('website'),
            'auto_status': avr.get('http_status')
        }
        rows.append(row)

    # Prioritize by issue_count desc
    rows_sorted = sorted(rows, key=lambda r: (-r['issue_count'], r['name'] or ''))

    # Write JSON
    with open(out_dir / 'verification_report.json', 'w') as f:
        json.dump(rows_sorted, f, indent=2)

    # Write CSV
    csv_path = out_dir / 'verification_report.csv'
    fieldnames = ['id','name','website','issue_count','issues','auto_status']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows_sorted:
            writer.writerow({
                'id': r['id'],
                'name': r['name'],
                'website': r['website'],
                'issue_count': r['issue_count'],
                'issues': ';'.join(r['issues']),
                'auto_status': r['auto_status']
            })

    print(f'Wrote report for {len(rows_sorted)} apps to {out_dir / "verification_report.json"} and {csv_path}')


if __name__ == '__main__':
    main()
