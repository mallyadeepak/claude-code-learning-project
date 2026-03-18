"""Tests for the task manager."""

import json
import tempfile
from pathlib import Path
from unittest import mock

import pytest

from src import tasks
from src.utils import generate_id, get_timestamp, format_task


class TestUtils:
    """Tests for utility functions."""

    def test_generate_id_returns_string(self):
        """Test that generate_id returns a string."""
        task_id = generate_id()
        assert isinstance(task_id, str)
        assert len(task_id) == 36  # UUID format

    def test_generate_id_unique(self):
        """Test that generate_id returns unique IDs."""
        ids = [generate_id() for _ in range(100)]
        assert len(set(ids)) == 100

    def test_get_timestamp_format(self):
        """Test that get_timestamp returns ISO format."""
        timestamp = get_timestamp()
        assert "T" in timestamp  # ISO 8601 format contains T

    def test_format_task_pending(self):
        """Test formatting a pending task."""
        task = {
            "id": "12345678-1234-1234-1234-123456789012",
            "title": "Test task",
            "status": "pending",
            "priority": "medium"
        }
        formatted = format_task(task)
        assert "[ ]" in formatted
        assert "Test task" in formatted

    def test_format_task_completed(self):
        """Test formatting a completed task."""
        task = {
            "id": "12345678-1234-1234-1234-123456789012",
            "title": "Done task",
            "status": "completed",
            "priority": "low"
        }
        formatted = format_task(task)
        assert "[x]" in formatted


class TestTasks:
    """Tests for task operations."""

    @pytest.fixture
    def temp_tasks_file(self, tmp_path):
        """Create a temporary tasks file for testing."""
        tasks_file = tmp_path / "tasks.json"
        tasks_file.write_text("[]")
        # Patch where the function is used (in tasks module), not where it's defined
        with mock.patch("src.tasks.get_tasks_file", return_value=tasks_file):
            yield tasks_file

    def test_add_task(self, temp_tasks_file):
        """Test adding a task."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            task = tasks.add_task("Test task")

            assert task["title"] == "Test task"
            assert task["status"] == "pending"
            assert task["priority"] == "medium"
            assert task["id"] is not None

    def test_add_task_with_priority(self, temp_tasks_file):
        """Test adding a task with custom priority."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            task = tasks.add_task("High priority task", priority="high")

            assert task["priority"] == "high"

    def test_add_task_empty_title_raises(self, temp_tasks_file):
        """Test that adding a task with empty title raises error."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            with pytest.raises(ValueError, match="cannot be empty"):
                tasks.add_task("")

    def test_add_task_invalid_priority_raises(self, temp_tasks_file):
        """Test that invalid priority raises error."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            with pytest.raises(ValueError, match="Priority must be"):
                tasks.add_task("Task", priority="invalid")

    def test_get_all_tasks(self, temp_tasks_file):
        """Test getting all tasks."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            tasks.add_task("Task 1")
            tasks.add_task("Task 2")

            all_tasks = tasks.get_all_tasks()
            assert len(all_tasks) == 2

    def test_complete_task(self, temp_tasks_file):
        """Test completing a task."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            task = tasks.add_task("Task to complete")
            task_id = task["id"]

            completed = tasks.complete_task(task_id[:8])
            assert completed["status"] == "completed"
            assert completed["completed_at"] is not None

    def test_delete_task(self, temp_tasks_file):
        """Test deleting a task."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            task = tasks.add_task("Task to delete")
            task_id = task["id"]

            assert tasks.delete_task(task_id[:8]) is True
            assert len(tasks.get_all_tasks()) == 0

    def test_filter_tasks_by_status(self, temp_tasks_file):
        """Test filtering tasks by status."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            task1 = tasks.add_task("Pending task")
            task2 = tasks.add_task("Another task")
            tasks.complete_task(task2["id"][:8])

            pending = tasks.filter_tasks(status="pending")
            assert len(pending) == 1
            assert pending[0]["title"] == "Pending task"

    def test_get_task_stats(self, temp_tasks_file):
        """Test getting task statistics."""
        with mock.patch("src.tasks.get_tasks_file", return_value=temp_tasks_file):
            tasks.add_task("Task 1")
            tasks.add_task("Task 2", priority="high")
            task3 = tasks.add_task("Task 3")
            tasks.complete_task(task3["id"][:8])

            stats = tasks.get_task_stats()
            assert stats["total"] == 3
            assert stats["pending"] == 2
            assert stats["completed"] == 1
            assert stats["high_priority"] == 1
