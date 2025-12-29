"""Integration tests for view tasks flow."""

import unittest
from datetime import datetime

from src.models.task import Task
from src.services.task_store import TaskStore


class TestViewTasksIntegration(unittest.TestCase):
    """Integration tests for viewing tasks."""

    def test_view_empty_list(self) -> None:
        """Test viewing tasks when list is empty."""
        store = TaskStore()

        tasks = store.get_all_tasks()

        self.assertEqual(tasks, [])
        self.assertEqual(len(tasks), 0)

    def test_view_single_task(self) -> None:
        """Test viewing a single task."""
        store = TaskStore()
        store.add_task("Test task")

        tasks = store.get_all_tasks()

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test task")

    def test_view_multiple_tasks_in_order(self) -> None:
        """Test that tasks are viewed in creation order."""
        store = TaskStore()
        store.add_task("First task")
        store.add_task("Second task")
        store.add_task("Third task")

        tasks = store.get_all_tasks()

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].title, "First task")
        self.assertEqual(tasks[1].title, "Second task")
        self.assertEqual(tasks[2].title, "Third task")

    def test_view_shows_correct_status(self) -> None:
        """Test that task status is correctly shown."""
        store = TaskStore()
        store.add_task("Incomplete task")
        store.add_task("Complete task")
        store.mark_complete(2)

        tasks = store.get_all_tasks()

        self.assertEqual(tasks[0].status, False)
        self.assertEqual(tasks[1].status, True)

    def test_view_returns_copy(self) -> None:
        """Test that get_all_tasks returns a copy, not the original list."""
        store = TaskStore()
        store.add_task("Test task")

        tasks1 = store.get_all_tasks()
        tasks1.clear()

        tasks2 = store.get_all_tasks()

        self.assertEqual(len(tasks2), 1)  # Original list is not affected


if __name__ == "__main__":
    unittest.main()
