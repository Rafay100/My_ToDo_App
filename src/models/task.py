"""Task data model with validation."""

from dataclasses import dataclass, field
from datetime import datetime

from src.errors import EmptyTitleError, InvalidIdError, TitleTooLongError


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique positive integer identifier (assigned sequentially).
        title: Task description (1-200 characters, required).
        description: Extended task details (0-500 characters, optional).
        status: Boolean indicating completion status.
        created_at: Timestamp of task creation.

    All fields except description are required.
    """

    id: int
    title: str
    description: str = field(default="")
    status: bool = field(default=False)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Validate task fields after initialization."""
        # Validate title is not empty or whitespace-only
        stripped_title = self.title.strip()
        if not stripped_title:
            raise EmptyTitleError()

        # Validate title length (after stripping)
        if len(stripped_title) > 200:
            raise TitleTooLongError(len(stripped_title))

        # Use stripped title
        self.title = stripped_title

        # Validate description length if provided
        if self.description:
            stripped_desc = self.description.strip()
            if len(stripped_desc) > 500:
                raise TitleTooLongError(len(stripped_desc), 500)
            self.description = stripped_desc

        # Validate ID is positive
        if self.id < 1:
            raise InvalidIdError(str(self.id))

    def __str__(self) -> str:
        """Return a string representation of the task."""
        status_str = "[X]" if self.status else "[ ]"
        desc_str = f" - {self.description}" if self.description else ""
        return f"{self.id}. {status_str} {self.title}{desc_str}"
