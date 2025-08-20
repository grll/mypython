#!/bin/bash

# Check if a repo name was provided
if [ -z "$1" ]; then
    echo "Usage: bash setup.sh YOUR_REPO_NAME [public|private]"
    echo "  Default visibility is public"
    exit 1
fi

REPO_NAME="$1"
VISIBILITY="${2:-public}"

# Validate visibility argument
if [ "$VISIBILITY" != "public" ] && [ "$VISIBILITY" != "private" ]; then
    echo "Error: Visibility must be 'public' or 'private'"
    exit 1
fi

# Convert repo name to valid Python package name (replace hyphens with underscores)
PACKAGE_NAME=$(echo "$REPO_NAME" | tr '-' '_')

# Create repo from template and clone it
echo "Creating $VISIBILITY repository '$REPO_NAME' from template..."
gh repo create "$REPO_NAME" --template grll/mypython --clone --$VISIBILITY
cd "$REPO_NAME" || exit 1

echo "Setting up template:"
echo "  Repository: $REPO_NAME"
echo "  Package: $PACKAGE_NAME"

# Rename the package directory
if [ -d "src/mypython" ]; then
    mv src/mypython "src/$PACKAGE_NAME"
    echo "✓ Renamed package directory to src/$PACKAGE_NAME"
fi

# Update all references in Python, TOML, YAML, and Markdown files
find . -type f \( -name "*.py" -o -name "*.toml" -o -name "*.yml" -o -name "*.md" \) \
    -not -path "./.git/*" \
    -exec sed -i.bak "s/mypython/$PACKAGE_NAME/g" {} \;

# Clean up backup files
find . -name "*.bak" -type f -delete

echo "✓ Updated all file references"

# Delete the setup script and commit the changes
rm -f setup.sh
git add -A
git commit -m "Initial setup: Rename package to $PACKAGE_NAME"
echo "✓ Removed setup script and committed changes"

echo "✓ Setup complete! Your package '$PACKAGE_NAME' is ready."
echo ""
echo "Next steps:"
echo "  cd $REPO_NAME"
echo "  uv sync --extra dev"
echo "  uv run pre-commit install"