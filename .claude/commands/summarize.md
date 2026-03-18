# Summarize Skill

Provide a summary of the codebase structure and current state.

## Instructions

1. Read the CLAUDE.md file to understand project context
2. List all Python files in the src/ directory
3. Count the number of tasks in data/tasks.json
4. Run tests to check project health: `pytest tests/ -v --tb=short`
5. Provide a summary including:
   - Project purpose
   - Number of source files
   - Number of tasks stored
   - Test status (passing/failing)
   - Any recommendations for improvements

## Example Output
```
## Project Summary

**Purpose:** Task management CLI application

**Source Files:** 4 files in src/
- main.py - CLI entry point
- tasks.py - Task operations
- utils.py - Utilities
- __init__.py - Package init

**Data:** 3 tasks stored (2 pending, 1 completed)

**Tests:** All 5 tests passing

**Health:** Good - no issues detected
```
