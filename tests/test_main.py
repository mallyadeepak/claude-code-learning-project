"""Tests for the CLI entry point (src/main.py)."""

import argparse
from unittest import mock

import pytest

from src import main as cli
from src import tasks


@pytest.fixture
def temp_tasks_file(tmp_path):
    """Temporary tasks file shared across all CLI tests."""
    tasks_file = tmp_path / "tasks.json"
    tasks_file.write_text("[]")
    with mock.patch("src.tasks.get_tasks_file", return_value=tasks_file):
        yield tasks_file


class TestCmdAdd:
    """Tests for cmd_add."""

    def test_add_success(self, temp_tasks_file, capsys):
        """Successful add prints confirmation and returns 0."""
        args = argparse.Namespace(title="Buy milk", priority="medium")
        result = cli.cmd_add(args)
        assert result == 0
        assert "Added task" in capsys.readouterr().out

    def test_add_high_priority(self, temp_tasks_file, capsys):
        """Add with high priority succeeds."""
        args = argparse.Namespace(title="Urgent task", priority="high")
        result = cli.cmd_add(args)
        assert result == 0

    def test_add_empty_title_returns_1(self, temp_tasks_file, capsys):
        """Empty title prints error to stderr and returns 1."""
        args = argparse.Namespace(title="", priority="medium")
        result = cli.cmd_add(args)
        assert result == 1
        assert "Error" in capsys.readouterr().err


class TestCmdList:
    """Tests for cmd_list."""

    def test_list_empty(self, temp_tasks_file, capsys):
        """Lists 'No tasks found' when there are no tasks."""
        args = argparse.Namespace(status=None, priority=None)
        result = cli.cmd_list(args)
        assert result == 0
        assert "No tasks found" in capsys.readouterr().out

    def test_list_with_tasks(self, temp_tasks_file, capsys):
        """Lists tasks when they exist."""
        tasks.add_task("Task A")
        tasks.add_task("Task B")
        args = argparse.Namespace(status=None, priority=None)
        result = cli.cmd_list(args)
        assert result == 0
        out = capsys.readouterr().out
        assert "Tasks (2)" in out

    def test_list_filtered_by_status(self, temp_tasks_file, capsys):
        """Filters tasks by status."""
        tasks.add_task("Pending task")
        task = tasks.add_task("Done task")
        tasks.complete_task(task["id"][:8])
        args = argparse.Namespace(status="pending", priority=None)
        result = cli.cmd_list(args)
        assert result == 0
        out = capsys.readouterr().out
        assert "Tasks (1)" in out

    def test_list_filtered_by_priority(self, temp_tasks_file, capsys):
        """Filters tasks by priority."""
        tasks.add_task("Normal task", priority="medium")
        tasks.add_task("High task", priority="high")
        args = argparse.Namespace(status=None, priority="high")
        result = cli.cmd_list(args)
        assert result == 0
        assert "Tasks (1)" in capsys.readouterr().out


class TestCmdComplete:
    """Tests for cmd_complete."""

    def test_complete_success(self, temp_tasks_file, capsys):
        """Completing an existing task returns 0."""
        task = tasks.add_task("Finish report")
        args = argparse.Namespace(task_id=task["id"][:8])
        result = cli.cmd_complete(args)
        assert result == 0
        assert "Completed" in capsys.readouterr().out

    def test_complete_not_found(self, temp_tasks_file, capsys):
        """Completing a missing task prints to stderr and returns 1."""
        args = argparse.Namespace(task_id="nonexistent")
        result = cli.cmd_complete(args)
        assert result == 1
        assert "not found" in capsys.readouterr().err


class TestCmdDelete:
    """Tests for cmd_delete."""

    def test_delete_success(self, temp_tasks_file, capsys):
        """Deleting an existing task returns 0."""
        task = tasks.add_task("Obsolete task")
        args = argparse.Namespace(task_id=task["id"][:8])
        result = cli.cmd_delete(args)
        assert result == 0
        assert "Deleted" in capsys.readouterr().out

    def test_delete_not_found(self, temp_tasks_file, capsys):
        """Deleting a missing task prints to stderr and returns 1."""
        args = argparse.Namespace(task_id="nonexistent")
        result = cli.cmd_delete(args)
        assert result == 1
        assert "not found" in capsys.readouterr().err


class TestCmdStats:
    """Tests for cmd_stats."""

    def test_stats_output(self, temp_tasks_file, capsys):
        """Stats command prints summary and returns 0."""
        tasks.add_task("Task 1")
        tasks.add_task("Task 2", priority="high")
        result = cli.cmd_stats(argparse.Namespace())
        assert result == 0
        out = capsys.readouterr().out
        assert "Total" in out
        assert "Pending" in out
        assert "High Priority" in out


class TestMain:
    """Tests for the main() entry point."""

    def test_no_command_prints_help(self, temp_tasks_file, capsys):
        """Calling main with no subcommand prints help and returns 0."""
        with mock.patch("sys.argv", ["task"]):
            result = cli.main()
        assert result == 0

    def test_main_add_command(self, temp_tasks_file, capsys):
        """main() routes 'add' subcommand correctly."""
        with mock.patch("sys.argv", ["task", "add", "My task"]):
            result = cli.main()
        assert result == 0
        assert "Added task" in capsys.readouterr().out

    def test_main_list_command(self, temp_tasks_file, capsys):
        """main() routes 'list' subcommand correctly."""
        with mock.patch("sys.argv", ["task", "list"]):
            result = cli.main()
        assert result == 0

    def test_main_stats_command(self, temp_tasks_file, capsys):
        """main() routes 'stats' subcommand correctly."""
        with mock.patch("sys.argv", ["task", "stats"]):
            result = cli.main()
        assert result == 0
        assert "Total" in capsys.readouterr().out
