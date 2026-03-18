#!/bin/bash
# Hook script: Logs file edits to data/edit.log
# This script is called by the PostToolUse hook when files are edited
# Claude Code passes JSON input via stdin

LOG_FILE="$(dirname "$0")/../data/edit.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Read JSON input from stdin and extract file path using jq
read -r hook_input
FILE_PATH=$(echo "$hook_input" | jq -r '.tool_input.file_path // empty')

# Log the edit if we got a file path
if [ -n "$FILE_PATH" ]; then
    echo "[$TIMESTAMP] Edited: $FILE_PATH" >> "$LOG_FILE"
fi
