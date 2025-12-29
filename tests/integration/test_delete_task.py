"""Integration tests for delete task flow."""

import unittest

from src.models.task import Task
from src.services.task_store import TaskStore
from src.errors import TaskNotFoundError


class TestDeleteTaskIntegration(unittest.TestCase):
    """Integration tests for deleting tasks."""

    def test_delete_single_task(self) -> None:
        """Test deleting the only task."""
        store = TaskStore()
        store.add_task("Test task")

        store.delete_task(1)

        self.assertEqual(len(store.get_all_tasks()), 0)

    def test_delete_first_of_multiple(self) -> None:
        """Test deleting the first task of multiple."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.add_task("Task 3")

        store.delete_task(1)

        tasks = store.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Task 2")
        self.assertEqual(tasks[1].title, "Task 3")

    def test_delete_middle_task(self) -> None:
        """Test deleting a middle task."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.add_task("Task 3")

        store.delete_task(2)

        tasks = store.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 3)

    def test_delete_last_task(self) -> None:
        """Test deleting the last task."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")

        store.delete_task(2)

        tasks = store.get_all_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, 1)

    def test_delete_nonexistent_task(self) -> None:
        """Test that deleting nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.delete_task(99)

    def test_ids_not_reused(self) -> None:
        """Test that deleted task IDs are not reused."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.delete_task(1)
        new_task = store.add_task("New task")

        self.assertEqual(new_task.id, 3)  # ID 1 was deleted, ID 2 exists, so new is 3

    def test_delete_preserves_remaining_tasks(self) -> None:
        """Test that deleting a task preserves remaining tasks."""
        store = TaskStore()
        store.add_task("Task 1", "Description 1")
        task2 = store.add_task("Task 2", "Description 2")
        task2.status = True
        store.add_task("Task 3")

        store.delete_task(2)

        tasks = store.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].description, "Description 1")
        self.assertEqual(tasks[1].id, 3)


if __name__ == "__main__":
    unittest.main()
