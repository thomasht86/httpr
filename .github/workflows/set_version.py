#!/usr/bin/env python3

import argparse
import os
import sys

import tomllib


def update_version(version):
    """Update project version in pyproject.toml file"""
    # Get the project root directory (assuming script is in .github/workflows)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pyproject_path = os.path.join(project_root, "pyproject.toml")

    # Check if pyproject.toml exists
    if not os.path.isfile(pyproject_path):
        print(f"Error: pyproject.toml not found at {pyproject_path}")
        sys.exit(1)

    try:
        # Load the pyproject.toml file
        data = tomllib.load(pyproject_path)

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
            tomllib.dump(data, f)

        print(f"Version updated to: {version}")

    except Exception as e:
        print(f"Error updating version: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Update project version in pyproject.toml")
    parser.add_argument("version", help="New version to set (e.g., '0.1.0')")

    args = parser.parse_args()

    # Update the version
    update_version(args.version)
