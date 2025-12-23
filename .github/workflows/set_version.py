#!/usr/bin/env python3

import argparse
import os
import re
import sys

# tomlkit preserves formatting/comments unlike standard toml library
import tomlkit


def update_cargo_version(project_root, version):
    """Update version in Cargo.toml file"""
    cargo_path = os.path.join(project_root, "Cargo.toml")

    if not os.path.isfile(cargo_path):
        print(f"Error: Cargo.toml not found at {cargo_path}")
        return False

    try:
        # Load Cargo.toml preserving formatting
        with open(cargo_path) as f:
            data = tomlkit.load(f)

        # Ensure the [package] section exists
        package_section = data.get("package")
        if not isinstance(package_section, (dict, tomlkit.items.Table)):
            print(f"Error: '[package]' section not found or invalid in {cargo_path}")
            return False

        # Update only the package version field
        package_section["version"] = version

        # Write back preserving formatting
        with open(cargo_path, "w") as f:
            f.write(tomlkit.dumps(data))

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
        # Load the pyproject.toml file preserving formatting
        with open(pyproject_path) as f:
            data = tomlkit.load(f)

        # Show the current version
        current_version = data.get("project", {}).get("version", "unknown")
        print(f"Current version: {current_version}")

        # Update the version
        if "project" not in data:
            print("Error: 'project' section not found in pyproject.toml")
            sys.exit(1)

        data["project"]["version"] = version

        # Write back preserving formatting
        with open(pyproject_path, "w") as f:
            f.write(tomlkit.dumps(data))

        print(f"pyproject.toml version updated to: {version}")

        # Also update Cargo.toml with base version (Cargo doesn't support .dev suffixes)
        # Extract base version by stripping any .devN suffix
        cargo_version = re.sub(r'\.dev\d+$', '', version)
        if not update_cargo_version(project_root, cargo_version):
            print("Error: failed to update Cargo.toml")
            sys.exit(1)

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
        with open(pyproject_path) as f:
            data = tomlkit.load(f)
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
