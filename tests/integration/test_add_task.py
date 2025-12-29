"""Integration tests for add task flow."""

import unittest
from datetime import datetime

from src.models.task import Task
from src.services.task_store import TaskStore


class TestAddTaskIntegration(unittest.TestCase):
    """Integration tests for adding tasks."""

    def test_add_task_from_empty_state(self) -> None:
        """Test adding a task when store is empty."""
        store = TaskStore()

        task = store.add_task("Buy groceries")

        self.assertIsNotNone(task)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Buy groceries")
        self.assertEqual(len(store.get_all_tasks()), 1)

    def test_add_multiple_tasks_in_sequence(self) -> None:
        """Test adding multiple tasks in sequence."""
        store = TaskStore()

        task1 = store.add_task("Task 1")
        task2 = store.add_task("Task 2")
        task3 = store.add_task("Task 3")

        tasks = store.get_all_tasks()

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)

    def test_add_task_with_description(self) -> None:
        """Test adding a task with description."""
        store = TaskStore()

        task = store.add_task("Buy groceries", "Milk, eggs, bread")

        self.assertEqual(task.description, "Milk, eggs, bread")
        self.assertEqual(len(store.get_all_tasks()), 1)

    def test_task_timestamps_are_set(self) -> None:
        """Test that task creation timestamps are automatically set."""
        store = TaskStore()

        task = store.add_task("Test task")

        self.assertIsNotNone(task.created_at)

    def test_tasks_persist_in_memory(self) -> None:
        """Test that tasks persist in memory after addition."""
        store = TaskStore()

        store.add_task("Task 1")
        store.add_task("Task 2")

        # Get all tasks and verify
        tasks = store.get_all_tasks()
        self.assertEqual(len(tasks), 2)

        # Add more tasks
        store.add_task("Task 3")

        # Verify all tasks still exist
        tasks = store.get_all_tasks()
        self.assertEqual(len(tasks), 3)

    def test_id_counter_increments(self) -> None:
        """Test that ID counter increments correctly."""
        store = TaskStore()

        for i in range(5):
            task = store.add_task(f"Task {i+1}")
            self.assertEqual(task.id, i + 1)

        self.assertEqual(store.next_id, 6)


if __name__ == "__main__":
    unittest.main()
