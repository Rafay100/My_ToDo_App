#!/usr/bin/env python3
"""Main application entry point for Todo CLI.

This module implements the main menu loop and dispatches
user actions to the appropriate handlers.
"""

import sys

from src.cli.input_handler import (
    confirm_delete,
    get_menu_choice,
    get_task_description,
    get_task_id,
    get_task_title,
    handle_keyboard_interrupt,
)
from src.cli.menu import (
    clear_screen,
    display_already_complete,
    display_already_incomplete,
    display_error,
    display_goodbye,
    display_main_menu,
    display_success,
    display_task_added,
    display_task_deleted,
    display_task_marked_complete,
    display_task_marked_incomplete,
    display_task_updated,
    display_tasks,
    display_welcome,
    pause_for_user,
)
from src.services.task_store import TaskStore


def main() -> None:
    """Run the Todo CLI application.

    Initializes the TaskStore and enters the main menu loop.
    Handles all user interactions and dispatches to appropriate
    service layer operations.
    """
    store = TaskStore()

    try:
        clear_screen()
        display_welcome()

        while True:
            display_main_menu()

            try:
                choice = get_menu_choice()
            except KeyboardInterrupt:
                display_goodbye()
                sys.exit(0)

            clear_screen()

            try:
                if choice == 1:
                    handle_add_task(store)
                elif choice == 2:
                    handle_view_tasks(store)
                elif choice == 3:
                    handle_update_task(store)
                elif choice == 4:
                    handle_delete_task(store)
                elif choice == 5:
                    handle_mark_complete(store)
                elif choice == 6:
                    handle_mark_incomplete(store)
                elif choice == 7:
                    display_goodbye()
                    sys.exit(0)

                # Pause before showing menu again (except for view which pauses)
                if choice != 2:
                    pause_for_user()
                    clear_screen()

            except KeyboardInterrupt:
                display_goodbye()
                sys.exit(0)
            except Exception as e:
                display_error(str(e))
                pause_for_user()
                clear_screen()

    except KeyboardInterrupt:
        display_goodbye()
        sys.exit(0)


def handle_add_task(store: TaskStore) -> None:
    """Handle adding a new task.

    Args:
        store: The TaskStore instance.
    """
    print("\n--- Add New Task ---")
    title = get_task_title()
    description = get_task_description()
    task = store.add_task(title, description)
    display_task_added(task)


def handle_view_tasks(store: TaskStore) -> None:
    """Handle viewing all tasks.

    Args:
        store: The TaskStore instance.
    """
    tasks = store.get_all_tasks()
    display_tasks(tasks)


def handle_update_task(store: TaskStore) -> None:
    """Handle updating a task's title.

    Args:
        store: The TaskStore instance.
    """
    print("\n--- Update Task ---")
    tasks = store.get_all_tasks()

    if not tasks:
        display_error("No tasks available to update.")
        return

    display_tasks(tasks)
    task_id = get_task_id()

    print(f"\nEnter new title for task {task_id}:")
    new_title = get_task_title()

    updated_task = store.update_task(task_id, new_title)
    display_task_updated(updated_task)


def handle_delete_task(store: TaskStore) -> None:
    """Handle deleting a task.

    Args:
        store: The TaskStore instance.
    """
    print("\n--- Delete Task ---")
    tasks = store.get_all_tasks()

    if not tasks:
        display_error("No tasks available to delete.")
        return

    display_tasks(tasks)
    task_id = get_task_id()

    if confirm_delete():
        store.delete_task(task_id)
        display_task_deleted(task_id)
    else:
        display_success("Delete cancelled. Task was not deleted.")


def handle_mark_complete(store: TaskStore) -> None:
    """Handle marking a task as complete.

    Args:
        store: The TaskStore instance.
    """
    print("\n--- Mark Task Complete ---")
    tasks = store.get_all_tasks()

    if not tasks:
        display_error("No tasks available.")
        return

    display_tasks(tasks)
    task_id = get_task_id()

    try:
        updated_task = store.mark_complete(task_id)
        display_task_marked_complete(task_id)
    except Exception as e:
        display_error(str(e))


def handle_mark_incomplete(store: TaskStore) -> None:
    """Handle marking a task as incomplete.

    Args:
        store: The TaskStore instance.
    """
    print("\n--- Mark Task Incomplete ---")
    tasks = store.get_all_tasks()

    if not tasks:
        display_error("No tasks available.")
        return

    display_tasks(tasks)
    task_id = get_task_id()

    try:
        updated_task = store.mark_incomplete(task_id)
        display_task_marked_incomplete(task_id)
    except Exception as e:
        display_error(str(e))


if __name__ == "__main__":
    main()
