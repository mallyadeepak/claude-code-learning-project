# Add Task Skill

Add a new task to the task manager.

## Arguments
- `$ARGUMENTS` - The task title to add

## Instructions

1. Validate that a task title was provided in `$ARGUMENTS`
2. If no title provided, ask the user for one
3. Run the command: `python -m src.main add "$ARGUMENTS"`
4. Confirm the task was added successfully
5. Show the updated task list by running: `python -m src.main list`

## Example Usage
```
/add-task Buy groceries
/add-task "Complete project documentation"
```
