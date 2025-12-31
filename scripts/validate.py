#!/usr/bin/env python3
"""
VetThe.App - YAML Validation Script

This script validates all app YAML files against the schema.
Run: python scripts/validate.py
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Color codes for terminal output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class AppValidator:
    def __init__(self, schema_path: str, data_dir: str):
        """Initialize validator with schema and data directory."""
        self.schema_path = Path(schema_path)
        self.data_dir = Path(data_dir)
        self.schema = self._load_schema()
        self.errors = []
        self.warnings = []

    def _load_schema(self) -> Dict:
        """Load the schema file."""
        try:
            with open(self.schema_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"{RED}Error loading schema: {e}{RESET}")
            sys.exit(1)

    def _load_app_file(self, filepath: Path) -> Tuple[Dict, str]:
        """Load an app YAML file."""
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            return data, None
        except Exception as e:
            return None, f"Failed to parse YAML: {e}"

    def validate_category(self, app_name: str, category: str) -> None:
        """Validate category value."""
        valid_categories = self.schema['categories']
        if category not in valid_categories:
            self.errors.append(
                f"{app_name}: Invalid category '{category}'. "
                f"Must be one of: {', '.join(valid_categories)}"
            )

    def validate_tier(self, app_name: str, field: str, tier: str) -> None:
        """Validate tier value."""
        valid_tiers = self.schema['tiers']
        if tier not in valid_tiers:
            self.errors.append(
                f"{app_name}: Invalid {field} tier '{tier}'. "
                f"Must be one of: {', '.join(valid_tiers)}"
            )

    def validate_sso_protocols(self, app_name: str, protocols: List[str]) -> None:
        """Validate SSO protocols."""
        valid_protocols = self.schema['sso_protocols']
        for protocol in protocols:
            if protocol not in valid_protocols:
                self.errors.append(
                    f"{app_name}: Invalid SSO protocol '{protocol}'. "
                    f"Must be one of: {', '.join(valid_protocols)}"
                )

    def validate_scim_support(self, app_name: str, support_level: str) -> None:
        """Validate SCIM support level."""
        valid_levels = self.schema['scim_support_levels']
        if support_level not in valid_levels:
            self.errors.append(
                f"{app_name}: Invalid SCIM support '{support_level}'. "
                f"Must be one of: {', '.join(valid_levels)}"
            )

    def validate_mfa_types(self, app_name: str, types: List[str]) -> None:
        """Validate MFA types."""
        valid_types = self.schema['mfa_types']
        for mfa_type in types:
            if mfa_type not in valid_types:
                self.errors.append(
                    f"{app_name}: Invalid MFA type '{mfa_type}'. "
                    f"Must be one of: {', '.join(valid_types)}"
                )

    def validate_mfa_enforcement(self, app_name: str, enforcement: str) -> None:
        """Validate MFA enforcement."""
        valid_enforcement = self.schema['mfa_enforcement']
        if enforcement not in valid_enforcement:
            self.errors.append(
                f"{app_name}: Invalid MFA enforcement '{enforcement}'. "
                f"Must be one of: {', '.join(valid_enforcement)}"
            )

    def validate_date(self, app_name: str, date_str: str) -> None:
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            self.errors.append(
                f"{app_name}: Invalid date format '{date_str}'. "
                f"Must be YYYY-MM-DD"
            )

    def validate_url(self, app_name: str, url: str) -> None:
        """Validate URL format."""
        if not url.startswith('http://') and not url.startswith('https://'):
            self.errors.append(
                f"{app_name}: Invalid URL '{url}'. Must start with http:// or https://"
            )

    def check_required_fields(self, app_name: str, data: Dict, section: str, fields: List[str]) -> None:
        """Check if required fields exist."""
        if section == 'root':
            section_data = data
        else:
            section_data = data.get(section, {})
            if not section_data:
                self.errors.append(f"{app_name}: Missing '{section}' section")
                return

        for field in fields:
            if field not in section_data:
                self.errors.append(
                    f"{app_name}: Missing required field '{section}.{field}'"
                )

    def validate_app(self, filepath: Path) -> bool:
        """Validate a single app file."""
        app_name = filepath.stem

        # Load file
        data, error = self._load_app_file(filepath)
        if error:
            self.errors.append(f"{app_name}: {error}")
            return False

        # Check required root fields
        root_fields = self.schema['required_fields']['root']
        self.check_required_fields(app_name, data, 'root', root_fields)

        # Validate basic fields
        if 'category' in data:
            self.validate_category(app_name, data['category'])

        if 'website' in data:
            self.validate_url(app_name, data['website'])

        # Validate SSO section
        if 'sso' in data:
            sso = data['sso']
            sso_fields = self.schema['required_fields']['sso']
            self.check_required_fields(app_name, data, 'sso', sso_fields)

            if sso.get('supported'):
                if 'protocols' not in sso or not sso['protocols']:
                    self.errors.append(f"{app_name}: SSO is supported but no protocols specified")
                elif sso.get('protocols'):
                    self.validate_sso_protocols(app_name, sso['protocols'])

                if 'tier' in sso:
                    self.validate_tier(app_name, 'SSO', sso['tier'])

        # Validate SCIM section
        if 'scim' in data:
            scim = data['scim']
            scim_fields = self.schema['required_fields']['scim']
            self.check_required_fields(app_name, data, 'scim', scim_fields)

            if 'supported' in scim:
                self.validate_scim_support(app_name, scim['supported'])

                if scim['supported'] in ['full', 'partial']:
                    if 'version' not in scim:
                        self.errors.append(f"{app_name}: SCIM is {scim['supported']} but no version specified")

                if 'tier' in scim:
                    self.validate_tier(app_name, 'SCIM', scim['tier'])

        # Validate MFA section
        if 'mfa' in data:
            mfa = data['mfa']
            mfa_fields = self.schema['required_fields']['mfa']
            self.check_required_fields(app_name, data, 'mfa', mfa_fields)

            if mfa.get('supported'):
                if 'types' not in mfa or not mfa['types']:
                    self.errors.append(f"{app_name}: MFA is supported but no types specified")
                elif mfa.get('types'):
                    self.validate_mfa_types(app_name, mfa['types'])

                if 'enforcement' in mfa:
                    self.validate_mfa_enforcement(app_name, mfa['enforcement'])

                if 'tier' in mfa:
                    self.validate_tier(app_name, 'MFA', mfa['tier'])

        # Validate compliance section
        if 'compliance' in data:
            comp_fields = self.schema['required_fields']['compliance']
            self.check_required_fields(app_name, data, 'compliance', comp_fields)

        # Validate meta section
        if 'meta' in data:
            meta = data['meta']
            meta_fields = self.schema['required_fields']['meta']
            self.check_required_fields(app_name, data, 'meta', meta_fields)

            if 'last_verified' in meta:
                self.validate_date(app_name, meta['last_verified'])

            # Warning if not ready to publish
            if meta.get('ready_to_publish') is False:
                self.warnings.append(f"{app_name}: Marked as not ready to publish")

        return len(self.errors) == 0

    def validate_all(self) -> Tuple[int, int]:
        """Validate all app files in the data directory."""
        app_files = sorted(self.data_dir.glob('*.yaml'))

        if not app_files:
            print(f"{RED}No YAML files found in {self.data_dir}{RESET}")
            return 0, 0

        print(f"{BLUE}Validating {len(app_files)} app files...{RESET}\n")

        valid_count = 0
        invalid_count = 0

        for filepath in app_files:
            initial_error_count = len(self.errors)
            self.validate_app(filepath)

            if len(self.errors) == initial_error_count:
                valid_count += 1
                print(f"{GREEN}✓{RESET} {filepath.stem}")
            else:
                invalid_count += 1
                print(f"{RED}✗{RESET} {filepath.stem}")

        return valid_count, invalid_count

    def print_results(self, valid_count: int, invalid_count: int) -> None:
        """Print validation results."""
        print(f"\n{'='*60}")
        print(f"{BLUE}Validation Results{RESET}")
        print(f"{'='*60}\n")

        total = valid_count + invalid_count
        print(f"Total files: {total}")
        print(f"{GREEN}Valid: {valid_count}{RESET}")
        print(f"{RED}Invalid: {invalid_count}{RESET}")

        if self.warnings:
            print(f"\n{YELLOW}Warnings ({len(self.warnings)}):{RESET}")
            for warning in self.warnings:
                print(f"  {YELLOW}⚠{RESET}  {warning}")

        if self.errors:
            print(f"\n{RED}Errors ({len(self.errors)}):{RESET}")
            for error in self.errors:
                print(f"  {RED}✗{RESET} {error}")

        print(f"\n{'='*60}\n")

        if invalid_count > 0:
            print(f"{RED}Validation failed. Please fix the errors above.{RESET}")
            sys.exit(1)
        else:
            print(f"{GREEN}All files valid! ✓{RESET}")
            sys.exit(0)


def main():
    """Main function."""
    # Get project root (script is in scripts/, project root is parent)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    schema_path = project_root / 'schemas' / 'app-schema.yaml'
    data_dir = project_root / 'data' / 'apps'

    if not schema_path.exists():
        print(f"{RED}Schema file not found: {schema_path}{RESET}")
        sys.exit(1)

    if not data_dir.exists():
        print(f"{RED}Data directory not found: {data_dir}{RESET}")
        sys.exit(1)

    validator = AppValidator(schema_path, data_dir)
    valid_count, invalid_count = validator.validate_all()
    validator.print_results(valid_count, invalid_count)


if __name__ == '__main__':
    main()