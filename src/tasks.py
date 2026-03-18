"""Task management operations - CRUD for tasks."""

from typing import Optional

from .utils import (
    generate_id,
    get_tasks_file,
    get_timestamp,
    load_json,
    save_json,
)


def get_all_tasks() -> list[dict]:
    """Get all tasks from storage."""
    return load_json(get_tasks_file())


def get_task_by_id(task_id: str) -> Optional[dict]:
    """Get a specific task by ID (supports partial ID matching)."""
    tasks = get_all_tasks()
    for task in tasks:
        if task["id"].startswith(task_id):
            return task
    return None


def add_task(title: str, priority: str = "medium") -> dict:
    """Add a new task."""
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    if priority not in ("low", "medium", "high"):
        raise ValueError("Priority must be 'low', 'medium', or 'high'")

    task = {
        "id": generate_id(),
        "title": title.strip(),
        "status": "pending",
        "priority": priority,
        "created_at": get_timestamp(),
        "completed_at": None
    }

    tasks = get_all_tasks()
    tasks.append(task)
    save_json(get_tasks_file(), tasks)

    return task


def update_task(task_id: str, **updates) -> Optional[dict]:
    """Update a task by ID."""
    tasks = get_all_tasks()

    for i, task in enumerate(tasks):
        if task["id"].startswith(task_id):
            allowed_fields = {"title", "status", "priority"}
            for key, value in updates.items():
                if key in allowed_fields:
                    tasks[i][key] = value

            if updates.get("status") == "completed":
                tasks[i]["completed_at"] = get_timestamp()

            save_json(get_tasks_file(), tasks)
            return tasks[i]

    return None


def delete_task(task_id: str) -> bool:
    """Delete a task by ID."""
    tasks = get_all_tasks()
    original_count = len(tasks)

    tasks = [t for t in tasks if not t["id"].startswith(task_id)]

    if len(tasks) < original_count:
        save_json(get_tasks_file(), tasks)
        return True

    return False


def complete_task(task_id: str) -> Optional[dict]:
    """Mark a task as completed."""
    return update_task(task_id, status="completed")


def filter_tasks(status: Optional[str] = None, priority: Optional[str] = None) -> list[dict]:
    """Filter tasks by status and/or priority."""
    tasks = get_all_tasks()

    if status:
        tasks = [t for t in tasks if t["status"] == status]

    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]

    return tasks


def get_task_stats() -> dict:
    """Get statistics about tasks."""
    tasks = get_all_tasks()

    return {
        "total": len(tasks),
        "pending": len([t for t in tasks if t["status"] == "pending"]),
        "in_progress": len([t for t in tasks if t["status"] == "in_progress"]),
        "completed": len([t for t in tasks if t["status"] == "completed"]),
        "high_priority": len([t for t in tasks if t["priority"] == "high"]),
    }
