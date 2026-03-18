# List Tasks Skill

Display all tasks in the task manager with optional filtering.

## Arguments
- `$ARGUMENTS` - Optional filter: "pending", "completed", "all" (default: all)

## Instructions

1. Check if a filter was provided in `$ARGUMENTS`
2. Run the appropriate command:
   - No filter or "all": `python -m src.main list`
   - "pending": `python -m src.main list --status pending`
   - "completed": `python -m src.main list --status completed`
3. Display the results in a formatted way
4. If no tasks exist, inform the user they can add tasks with `/add-task`

## Example Usage
```
/list-tasks
/list-tasks pending
/list-tasks completed
```
