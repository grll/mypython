# My Python - Template

## How to use this template?

### Quick Start

Run this one-liner to create a new Python project from this template:

```bash
# Create a public repository (default)
curl -s https://raw.githubusercontent.com/grll/mypython/main/setup.sh | bash -s YOUR_REPO_NAME

# Create a private repository
curl -s https://raw.githubusercontent.com/grll/mypython/main/setup.sh | bash -s YOUR_REPO_NAME private
```

This will:
1. Create a new GitHub repository from this template (public by default, or private if specified)
2. Clone it locally
3. Rename the package from `mypython` to your repository name (converting hyphens to underscores for Python compatibility)
4. Update all references throughout the codebase

For example, if you run `bash -s my-awesome-project`, it will create a public repo called `my-awesome-project` with a Python package named `my_awesome_project`.

## Installation

## Development

Install dev dependencies:

```bash
uv sync --extra dev
```

The dev dependencies include linting, type checking, and testing.

Install pre-commit hooks:

```bash
uv run pre-commit install
```

Run tests:

```bash
uv run pytest
```

## Project Maintenance

**Note:** Make sure you are on the main branch and your git status is clean before doing the following.

You can create a new GitHub release while bumping the version of your package via the bump_version script:

```bash
./scripts/bump_version.py
```