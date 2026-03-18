#!/bin/bash
# Hook script: Logs file edits to data/edit.log
# This script is called by the PostToolUse hook when files are edited

FILE_PATHS="$1"
LOG_FILE="$(dirname "$0")/../data/edit.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Log the edit
echo "[$TIMESTAMP] Edited: $FILE_PATHS" >> "$LOG_FILE"
