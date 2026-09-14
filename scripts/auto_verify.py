#!/usr/bin/env python3
"""
Automated lightweight verification of app data.

Checks:
- HTTP status of `website` URL
- Presence of keywords on the landing page related to SSO, SCIM, MFA, SOC2, ISO27001

Outputs `site/static/data/auto_verify.json` and `auto_verify.csv`.
"""
from pathlib import Path
import json
import csv
import sys
import time
from urllib.parse import urlparse

import requests


KEYWORDS = {
    'sso': ['sso', 'single sign-on', 'saml', 'oidc', 'openID', 'oauth'],
    'scim': ['scim', 'provision', 'provisioning', 'provisioning API'],
    'mfa': ['mfa', 'multi-factor', 'two-factor', '2fa', 'totp', 'webauthn', 'security key'],
    'soc2': ['soc 2', 'soc2'],
    'iso27001': ['iso 27001', 'iso27001']
}


def scan_text_for_keywords(text: str, keywords):
    txt = text.lower()
    found = {}
    for k, kws in keywords.items():
        found[k] = any(kw.lower() in txt for kw in kws)
    return found


def main():
    repo = Path(__file__).resolve().parent.parent
    apps_json = repo / 'site' / 'static' / 'data' / 'apps.json'
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    if not apps_json.exists():
        print('apps.json not found. Run scripts/generate_data.py first.')
        sys.exit(1)

    apps = json.loads(apps_json.read_text())

    results = []

    session = requests.Session()
    session.headers.update({'User-Agent': 'VetThe.App AutoVerify/1.0 (+https://vetthe.app)'})

    for a in apps:
        rec = {'id': a.get('_id'), 'name': a.get('name'), 'website': a.get('website')}
        url = a.get('website')
        if not url:
            rec.update({'http_status': None, 'error': 'no-website'})
            results.append(rec)
            continue

        try:
            # ensure scheme
            parsed = urlparse(url)
            if not parsed.scheme:
                url = 'https://' + url

            r = session.get(url, timeout=10)
            rec['http_status'] = r.status_code
            rec.update(scan_text_for_keywords(r.text, KEYWORDS))
        except requests.RequestException as e:
            rec['http_status'] = None
            rec['error'] = str(e)

        results.append(rec)
        time.sleep(0.2)

    # Write JSON and CSV
    with open(out_dir / 'auto_verify.json', 'w') as f:
        json.dump(results, f, indent=2)

    csv_path = out_dir / 'auto_verify.csv'
    fieldnames = ['id', 'name', 'website', 'http_status', 'sso', 'scim', 'mfa', 'soc2', 'iso27001', 'error']
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, '') for k in fieldnames})

    print(f'Wrote {len(results)} verification results to {out_dir / "auto_verify.json"} and {csv_path}')


if __name__ == '__main__':
    main()
