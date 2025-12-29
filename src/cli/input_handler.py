"""User input handling and validation functions."""

import sys
from typing import Optional

from src.errors import InvalidIdError


def get_menu_choice() -> int:
    """Get and validate main menu choice from user.

    Returns:
        Integer between 1 and 7 representing the menu choice.

    Keeps prompting until valid input is received.
    """
    while True:
        try:
            choice = input("Enter your choice (1-7): ").strip()
            if not choice:
                print("Please enter a number between 1 and 7.")
                continue

            choice_int = int(choice)
            if 1 <= choice_int <= 7:
                return choice_int
            else:
                print("Please enter a number between 1 and 7.")
        except ValueError:
            print("Please enter a valid number.")


def get_task_id() -> int:
    """Get and validate a task ID from user.

    Returns:
        Positive integer representing the task ID.

    Keeps prompting until valid input is received.
    """
    while True:
        try:
            task_id_str = input("Enter task ID: ").strip()
            if not task_id_str:
                print("Please enter a task ID.")
                continue

            task_id = int(task_id_str)
            if task_id > 0:
                return task_id
            else:
                print("Task ID must be a positive integer.")
        except ValueError:
            print("Please enter a valid number.")


def get_task_title() -> str:
    """Get and validate a task title from user.

    Returns:
        Non-empty string (1-200 characters) representing the task title.

    Keeps prompting until valid input is received.
    """
    while True:
        title = input("Enter task title: ").strip()
        if not title:
            print("Task title cannot be empty. Please try again.")
            continue

        if len(title) > 200:
            print(f"Task title is {len(title)} characters. Maximum is 200. Please shorten it.")
            continue

        return title


def get_task_description() -> str:
    """Get an optional task description from user.

    Returns:
        String representing the task description (may be empty).

    User can press Enter to skip (no description).
    """
    description = input("Enter task description (optional, press Enter to skip): ").strip()
    return description


def confirm_delete() -> bool:
    """Get delete confirmation from user.

    Returns:
        True if user confirms with 'y' or 'yes' (case-insensitive).
        False otherwise.
    """
    while True:
        confirmation = input("Are you sure you want to delete this task? (y/n): ").strip().lower()
        if confirmation in ('y', 'yes'):
            return True
        elif confirmation in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def get_optional_input(prompt: str) -> str:
    """Get optional input from user (press Enter to skip).

    Args:
        prompt: The prompt to display.

    Returns:
        The input string, which may be empty.
    """
    return input(prompt).strip()


def handle_keyboard_interrupt() -> None:
    """Handle Ctrl+C gracefully with a goodbye message."""
    print("\n\nThank you for using Todo CLI. Goodbye!")
    sys.exit(0)
