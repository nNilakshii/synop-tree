#!/usr/bin/env bash
# PostToolUse hook (P0.2.5): ruff-format a Python file after Claude edits or writes it.
# Input: hook JSON on stdin. Never fails the tool call.
file=$(jq -r ".tool_input.file_path // empty")
case "$file" in
  *.py | *.pyi)
    cd "${CLAUDE_PROJECT_DIR:-.}" && uv run --quiet ruff format --quiet "$file" >&2
    ;;
esac
exit 0
