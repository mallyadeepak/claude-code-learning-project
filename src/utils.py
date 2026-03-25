"""Utility functions for the task manager application."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any


def get_data_path() -> Path:
    """Get the path to the data directory."""
    return Path(__file__).parent.parent / "data"


def get_tasks_file() -> Path:
    """Get the path to the tasks JSON file."""
    return get_data_path() / "tasks.json"


def generate_id() -> str:
    """Generate a unique task ID."""
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """Get current timestamp in ISO 8601 format."""
    return datetime.now().isoformat()


def load_json(filepath: Path) -> Any:
    """Load JSON data from a file."""
    if not filepath.exists():
        return []
    with open(filepath, "r") as f:
        return json.load(f)


def save_json(filepath: Path, data: Any) -> None:
    """Save data to a JSON file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def format_task(task: dict) -> str:
    """Format a task for display."""
    status_icons = {"pending": "[ ]", "in_progress": "[~]", "completed": "[x]"}
    priority_colors = {"low": "", "medium": "*", "high": "**"}
    icon = status_icons.get(task["status"], "[ ]")
    priority = priority_colors.get(task["priority"], "")
    title = task["title"]
    if priority:
        title = f"{priority}{title}{priority}"
    return f"{icon} {task['id'][:8]}... - {title}"
