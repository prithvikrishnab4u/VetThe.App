#!/usr/bin/env python3
"""
Probe common vendor paths (security, trust, docs, support) for apps listed in needs_review.csv.
Writes site/static/data/alt_path_checks.json and alt_path_checks.csv with first-match results.
"""
from pathlib import Path
import csv
import json
import requests
import time

COMMON_PATHS = [
    '/security', '/trust', '/trust/security', '/security.html', '/security/privacy',
    '/docs', '/documentation', '/help', '/support', '/developers', '/developer',
    '/.well-known/security.txt', '/security/overview'
]


def main():
    repo = Path(__file__).resolve().parent.parent
    needs = repo / 'site' / 'static' / 'data' / 'needs_review.csv'
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    if not needs.exists():
        print('needs_review.csv not found')
        return

    rows = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'VetThe.App AltPathChecker/1.0'})

    with needs.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            aid = r['id']
            name = r['name']
            website = None
            # attempt to find website from apps.json
            apps_json = repo / 'site' / 'static' / 'data' / 'apps.json'
            if apps_json.exists():
                import json as _j
                apps = _j.loads(apps_json.read_text())
                for a in apps:
                    if a.get('_id') == aid:
                        website = a.get('website')
                        break

            entry = {'id': aid, 'name': name, 'website': website, 'found': False, 'found_url': '', 'status': ''}
            if not website:
                rows.append(entry)
                continue

            for p in COMMON_PATHS:
                url = website.rstrip('/') + p
                try:
                    resp = session.get(url, timeout=10)
                    status = resp.status_code
                    if 200 <= status < 400:
                        entry.update({'found': True, 'found_url': url, 'status': status})
                        break
                except requests.RequestException:
                    pass
                time.sleep(0.2)

            rows.append(entry)

    # write JSON and CSV
    (out_dir / 'alt_path_checks.json').write_text(json.dumps(rows, indent=2))
    csv_path = out_dir / 'alt_path_checks.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id','name','website','found','found_url','status'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print('Wrote alt path checks to', out_dir / 'alt_path_checks.json')


if __name__ == '__main__':
    main()
