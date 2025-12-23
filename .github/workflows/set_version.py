#!/usr/bin/env python3

import argparse
import os
import re
import sys

# Replace tomllib with toml (needs to be installed with pip)
import toml


def update_cargo_version(project_root, version):
    """Update version in Cargo.toml file"""
    cargo_path = os.path.join(project_root, "Cargo.toml")

    if not os.path.isfile(cargo_path):
        print(f"Warning: Cargo.toml not found at {cargo_path}")
        return False

    try:
        with open(cargo_path) as f:
            content = f.read()

        # Use regex to replace version in [package] section
        # Match: version = "X.Y.Z" in the package section
        new_content = re.sub(
            r'^(version\s*=\s*")[^"]+(")',
            rf'\g<1>{version}\g<2>',
            content,
            count=1,
            flags=re.MULTILINE
        )

        with open(cargo_path, "w") as f:
            f.write(new_content)

        print(f"Cargo.toml version updated to: {version}")
        return True

    except Exception as e:
        print(f"Error updating Cargo.toml: {e}")
        return False


def update_version(version):
    """Update project version in pyproject.toml and Cargo.toml files"""
    # Get the project root directory (assuming script is in .github/workflows)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pyproject_path = os.path.join(project_root, "pyproject.toml")

    # Check if pyproject.toml exists
    if not os.path.isfile(pyproject_path):
        print(f"Error: pyproject.toml not found at {pyproject_path}")
        sys.exit(1)

    try:
        # Load the pyproject.toml file
        data = toml.load(pyproject_path)

        # Show the current version
        current_version = data.get("project", {}).get("version", "unknown")
        print(f"Current version: {current_version}")

        # Update the version
        if "project" not in data:
            print("Error: 'project' section not found in pyproject.toml")
            sys.exit(1)

        data["project"]["version"] = version

        # Write the updated content back to the file
        with open(pyproject_path, "w") as f:
            toml.dump(data, f)

        print(f"pyproject.toml version updated to: {version}")

        # Also update Cargo.toml
        update_cargo_version(project_root, version)

    except Exception as e:
        print(f"Error updating version: {e}")
        sys.exit(1)


def get_base_version():
    """Get the base version from pyproject.toml (without any dev suffix)"""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pyproject_path = os.path.join(project_root, "pyproject.toml")

    if not os.path.isfile(pyproject_path):
        print(f"Error: pyproject.toml not found at {pyproject_path}", file=sys.stderr)
        sys.exit(1)

    try:
        data = toml.load(pyproject_path)
        version = data.get("project", {}).get("version", "0.0.0")
        # Strip any existing dev suffix to get clean base version
        base_version = re.sub(r'\.dev\d+$', '', version)
        return base_version
    except Exception as e:
        print(f"Error reading version: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Update project version in pyproject.toml and Cargo.toml")
    parser.add_argument("version", nargs="?", help="New version to set (e.g., '0.1.0')")
    parser.add_argument("--get-base", action="store_true", help="Print the base version from pyproject.toml and exit")

    args = parser.parse_args()

    if args.get_base:
        # Just print the base version (for use in shell scripts)
        print(get_base_version())
    elif args.version:
        # Update the version
        update_version(args.version)
    else:
        parser.error("Either provide a version or use --get-base")
