"""Integration tests for update task flow."""

import unittest

from src.models.task import Task
from src.services.task_store import TaskStore
from src.errors import EmptyTitleError, TaskNotFoundError, TitleTooLongError


class TestUpdateTaskIntegration(unittest.TestCase):
    """Integration tests for updating tasks."""

    def test_update_task_title(self) -> None:
        """Test updating a task's title."""
        store = TaskStore()
        store.add_task("Original title")

        updated_task = store.update_task(1, "New title")

        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(store.get_task_by_id(1).title, "New title")

    def test_update_preserves_other_fields(self) -> None:
        """Test that updating title preserves other fields."""
        store = TaskStore()
        store.add_task("Original title", "Original description")
        original_created = store.get_task_by_id(1).created_at

        updated_task = store.update_task(1, "New title")

        self.assertEqual(updated_task.description, "Original description")
        self.assertEqual(updated_task.created_at, original_created)
        self.assertEqual(updated_task.status, False)
        self.assertEqual(updated_task.id, 1)

    def test_update_nonexistent_task(self) -> None:
        """Test that updating nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.update_task(99, "New title")

    def test_update_with_empty_title(self) -> None:
        """Test that updating with empty title raises error."""
        store = TaskStore()
        store.add_task("Test task")

        with self.assertRaises(EmptyTitleError):
            store.update_task(1, "")

    def test_update_with_whitespace_title(self) -> None:
        """Test that updating with whitespace title raises error."""
        store = TaskStore()
        store.add_task("Test task")

        with self.assertRaises(EmptyTitleError):
            store.update_task(1, "   ")

    def test_update_with_title_too_long(self) -> None:
        """Test that updating with title > 200 chars raises error."""
        store = TaskStore()
        store.add_task("Test task")
        long_title = "x" * 201

        with self.assertRaises(TitleTooLongError):
            store.update_task(1, long_title)

    def test_update_multiple_tasks(self) -> None:
        """Test updating multiple tasks independently."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.add_task("Task 3")

        store.update_task(2, "Updated Task 2")

        self.assertEqual(store.get_task_by_id(1).title, "Task 1")
        self.assertEqual(store.get_task_by_id(2).title, "Updated Task 2")
        self.assertEqual(store.get_task_by_id(3).title, "Task 3")


if __name__ == "__main__":
    unittest.main()
