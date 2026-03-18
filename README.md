# Task Manager CLI - Claude Code Learning Project

A simple task management CLI application built in Python that demonstrates key Claude Code concepts through practical examples.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the CLI
python -m src.main --help

# Add a task
python -m src.main add "My first task"

# List all tasks
python -m src.main list

# Run tests
pytest tests/ -v
```

## Project Structure

```
claude-code-learning-project/
├── CLAUDE.md                    # Project memory/context
├── .claude/
│   ├── settings.json           # Claude Code settings (hooks, permissions)
│   └── commands/               # Custom skills (slash commands)
│       ├── add-task.md         # /add-task skill
│       ├── list-tasks.md       # /list-tasks skill
│       ├── summarize.md        # /summarize skill
│       └── test.md             # /test skill
├── src/
│   ├── __init__.py             # Package init
│   ├── main.py                 # CLI entry point
│   ├── tasks.py                # Task management logic
│   └── utils.py                # Utility functions
├── tests/
│   └── test_tasks.py           # Unit tests (pytest)
├── data/
│   └── tasks.json              # Task storage
├── scripts/
│   └── log-edit.sh             # Hook: logs file edits
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## Claude Code Concepts Demonstrated

### 1. Skills (Slash Commands)

Skills are custom commands defined in `.claude/commands/` that extend Claude Code's capabilities. Each skill is a markdown file that provides instructions for Claude.

**Available Skills:**

| Skill | File | Description |
|-------|------|-------------|
| `/add-task` | `add-task.md` | Add a new task with validation |
| `/list-tasks` | `list-tasks.md` | List tasks with optional filtering |
| `/summarize` | `summarize.md` | Summarize the codebase state |
| `/test` | `test.md` | Run tests and report results |

**Example Skill Definition** (`add-task.md`):
```markdown
# Add Task Skill

Add a new task to the task manager.

## Arguments
- `$ARGUMENTS` - The task title to add

## Instructions
1. Validate that a task title was provided
2. Run: `python -m src.main add "$ARGUMENTS"`
3. Show the updated task list
```

**Usage:**
```
> /add-task Buy groceries
> /list-tasks pending
> /test
```

---

### 2. Hooks

Hooks are event-driven shell commands that execute at specific points during Claude Code's operation. They're defined in `.claude/settings.json`.

**Configured Hooks:**

| Hook Type | Trigger | Action |
|-----------|---------|--------|
| `PreToolUse` | Before Bash commands | Logs command info to stderr |
| `PostToolUse` | After file edits | Logs changes to `data/edit.log` |

**Hook Configuration** (`.claude/settings.json`):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[Hook] About to run Bash command\" >&2"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/log-edit.sh \"$CLAUDE_FILE_PATHS\""
          }
        ]
      }
    ]
  }
}
```

**Hook Script** (`scripts/log-edit.sh`):
```bash
#!/bin/bash
FILE_PATHS="$1"
LOG_FILE="data/edit.log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
echo "[$TIMESTAMP] Edited: $FILE_PATHS" >> "$LOG_FILE"
```

---

### 3. CLAUDE.md (Project Memory)

The `CLAUDE.md` file serves as persistent project memory that Claude reads at the start of each session. It contains:

- Project overview and purpose
- Coding conventions and style guides
- Data structures and schemas
- Important commands
- Key patterns to follow

**Why It Matters:**
- Ensures consistency across sessions
- Reduces need to re-explain project context
- Enforces coding standards automatically

---

### 4. Settings Configuration

The `.claude/settings.json` file configures Claude Code's behavior for this project:

```json
{
  "hooks": { /* ... */ },
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(python:*)",
      "Read",
      "Edit",
      "Write"
    ],
    "deny": []
  }
}
```

**Permission Patterns:**
- `Bash(pytest:*)` - Allow running pytest commands
- `Bash(python:*)` - Allow running Python commands
- `Read`, `Edit`, `Write` - Allow file operations

---

### 5. Subagents

Claude Code uses specialized subagents for different tasks. Here's when each is used:

#### Explore Agent
Used for navigating and understanding the codebase.

**Example Prompt:** "Where is task validation handled?"

**Claude's Action:** Launches Explore agent to search through files and find validation logic in `src/tasks.py`.

#### Plan Agent
Used for designing implementation strategies.

**Example Prompt:** "Add a feature to export tasks to CSV"

**Claude's Action:** Launches Plan agent to:
1. Analyze existing code structure
2. Identify integration points
3. Design implementation approach
4. Present plan for approval

#### Bash Agent
Used for executing shell commands.

**Example Prompt:** "Run the test suite"

**Claude's Action:** Launches Bash agent to execute `pytest tests/ -v`.

---

## CLI Commands

```bash
# Add a task
python -m src.main add "Task title"
python -m src.main add "Urgent task" -p high

# List tasks
python -m src.main list
python -m src.main list --status pending
python -m src.main list --priority high

# Complete a task
python -m src.main complete <task-id>

# Delete a task
python -m src.main delete <task-id>

# View statistics
python -m src.main stats
```

---

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_tasks.py::TestTasks::test_add_task -v

# Run with coverage
pytest tests/ -v --cov=src
```

---

## Task Data Format

Tasks are stored in `data/tasks.json`:

```json
{
  "id": "uuid-string",
  "title": "Task title",
  "status": "pending|in_progress|completed",
  "priority": "low|medium|high",
  "created_at": "2024-01-15T10:00:00",
  "completed_at": null
}
```

---

## Learning Exercises

Try these to explore Claude Code features:

1. **Skills**: Run `/add-task Learn Claude Code` and observe how the skill works
2. **Hooks**: Edit a file and check `data/edit.log` to see the hook in action
3. **Project Memory**: Ask Claude about coding conventions - it will reference CLAUDE.md
4. **Subagents**: Ask "What files handle task filtering?" to see the Explore agent

---

## License

MIT
