#!/usr/bin/env python3
"""Generate a markdown list of roles with descriptions from their metadata."""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def generate_role_list():
    """Generate markdown list of roles from their meta/main.yml files."""
    roles_dir = Path("roles")

    if not roles_dir.exists():
        print(f"Error: {roles_dir} directory not found", file=sys.stderr)
        sys.exit(1)

    role_list = []

    for role_path in sorted(roles_dir.iterdir()):
        if not role_path.is_dir() or role_path.name.startswith('.'):
            continue

        meta_file = role_path / "meta" / "main.yml"
        if not meta_file.exists():
            print(f"Warning: {meta_file} not found, skipping {role_path.name}", file=sys.stderr)
            continue

        try:
            with open(meta_file, 'r') as f:
                meta = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"Warning: Failed to parse {meta_file}: {e}", file=sys.stderr)
            continue

        description = meta.get("galaxy_info", {}).get("description", "No description available")
        role_name = role_path.name

        role_list.append(f"* [{role_name}](roles/{role_name}/README.md) - {description}")

    if not role_list:
        print("Warning: No roles found", file=sys.stderr)

    return "\n".join(role_list)


if __name__ == "__main__":
    print(generate_role_list())
