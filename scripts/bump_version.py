#!/usr/bin/env python
"""Script to bump version and create releases."""

import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn


def run_command(command: str) -> None:
    """Execute a shell command and exit on failure.

    Args:
        command: The command to execute.
    """
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error: {e}")
        sys.exit(1)


def bump_version(version_type: str) -> NoReturn:
    """Bump the version and create a release.

    Args:
        version_type: The type of version bump (major, minor, or patch).
    """
    init_file = Path("src/mypython/__init__.py")

    # Read current version
    content = init_file.read_text()
    version_match = re.search(r'__version__ = ["\']([^"\']+)["\']', content)
    if not version_match:
        print("Could not find version in __init__.py")
        sys.exit(1)
    current_version = version_match.group(1)
    major, minor, patch = map(int, current_version.split("."))

    # Update version based on argument
    if version_type == "major":
        new_version = f"{major + 1}.0.0"
    elif version_type == "minor":
        new_version = f"{major}.{minor + 1}.0"
    elif version_type == "patch":
        new_version = f"{major}.{minor}.{patch + 1}"
    else:
        print("Invalid version type. Use 'major', 'minor', or 'patch'")
        sys.exit(1)

    # Update __init__.py
    new_content = re.sub(
        r'__version__ = ["\']([^"\']+)["\']', f'__version__ = "{new_version}"', content
    )
    init_file.write_text(new_content)

    # Git operations
    run_command("git add src/mypython/__init__.py")
    run_command(f'git commit -m "release {new_version}: version bump commit"')
    run_command("git push")
    run_command(f"git tag v{new_version}")
    run_command("git push --tags")

    # Create GitHub release using gh CLI
    run_command(
        f'gh release create v{new_version} --title "Release {new_version}" --generate-notes'
    )

    print(f"Version bumped from {current_version} to {new_version}")
    print(f"Git operations completed and GitHub release v{new_version} created")
    sys.exit(0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <major|minor|patch>")
        sys.exit(1)

    bump_version(sys.argv[1])
