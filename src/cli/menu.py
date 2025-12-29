"""Menu display and user interface functions."""

import os
from datetime import datetime
from typing import List, Optional

from src.models.task import Task


def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform manner."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_welcome() -> None:
    """Display the welcome message on application startup."""
    print("=" * 50)
    print("       Welcome to Todo CLI")
    print("       Your Simple Task Manager")
    print("=" * 50)
    print()


def display_main_menu() -> None:
    """Display the main menu options."""
    print("-" * 30)
    print("       Main Menu")
    print("-" * 30)
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete")
    print("6. Mark Incomplete")
    print("7. Exit")
    print("-" * 30)


def display_tasks(tasks: List[Task]) -> None:
    """Display all tasks in a formatted list.

    Args:
        tasks: List of Task objects to display.
    """
    if not tasks:
        display_empty_list_message()
        return

    print("\n" + "=" * 60)
    print("                    Your Tasks")
    print("=" * 60)

    for task in tasks:
        status = "[X]" if task.status else "[ ]"
        print(f"  {task.id:3}. {status} {task.title}")

        if task.description:
            desc_lines = wrap_text(task.description, 50)
            for line in desc_lines:
                print(f"      {line}")

    print("=" * 60)
    print()


def wrap_text(text: str, width: int) -> List[str]:
    """Wrap text to specified width.

    Args:
        text: The text to wrap.
        width: Maximum line width.

    Returns:
        List of wrapped lines.
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + len(word) + 1 <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines if lines else [""]


def display_task_details(task: Task) -> None:
    """Display detailed information about a single task.

    Args:
        task: The Task object to display.
    """
    status = "Complete" if task.status else "Incomplete"

    print(f"\nTask Details:")
    print(f"  ID:          {task.id}")
    print(f"  Title:       {task.title}")
    if task.description:
        print(f"  Description: {task.description}")
    print(f"  Status:      {status}")
    print(f"  Created:     {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


def display_error(message: str) -> None:
    """Display an error message to the user.

    Args:
        message: The error message to display.
    """
    print(f"\n  ERROR: {message}")
    print()


def display_success(message: str) -> None:
    """Display a success message to the user.

    Args:
        message: The success message to display.
    """
    print(f"\n  SUCCESS: {message}")
    print()


def display_empty_list_message() -> None:
    """Display message when task list is empty."""
    print("\n" + " " * 15 + "-" * 30)
    print(" " * 20 + "No tasks yet")
    print(" " * 10 + "Add a task to get started!")
    print(" " * 15 + "-" * 30 + "\n")


def display_task_added(task: Task) -> None:
    """Display confirmation when a task is added.

    Args:
        task: The newly created Task.
    """
    display_success(f"Task '{task.title}' added with ID {task.id}")


def display_task_updated(task: Task) -> None:
    """Display confirmation when a task is updated.

    Args:
        task: The updated Task.
    """
    display_success(f"Task {task.id} updated")


def display_task_deleted(task_id: int) -> None:
    """Display confirmation when a task is deleted.

    Args:
        task_id: The ID of the deleted task.
    """
    display_success(f"Task {task_id} deleted")


def display_task_marked_complete(task_id: int) -> None:
    """Display confirmation when a task is marked complete.

    Args:
        task_id: The ID of the marked task.
    """
    display_success(f"Task {task_id} marked as complete")


def display_task_marked_incomplete(task_id: int) -> None:
    """Display confirmation when a task is marked incomplete.

    Args:
        task_id: The ID of the marked task.
    """
    display_success(f"Task {task_id} marked as incomplete")


def display_already_complete(task_id: int) -> None:
    """Display message when task is already complete.

    Args:
        task_id: The ID of the task.
    """
    print(f"\n  Task {task_id} is already complete.")


def display_already_incomplete(task_id: int) -> None:
    """Display message when task is already incomplete.

    Args:
        task_id: The ID of the task.
    """
    print(f"\n  Task {task_id} is already incomplete.")


def display_goodbye() -> None:
    """Display goodbye message on exit."""
    print("\n" + "=" * 40)
    print("       Thank you for using Todo CLI!")
    print("       Have a great day!")
    print("=" * 40)


def display_prompt(prompt: str) -> None:
    """Display a prompt message.

    Args:
        prompt: The prompt text.
    """
    print(f"\n  {prompt}")


def display_info(message: str) -> None:
    """Display an informational message.

    Args:
        message: The message to display.
    """
    print(f"  {message}")


def pause_for_user() -> None:
    """Pause to let user read the output."""
    input("\n  Press Enter to continue...")
