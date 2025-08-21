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

The dev dependencies includes linting, type checking and testing.

Install pre-commit hooks:

```bash
uv run pre-commit install
```

Run tests:

```bash
uv run pytest
```

## Project Maintenance

### Version Management

This project includes a `bump_version.py` script to automate version bumping and release creation. The script:
- Updates the version in `src/mypython/__init__.py`
- Creates a git commit with the version change
- Tags the commit with the new version
- Pushes the changes and tags to GitHub
- Creates a GitHub release with auto-generated release notes

#### Usage

```bash
# Bump patch version (e.g., 1.0.0 -> 1.0.1)
python scripts/bump_version.py patch

# Bump minor version (e.g., 1.0.0 -> 1.1.0)
python scripts/bump_version.py minor

# Bump major version (e.g., 1.0.0 -> 2.0.0)
python scripts/bump_version.py major
```

### PyPI Publishing Setup

This template includes a GitHub Actions workflow for automatic PyPI publishing when releases are created. To enable this, you need to configure PyPI Trusted Publisher:

#### Steps to Configure PyPI Trusted Publisher

1. **Create your package on PyPI** (if not already exists):
   - Go to [PyPI](https://pypi.org)
   - Upload an initial version manually or create a placeholder

2. **Configure Trusted Publisher on PyPI**:
   - Go to your project page on PyPI
   - Navigate to "Settings" → "Publishing"
   - Under "Trusted Publishers", click "Add a new publisher"
   - Fill in the following details:
     - **Owner**: Your GitHub username or organization
     - **Repository name**: Your repository name
     - **Workflow name**: `release.yml`
     - **Environment**: Leave blank (optional)
   - Click "Add"

3. **Verify the GitHub Actions workflow**:
   - The `.github/workflows/release.yml` file is already configured in this template
   - It will automatically trigger when you create a new release (using `bump_version.py` or manually)
   - The workflow will build and publish your package to PyPI using trusted publishing (no API tokens needed!)

Once configured, your release process becomes:
1. Run `python scripts/bump_version.py [major|minor|patch]` to create a release
2. GitHub Actions automatically publishes to PyPI using trusted publishing

