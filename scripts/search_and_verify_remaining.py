#!/usr/bin/env python3
"""
Search remaining apps using DuckDuckGo HTML results and verify vendor pages conservatively.

For each app in `site/static/data/needs_review.csv`:
- Run a few DuckDuckGo queries (site:domain security, domain trust, domain docs).
- Parse result links and fetch candidate pages.
- Scan for verification keywords and, if found, add a conservative `provenance` to `data/apps/<id>.yaml`.

Writes `site/static/data/search_verify_report.json` and commits nothing by itself.
"""
from pathlib import Path
import csv
import json
import re
import time
import requests
import yaml

KEYWORDS = ['security', 'trust', 'scim', 'sso', 'single sign-on', 'saml', 'mfa', 'multi-factor', 'soc2', 'iso 27001', 'iso27001']

DDG_BASE = 'https://html.duckduckgo.com/html/'


def ddg_search(query, session):
    r = session.post(DDG_BASE, data={'q': query}, timeout=10)
    # extract hrefs
    hrefs = re.findall(r'href="(https?://[^"]+)"', r.text)
    return hrefs


def scan_text_for_keywords(text):
    txt = text.lower()
    found = [k for k in KEYWORDS if k in txt]
    return found


def main():
    repo = Path(__file__).resolve().parent.parent
    needs = repo / 'site' / 'static' / 'data' / 'needs_review.csv'
    apps_json = repo / 'site' / 'static' / 'data' / 'apps.json'
    out_dir = repo / 'site' / 'static' / 'data'
    out_dir.mkdir(parents=True, exist_ok=True)

    if not needs.exists():
        print('needs_review.csv not found')
        return

    apps = {}
    if apps_json.exists():
        apps = {a['_id']: a for a in json.loads(apps_json.read_text())}

    session = requests.Session()
    session.headers.update({'User-Agent': 'VetThe.App SearchVerifier/1.0'})

    report = []

    with needs.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            aid = r['id']
            name = r['name']
            website = apps.get(aid, {}).get('website') if apps else None
            entry = {'id': aid, 'name': name, 'website': website, 'verified': False, 'source_url': '', 'evidence': ''}

            queries = []
            if website:
                domain = re.sub(r'^https?://', '', website).split('/')[0]
                queries = [f'site:{domain} security', f'site:{domain} trust', f'site:{domain} docs']
            else:
                queries = [f'{name} security', f'{name} trust', f'{name} docs']

            candidates = []
            for q in queries:
                try:
                    hrefs = ddg_search(q, session)
                    candidates.extend(hrefs)
                except requests.RequestException:
                    pass
                time.sleep(0.5)

            # de-duplicate while preserving order
            seen = set()
            candidates = [h for h in candidates if not (h in seen or seen.add(h))]

            for url in candidates[:10]:
                try:
                    resp = session.get(url, timeout=10)
                    if resp.status_code >= 400:
                        continue
                    found = scan_text_for_keywords(resp.text)
                    if found:
                        entry.update({'verified': True, 'source_url': url, 'evidence': ','.join(found)})
                        break
                except requests.RequestException:
                    continue
                time.sleep(0.3)

            # If verified, write provenance into YAML if missing
            if entry['verified']:
                yaml_path = repo / 'data' / 'apps' / f'{aid}.yaml'
                if yaml_path.exists():
                    try:
                        doc = yaml.safe_load(yaml_path.read_text()) or {}
                        if 'provenance' not in doc:
                            doc['provenance'] = {
                                'source': 'auto-search',
                                'source_url': entry['source_url'],
                                'verified_by': 'auto-search',
                                'checked': time.strftime('%Y-%m-%d'),
                                'evidence': entry['evidence']
                            }
                            yaml_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
                    except Exception:
                        pass

            report.append(entry)

    (out_dir / 'search_verify_report.json').write_text(json.dumps(report, indent=2))
    print('Wrote search+verify report to', out_dir / 'search_verify_report.json')


if __name__ == '__main__':
    main()
