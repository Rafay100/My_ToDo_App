"""Integration tests for mark complete/incomplete flow."""

import unittest

from src.models.task import Task
from src.services.task_store import TaskStore
from src.errors import DuplicateStateError, TaskNotFoundError


class TestMarkCompleteIntegration(unittest.TestCase):
    """Integration tests for marking tasks complete."""

    def test_mark_incomplete_task_complete(self) -> None:
        """Test marking an incomplete task as complete."""
        store = TaskStore()
        store.add_task("Test task")

        updated_task = store.mark_complete(1)

        self.assertEqual(updated_task.status, True)
        self.assertEqual(store.get_task_by_id(1).status, True)

    def test_mark_already_complete_raises_error(self) -> None:
        """Test that marking already complete task raises error."""
        store = TaskStore()
        store.add_task("Test task")
        store.mark_complete(1)

        with self.assertRaises(DuplicateStateError):
            store.mark_complete(1)

    def test_mark_nonexistent_task_raises_error(self) -> None:
        """Test that marking nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.mark_complete(99)

    def test_mark_complete_preserves_other_fields(self) -> None:
        """Test that marking complete preserves other fields."""
        store = TaskStore()
        store.add_task("Test task", "Description")

        updated_task = store.mark_complete(1)

        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.title, "Test task")
        self.assertEqual(updated_task.description, "Description")

    def test_mark_multiple_tasks_complete(self) -> None:
        """Test marking multiple tasks complete independently."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.add_task("Task 3")

        store.mark_complete(1)
        store.mark_complete(3)

        self.assertEqual(store.get_task_by_id(1).status, True)
        self.assertEqual(store.get_task_by_id(2).status, False)
        self.assertEqual(store.get_task_by_id(3).status, True)


class TestMarkIncompleteIntegration(unittest.TestCase):
    """Integration tests for marking tasks incomplete."""

    def test_mark_complete_task_incomplete(self) -> None:
        """Test marking a complete task as incomplete."""
        store = TaskStore()
        store.add_task("Test task")
        store.mark_complete(1)

        updated_task = store.mark_incomplete(1)

        self.assertEqual(updated_task.status, False)
        self.assertEqual(store.get_task_by_id(1).status, False)

    def test_mark_already_incomplete_raises_error(self) -> None:
        """Test that marking already incomplete task raises error."""
        store = TaskStore()
        store.add_task("Test task")

        with self.assertRaises(DuplicateStateError):
            store.mark_incomplete(1)

    def test_mark_nonexistent_task_raises_error(self) -> None:
        """Test that marking nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.mark_incomplete(99)

    def test_mark_incomplete_preserves_other_fields(self) -> None:
        """Test that marking incomplete preserves other fields."""
        store = TaskStore()
        store.add_task("Test task", "Description")

        store.mark_complete(1)
        updated_task = store.mark_incomplete(1)

        self.assertEqual(updated_task.id, 1)
        self.assertEqual(updated_task.title, "Test task")
        self.assertEqual(updated_task.description, "Description")

    def test_toggle_complete_incomplete(self) -> None:
        """Test toggling task between complete and incomplete."""
        store = TaskStore()
        store.add_task("Test task")

        # Start incomplete
        self.assertEqual(store.get_task_by_id(1).status, False)

        # Mark complete
        store.mark_complete(1)
        self.assertEqual(store.get_task_by_id(1).status, True)

        # Mark incomplete
        store.mark_incomplete(1)
        self.assertEqual(store.get_task_by_id(1).status, False)

        # Mark complete again
        store.mark_complete(1)
        self.assertEqual(store.get_task_by_id(1).status, True)


if __name__ == "__main__":
    unittest.main()
