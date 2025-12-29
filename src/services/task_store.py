"""In-memory task storage and CRUD operations."""

from datetime import datetime
from typing import List, Optional

from src.errors import (
    DuplicateStateError,
    TaskNotFoundError,
)
from src.models.task import Task


class TaskStore:
    """Manages in-memory storage of tasks.

    Attributes:
        tasks: List of all tasks, ordered by creation time.
        next_id: Counter for generating sequential task IDs.

    All state is ephemeral and lost when the application exits.
    """

    def __init__(self) -> None:
        """Initialize an empty task store."""
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """Create a new task and add it to the store.

        Args:
            title: Task title (1-200 characters, required).
            description: Optional task description (0-500 characters).

        Returns:
            The newly created Task.

        Raises:
            EmptyTitleError: If title is empty or whitespace.
            TitleTooLongError: If title exceeds 200 characters.
        """
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            status=False,
            created_at=datetime.now(),
        )
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in creation order.

        Returns:
            List of all tasks, oldest first.
            Returns empty list if no tasks exist.
        """
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Task:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The Task with the given ID.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)

    def update_task(self, task_id: int, new_title: str) -> Task:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update.
            new_title: The new title for the task.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            EmptyTitleError: If new_title is empty or whitespace.
            TitleTooLongError: If new_title exceeds 200 characters.
        """
        task = self.get_task_by_id(task_id)
        # Create new Task with updated title to trigger validation
        updated_task = Task(
            id=task.id,
            title=new_title,
            description=task.description,
            status=task.status,
            created_at=task.created_at,
        )
        # Find and replace the task
        index = self._find_task_index(task_id)
        self.tasks[index] = updated_task
        return updated_task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
        """
        index = self._find_task_index(task_id)
        self.tasks.pop(index)
        # Note: next_id is NOT decremented; IDs are never reused

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            DuplicateStateError: If task is already complete.
        """
        task = self.get_task_by_id(task_id)
        if task.status:
            raise DuplicateStateError(task_id, "complete")
        task.status = True
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            DuplicateStateError: If task is already incomplete.
        """
        task = self.get_task_by_id(task_id)
        if not task.status:
            raise DuplicateStateError(task_id, "incomplete")
        task.status = False
        return task

    def _find_task_index(self, task_id: int) -> int:
        """Find the index of a task by ID.

        Args:
            task_id: The ID to search for.

        Returns:
            The index of the task in the list.

        Raises:
            TaskNotFoundError: If task not found.
        """
        for index, task in enumerate(self.tasks):
            if task.id == task_id:
                return index
        raise TaskNotFoundError(task_id)

    def task_exists(self, task_id: int) -> bool:
        """Check if a task with the given ID exists.

        Args:
            task_id: The ID to check.

        Returns:
            True if task exists, False otherwise.
        """
        try:
            self.get_task_by_id(task_id)
            return True
        except TaskNotFoundError:
            return False
