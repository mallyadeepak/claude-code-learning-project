# Task Manager CLI - Project Memory

## Project Overview
A simple task management CLI application built in Python to demonstrate Claude Code concepts including skills, hooks, and project memory.

## Project Structure
- `src/` - Main application code
- `tests/` - pytest test files
- `data/` - JSON data storage
- `scripts/` - Hook scripts
- `.claude/` - Claude Code configuration

## Coding Conventions

### Python Style
- Use snake_case for functions and variables
- Use PascalCase for classes
- Maximum line length: 100 characters
- Use type hints for function parameters and return values
- Use docstrings for all public functions

### Task Data Structure
Tasks follow this schema:
```python
{
    "id": str,          # UUID string
    "title": str,       # Task title (required)
    "status": str,      # "pending", "in_progress", "completed"
    "priority": str,    # "low", "medium", "high"
    "created_at": str,  # ISO 8601 timestamp
    "completed_at": str # ISO 8601 timestamp or null
}
```

### File Patterns
- Task storage: `data/tasks.json`
- Log files: `data/edit.log` (created by hooks)
- Test files: `tests/test_*.py`

## Important Commands
- Run app: `python -m src.main <command>`
- Run tests: `pytest tests/`
- Add task: `python -m src.main add "Task title"`
- List tasks: `python -m src.main list`

## Key Patterns
1. All task operations go through `src/tasks.py`
2. Utility functions live in `src/utils.py`
3. CLI argument parsing happens in `src/main.py`
4. Data is persisted to JSON files in `data/`

## Testing Requirements
- All new features must have corresponding tests
- Run `pytest tests/ -v` before committing changes
- Maintain >80% code coverage
