"""Unit tests for the TaskStore class."""

import unittest

from src.models.task import Task
from src.services.task_store import TaskStore
from src.errors import (
    DuplicateStateError,
    EmptyTitleError,
    TaskNotFoundError,
    TitleTooLongError,
)


class TestTaskStoreInitialization(unittest.TestCase):
    """Tests for TaskStore initialization."""

    def test_initialize_empty_store(self) -> None:
        """Test that a new TaskStore is empty."""
        store = TaskStore()
        self.assertEqual(len(store.tasks), 0)
        self.assertEqual(store.next_id, 1)


class TestAddTask(unittest.TestCase):
    """Tests for the add_task method."""

    def test_add_single_task(self) -> None:
        """Test adding a single task."""
        store = TaskStore()
        task = store.add_task("Test task")

        self.assertEqual(len(store.tasks), 1)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.status, False)
        self.assertEqual(store.next_id, 2)

    def test_add_multiple_tasks(self) -> None:
        """Test adding multiple tasks."""
        store = TaskStore()
        task1 = store.add_task("Task 1")
        task2 = store.add_task("Task 2")
        task3 = store.add_task("Task 3")

        self.assertEqual(len(store.tasks), 3)
        self.assertEqual(task1.id, 1)
        self.assertEqual(task2.id, 2)
        self.assertEqual(task3.id, 3)
        self.assertEqual(store.next_id, 4)

    def test_add_task_with_description(self) -> None:
        """Test adding a task with description."""
        store = TaskStore()
        task = store.add_task("Test task", "Test description")

        self.assertEqual(task.description, "Test description")

    def test_add_empty_title_raises_error(self) -> None:
        """Test that adding task with empty title raises error."""
        store = TaskStore()

        with self.assertRaises(EmptyTitleError):
            store.add_task("")

    def test_add_title_too_long_raises_error(self) -> None:
        """Test that adding task with title > 200 chars raises error."""
        store = TaskStore()
        long_title = "x" * 201

        with self.assertRaises(TitleTooLongError):
            store.add_task(long_title)


class TestGetAllTasks(unittest.TestCase):
    """Tests for the get_all_tasks method."""

    def test_get_empty_list(self) -> None:
        """Test getting all tasks from empty store."""
        store = TaskStore()
        tasks = store.get_all_tasks()

        self.assertEqual(tasks, [])
        self.assertIsNot(tasks, store.tasks)  # Should return a copy

    def test_get_tasks_in_order(self) -> None:
        """Test that tasks are returned in creation order."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.add_task("Task 3")

        tasks = store.get_all_tasks()

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, 1)
        self.assertEqual(tasks[1].id, 2)
        self.assertEqual(tasks[2].id, 3)


class TestGetTaskById(unittest.TestCase):
    """Tests for the get_task_by_id method."""

    def test_get_existing_task(self) -> None:
        """Test getting an existing task by ID."""
        store = TaskStore()
        store.add_task("Test task")
        task = store.get_task_by_id(1)

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")

    def test_get_nonexistent_task_raises_error(self) -> None:
        """Test that getting nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.get_task_by_id(1)


class TestUpdateTask(unittest.TestCase):
    """Tests for the update_task method."""

    def test_update_task_title(self) -> None:
        """Test updating a task's title."""
        store = TaskStore()
        store.add_task("Original title")
        updated_task = store.update_task(1, "New title")

        self.assertEqual(updated_task.title, "New title")
        self.assertEqual(store.tasks[0].title, "New title")

    def test_update_nonexistent_task_raises_error(self) -> None:
        """Test that updating nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.update_task(1, "New title")

    def test_update_with_empty_title_raises_error(self) -> None:
        """Test that updating with empty title raises error."""
        store = TaskStore()
        store.add_task("Test task")

        with self.assertRaises(EmptyTitleError):
            store.update_task(1, "")


class TestDeleteTask(unittest.TestCase):
    """Tests for the delete_task method."""

    def test_delete_task(self) -> None:
        """Test deleting a task."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")

        store.delete_task(1)

        self.assertEqual(len(store.tasks), 1)
        self.assertEqual(store.tasks[0].id, 2)  # Remaining task keeps its ID

    def test_delete_nonexistent_task_raises_error(self) -> None:
        """Test that deleting nonexistent task raises error."""
        store = TaskStore()

        with self.assertRaises(TaskNotFoundError):
            store.delete_task(1)

    def test_ids_not_reused_after_delete(self) -> None:
        """Test that deleted task IDs are not reused."""
        store = TaskStore()
        store.add_task("Task 1")
        store.delete_task(1)
        new_task = store.add_task("New task")

        self.assertEqual(new_task.id, 2)  # ID 1 was deleted, not reused


class TestMarkComplete(unittest.TestCase):
    """Tests for the mark_complete method."""

    def test_mark_incomplete_task_complete(self) -> None:
        """Test marking an incomplete task as complete."""
        store = TaskStore()
        store.add_task("Test task")
        updated_task = store.mark_complete(1)

        self.assertEqual(updated_task.status, True)
        self.assertEqual(store.tasks[0].status, True)

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
            store.mark_complete(1)


class TestMarkIncomplete(unittest.TestCase):
    """Tests for the mark_incomplete method."""

    def test_mark_complete_task_incomplete(self) -> None:
        """Test marking a complete task as incomplete."""
        store = TaskStore()
        store.add_task("Test task")
        store.mark_complete(1)
        updated_task = store.mark_incomplete(1)

        self.assertEqual(updated_task.status, False)
        self.assertEqual(store.tasks[0].status, False)

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
            store.mark_incomplete(1)


class TestTaskExists(unittest.TestCase):
    """Tests for the task_exists method."""

    def test_existing_task_exists(self) -> None:
        """Test that existing task is found."""
        store = TaskStore()
        store.add_task("Test task")

        self.assertTrue(store.task_exists(1))

    def test_nonexistent_task_not_found(self) -> None:
        """Test that nonexistent task is not found."""
        store = TaskStore()

        self.assertFalse(store.task_exists(1))

    def test_deleted_task_not_found(self) -> None:
        """Test that deleted task is not found."""
        store = TaskStore()
        store.add_task("Test task")
        store.delete_task(1)

        self.assertFalse(store.task_exists(1))


if __name__ == "__main__":
    unittest.main()
