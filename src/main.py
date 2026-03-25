"""Main CLI entry point for the task manager."""

import argparse
import sys

from . import tasks
from .utils import format_task


def cmd_add(args: argparse.Namespace) -> int:
    """Handle the add command."""
    try:
        task = tasks.add_task(args.title, args.priority)
        print(f"Added task: {task['id'][:8]}... - {task['title']}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def cmd_list(args: argparse.Namespace) -> int:
    """Handle the list command."""
    filtered_tasks = tasks.filter_tasks(status=args.status, priority=args.priority)

    if not filtered_tasks:
        print("No tasks found.")
        return 0

    print(f"Tasks ({len(filtered_tasks)}):")
    print("-" * 40)
    for task in filtered_tasks:
        print(format_task(task))

    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    """Handle the complete command."""
    task = tasks.complete_task(args.task_id)
    if task:
        print(f"Completed: {task['title']}")
        return 0
    else:
        print(f"Task not found: {args.task_id}", file=sys.stderr)
        return 1


def cmd_delete(args: argparse.Namespace) -> int:
    """Handle the delete command."""
    if tasks.delete_task(args.task_id):
        print(f"Deleted task: {args.task_id}")
        return 0
    else:
        print(f"Task not found: {args.task_id}", file=sys.stderr)
        return 1


def cmd_stats(args: argparse.Namespace) -> int:
    """Handle the stats command."""
    stats = tasks.get_task_stats()
    print("Task Statistics:")
    print("-" * 20)
    print(f"Total:       {stats['total']}")
    print(f"Pending:     {stats['pending']}")
    print(f"In Progress: {stats['in_progress']}")
    print(f"Completed:   {stats['completed']}")
    print(f"High Priority: {stats['high_priority']}")
    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Task Manager CLI - Manage your tasks from the command line"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "-p",
        "--priority",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority (default: medium)",
    )
    add_parser.set_defaults(func=cmd_add)

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "-s", "--status", choices=["pending", "in_progress", "completed"], help="Filter by status"
    )
    list_parser.add_argument(
        "-p", "--priority", choices=["low", "medium", "high"], help="Filter by priority"
    )
    list_parser.set_defaults(func=cmd_list)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as completed")
    complete_parser.add_argument("task_id", help="Task ID (or partial ID)")
    complete_parser.set_defaults(func=cmd_complete)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID (or partial ID)")
    delete_parser.set_defaults(func=cmd_delete)

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show task statistics")
    stats_parser.set_defaults(func=cmd_stats)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
