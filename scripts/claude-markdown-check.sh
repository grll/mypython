#!/bin/bash

# Build a comma-separated list of file patterns for tool scoping
file_patterns=""
for file in "$@"; do
    # Get absolute path for each file
    abs_path=$(realpath "$file")
    if [ -z "$file_patterns" ]; then
        file_patterns="Read($abs_path),Write($abs_path),Edit($abs_path),MultiEdit($abs_path)"
    else
        file_patterns="$file_patterns,Read($abs_path),Write($abs_path),Edit($abs_path),MultiEdit($abs_path)"
    fi
done

# Run claude on the markdown files with tools scoped to only those files
$HOME/.claude/local/claude -p "Fix any spelling/grammar errors and ensure proper markdown formatting in these files. Make corrections directly without explanations." --model haiku --allowedTools "$file_patterns" "$@"

# Check if any files were modified
changed=0
for file in "$@"; do
    if ! git diff --quiet "$file"; then
        echo "File modified: $file"
        changed=1
    fi
done

# Exit with non-zero if files were changed
exit $changed