#!/usr/bin/env python3
"""
VetThe.App - app data validator

Checks every data/apps/*.yaml against data/schema.yaml and reports how much of the
data has been verified against a source. Exits 1 if any file has errors.

Run: python scripts/validate.py
"""

import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

import yaml

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / 'data' / 'schema.yaml'
APPS_DIR = REPO / 'data' / 'apps'

ROOT_FIELDS = ['name', 'category', 'website', 'description', 'status', 'capabilities']
CAPABILITY_FIELDS = {'support', 'tier', 'plan', 'notes', 'source', 'checked'}
# Support levels that describe a working feature, so a tier makes sense
TIERED_SUPPORT = {'supported', 'partial'}


def ids(entries):
    return [e['id'] if isinstance(e, dict) else e for e in entries]


def is_url(value):
    return isinstance(value, str) and re.fullmatch(r'https?://\S+', value) is not None


def date_problem(value):
    """Return an error message, or None if value is a quoted YYYY-MM-DD string."""
    if isinstance(value, date):
        return 'must be quoted, e.g. "2026-01-31"'
    try:
        datetime.strptime(str(value), '%Y-%m-%d')
    except ValueError:
        return f"'{value}' must be YYYY-MM-DD"
    return None


def validate_capability(cid, definition, cap, schema, published):
    if not isinstance(cap, dict):
        return [f"{cid}: must be a mapping with at least 'support'"]

    errors = []
    allowed = CAPABILITY_FIELDS | set(definition.get('fields', []))
    for key in cap:
        if key not in allowed:
            errors.append(f"{cid}: unknown field '{key}'")

    support = cap.get('support')
    support_levels = ids(schema['support_levels'])
    if support not in support_levels:
        errors.append(f"{cid}: support '{support}' must be one of: {', '.join(support_levels)}")
        return errors

    tier = cap.get('tier')
    if tier is not None:
        tiers = ids(schema['tiers'])
        if support not in TIERED_SUPPORT:
            errors.append(f"{cid}: tier only applies when support is supported or partial")
        elif tier not in tiers:
            errors.append(f"{cid}: tier '{tier}' must be one of: {', '.join(tiers)}")

    source, checked = cap.get('source'), cap.get('checked')
    if source is not None and not is_url(source):
        errors.append(f"{cid}: source '{source}' must be an http(s) URL")
    if checked is not None:
        problem = date_problem(checked)
        if problem:
            errors.append(f"{cid}: checked {problem}")
    if (source is None) != (checked is None):
        errors.append(f"{cid}: source and checked must be set together")
    if support == 'unknown' and source is not None:
        errors.append(f"{cid}: an unknown capability can't have a source")

    if 'protocols' in cap:
        protocols = cap['protocols']
        if not isinstance(protocols, list) or not protocols:
            errors.append(f"{cid}: protocols must be a non-empty list")
        else:
            for protocol in protocols:
                if protocol not in schema['sso_protocols']:
                    errors.append(f"{cid}: protocol '{protocol}' must be one of: {', '.join(schema['sso_protocols'])}")
        if support not in TIERED_SUPPORT:
            errors.append(f"{cid}: protocols only apply when support is supported or partial")
    if 'retention' in cap and not isinstance(cap['retention'], str):
        errors.append(f"{cid}: retention must be quoted text, e.g. \"90 days\"")

    if published:
        if definition.get('core') and support == 'unknown':
            errors.append(f"{cid}: core capability must be researched before publishing")
        if support != 'unknown' and source is None:
            errors.append(f"{cid}: needs a source and checked date before publishing")
        if support in TIERED_SUPPORT and tier is None:
            errors.append(f"{cid}: needs a tier before publishing")

    return errors


def validate_app(path, schema):
    """Return (data, errors). data is None when the file can't be parsed."""
    try:
        data = yaml.safe_load(path.read_text())
    except yaml.YAMLError as e:
        return None, [f"invalid YAML: {e}"]
    if not isinstance(data, dict):
        return None, ['file must be a YAML mapping']

    errors = []
    for field in ROOT_FIELDS:
        if field not in data:
            errors.append(f"missing '{field}'")
    for field in data:
        if field not in ROOT_FIELDS:
            errors.append(f"unknown field '{field}'")

    if 'category' in data and data['category'] not in schema['categories']:
        errors.append(f"category '{data['category']}' must be one of: {', '.join(schema['categories'])}")
    if 'website' in data and not is_url(data['website']):
        errors.append(f"website '{data['website']}' must be an http(s) URL")
    if 'status' in data and data['status'] not in schema['statuses']:
        errors.append(f"status '{data['status']}' must be one of: {', '.join(schema['statuses'])}")

    caps = data.get('capabilities')
    if not isinstance(caps, dict):
        if 'capabilities' in data:
            errors.append('capabilities must be a mapping')
        return data, errors

    definitions = {c['id']: c for c in schema['capabilities']}
    for cid in caps:
        if cid not in definitions:
            errors.append(f"unknown capability '{cid}'")

    published = data.get('status') == 'published'
    for cid, definition in definitions.items():
        if cid not in caps:
            errors.append(f"missing capability '{cid}'")
            continue
        errors.extend(validate_capability(cid, definition, caps[cid], schema, published))

    return data, errors


def main():
    if not SCHEMA_PATH.exists():
        print(f"{RED}Schema file not found: {SCHEMA_PATH}{RESET}")
        sys.exit(1)
    schema = yaml.safe_load(SCHEMA_PATH.read_text())

    files = sorted(APPS_DIR.glob('*.yaml'))
    if not files:
        print(f"{RED}No YAML files found in {APPS_DIR}{RESET}")
        sys.exit(1)

    print(f"{BLUE}Validating {len(files)} app files...{RESET}\n")

    failed = 0
    statuses = Counter()
    points = Counter()

    for path in files:
        data, errors = validate_app(path, schema)
        if errors:
            failed += 1
            print(f"{RED}✗ {path.stem}{RESET}")
            for error in errors:
                print(f"    {error}")

        if data:
            statuses[data.get('status')] += 1
            for cap in (data.get('capabilities') or {}).values():
                if not isinstance(cap, dict):
                    continue
                if cap.get('support') == 'unknown':
                    points['unknown'] += 1
                elif cap.get('source'):
                    points['verified'] += 1
                else:
                    points['unverified'] += 1

    print(f"\n{'=' * 60}")
    print(f"Apps:        {len(files)} ({statuses['published']} published, {statuses['draft']} draft)")
    print(f"Data points: {sum(points.values())} "
          f"({GREEN}{points['verified']} verified{RESET}, "
          f"{YELLOW}{points['unverified']} unverified{RESET}, "
          f"{points['unknown']} unknown)")
    print(f"{'=' * 60}\n")

    if failed:
        print(f"{RED}{failed} file(s) failed validation.{RESET}")
        sys.exit(1)
    print(f"{GREEN}All files valid ✓{RESET}")


if __name__ == '__main__':
    main()
