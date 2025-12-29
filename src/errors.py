"""Custom exceptions for the Todo CLI application."""


class TaskNotFoundError(Exception):
    """Raised when a task ID does not exist."""

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class ValidationError(Exception):
    """Base class for validation errors."""

    pass


class EmptyTitleError(ValidationError):
    """Raised when a task title is empty or whitespace."""

    def __init__(self) -> None:
        super().__init__("Task title cannot be empty")


class TitleTooLongError(ValidationError):
    """Raised when a task title exceeds maximum length."""

    def __init__(self, length: int, max_length: int = 200) -> None:
        self.length = length
        self.max_length = max_length
        super().__init__(
            f"Task title is {length} characters, exceeds maximum of {max_length}"
        )


class InvalidIdError(ValidationError):
    """Raised when a task ID is not a positive integer."""

    def __init__(self, input_value: str) -> None:
        self.input_value = input_value
        super().__init__(f"Invalid task ID: '{input_value}'. Must be a positive integer.")


class DuplicateStateError(ValidationError):
    """Raised when trying to mark a task as a state it already is."""

    def __init__(self, task_id: int, state: str) -> None:
        self.task_id = task_id
        self.state = state
        super().__init__(f"Task {task_id} is already {state}")
