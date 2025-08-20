#!/usr/bin/env .venv/bin/python
"""Pre-commit hook for checking markdown files with Claude.

Uses Claude Code SDK to fix spelling, grammar, and markdown formatting issues.
"""

import sys
from pathlib import Path
from textwrap import dedent

from claude_code_sdk import ClaudeCodeOptions, query
from claude_code_sdk.types import AssistantMessage, ToolResultBlock, ToolUseBlock

SCRIPTS_DIR = Path(__file__).resolve().parent


async def check_markdown_file(file_path: Path) -> bool:
    """Check and fix a markdown file using Claude.

    Args:
        file_path: Path to the markdown file to check

    Returns:
        True if file was modified, False otherwise
    """
    abs_path = file_path.absolute()

    # Read the file content
    with open(abs_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Prepare the prompt with the file content
    prompt = dedent(
        f"""
Fix spelling/grammar errors and ensure proper markdown formatting in the file at {abs_path}.

Current content of the file:
```markdown
{content}
```

Make corrections directly to the file using the Edit tool.

Fix **ONLY**:
- Spelling mistakes
- Grammar errors  
- Markdown formatting issues

DO NOT change the content or meaning of the file, only fix clear errors.
Do not add explanations, just make the necessary edits.
""".strip()
    )

    # Call Claude with only Edit tool allowed for this specific file
    modified = False
    edit_requested = False

    async for message in query(
        prompt=prompt,
        options=ClaudeCodeOptions(
            cwd=SCRIPTS_DIR.parent,
            model="haiku",
            permission_mode="acceptEdits",  # Allow Edit tool to modify files.
            allowed_tools=[f"Edit({abs_path})"],
            max_turns=2,  # we should only need one turn but edit are not performed in one turn it seems.
        ),
    ):
        if isinstance(message, AssistantMessage):
            if message.content:
                for content_block in message.content:
                    if isinstance(content_block, ToolUseBlock):
                        if content_block.name == "Edit" and content_block.input.get(
                            "file_path"
                        ) == str(abs_path):
                            # Debug: print what's being changed
                            print(f"Edit requested for {abs_path}:", file=sys.stderr)
                            print(
                                f"  Old: {repr(content_block.input.get('old_string', '')[:100])}",
                                file=sys.stderr,
                            )
                            print(
                                f"  New: {repr(content_block.input.get('new_string', '')[:100])}",
                                file=sys.stderr,
                            )
                            edit_requested = True
                    elif isinstance(content_block, ToolResultBlock):
                        # Check if the edit was successful
                        if edit_requested and not content_block.is_error:
                            print(f"Edit successfully applied", file=sys.stderr)
                            modified = True
                        elif edit_requested and content_block.is_error:
                            print(
                                f"Edit failed: {content_block.content}", file=sys.stderr
                            )

    return modified


async def process_file(file_path: Path) -> tuple[Path, bool, str | None]:
    """Process a single markdown file.

    Returns:
        Tuple of (file_path, was_modified, error_message)
    """
    try:
        print(f"Checking {file_path}...", file=sys.stderr)
        modified = await check_markdown_file(file_path)
        if modified:
            print(f"File modified: {file_path}", file=sys.stderr)
        return file_path, modified, None
    except Exception as e:
        return file_path, False, str(e)


async def main() -> None:
    """Main function to process all markdown files concurrently."""
    if len(sys.argv) < 2:
        print("No files provided", file=sys.stderr)
        sys.exit(0)

    # Filter markdown files
    markdown_files = []
    for file_arg in sys.argv[1:]:
        file_path = Path(file_arg)
        if file_path.suffix == ".md":
            markdown_files.append(file_path)

    if not markdown_files:
        print("No markdown files to check", file=sys.stderr)
        sys.exit(0)

    # Process all files concurrently
    tasks = [process_file(file_path) for file_path in markdown_files]
    results = await asyncio.gather(*tasks)

    # Check results
    files_modified = False
    had_errors = False

    for file_path, modified, error in results:
        if error:
            print(f"Error processing {file_path}: {error}", file=sys.stderr)
            had_errors = True
        elif modified:
            files_modified = True

    # Exit with error if any file failed
    if had_errors:
        sys.exit(1)

    # Exit with 1 if any files were modified (for pre-commit)
    sys.exit(1 if files_modified else 0)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
