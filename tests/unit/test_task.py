"""Unit tests for the Task dataclass."""

import unittest
from datetime import datetime

from src.models.task import Task
from src.errors import EmptyTitleError, TitleTooLongError, InvalidIdError as BaseInvalidIdError


class TestTaskCreation(unittest.TestCase):
    """Tests for Task dataclass creation and validation."""

    def test_create_task_with_minimal_fields(self) -> None:
        """Test creating a task with only required fields."""
        task = Task(id=1, title="Test task")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "")
        self.assertEqual(task.status, False)
        self.assertIsInstance(task.created_at, datetime)

    def test_create_task_with_all_fields(self) -> None:
        """Test creating a task with all fields."""
        now = datetime.now()
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=now,
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.status, False)
        self.assertEqual(task.created_at, now)

    def test_create_task_with_empty_title_raises_error(self) -> None:
        """Test that empty title raises EmptyTitleError."""
        with self.assertRaises(EmptyTitleError):
            Task(id=1, title="")

    def test_create_task_with_whitespace_title_raises_error(self) -> None:
        """Test that whitespace-only title raises EmptyTitleError."""
        with self.assertRaises(EmptyTitleError):
            Task(id=1, title="   ")

    def test_create_task_with_title_too_long_raises_error(self) -> None:
        """Test that title exceeding 200 chars raises TitleTooLongError."""
        long_title = "x" * 201
        with self.assertRaises(TitleTooLongError) as cm:
            Task(id=1, title=long_title)
        self.assertEqual(cm.exception.length, 201)
        self.assertEqual(cm.exception.max_length, 200)

    def test_title_is_stripped(self) -> None:
        """Test that leading/trailing whitespace is stripped from title."""
        task = Task(id=1, title="  Test task  ")
        self.assertEqual(task.title, "Test task")

    def test_description_is_stripped(self) -> None:
        """Test that leading/trailing whitespace is stripped from description."""
        task = Task(id=1, title="Test", description="  Test description  ")
        self.assertEqual(task.description, "Test description")

    def test_description_too_long_raises_error(self) -> None:
        """Test that description exceeding 500 chars raises error."""
        long_desc = "x" * 501
        with self.assertRaises(TitleTooLongError) as cm:
            Task(id=1, title="Test", description=long_desc)
        self.assertEqual(cm.exception.max_length, 500)

    def test_negative_id_raises_error(self) -> None:
        """Test that negative ID raises InvalidIdError."""
        with self.assertRaises(BaseInvalidIdError):
            Task(id=-1, title="Test")

    def test_zero_id_raises_error(self) -> None:
        """Test that zero ID raises InvalidIdError."""
        with self.assertRaises(BaseInvalidIdError):
            Task(id=0, title="Test")


class TestTaskStringRepresentation(unittest.TestCase):
    """Tests for Task string representation."""

    def test_str_incomplete_task(self) -> None:
        """Test string representation of incomplete task."""
        task = Task(id=1, title="Test task")
        self.assertEqual(str(task), "1. [ ] Test task")

    def test_str_complete_task(self) -> None:
        """Test string representation of complete task."""
        task = Task(id=1, title="Test task", status=True)
        self.assertEqual(str(task), "1. [X] Test task")

    def test_str_task_with_description(self) -> None:
        """Test string representation includes description."""
        task = Task(id=1, title="Test task", description="Description here")
        self.assertIn("1. [ ] Test task - Description here", str(task))


class TestTaskEquality(unittest.TestCase):
    """Tests for Task equality."""

    def test_tasks_with_same_values_are_equal(self) -> None:
        """Test that two tasks with same values are equal."""
        now = datetime.now()
        task1 = Task(id=1, title="Test", created_at=now)
        task2 = Task(id=1, title="Test", created_at=now)
        # Note: datetime.now() might differ slightly, so use same now
        self.assertEqual(task1, task2)

    def test_tasks_with_different_ids_are_not_equal(self) -> None:
        """Test that tasks with different IDs are not equal."""
        now = datetime.now()
        task1 = Task(id=1, title="Test", created_at=now)
        task2 = Task(id=2, title="Test", created_at=now)
        self.assertNotEqual(task1, task2)


if __name__ == "__main__":
    unittest.main()
