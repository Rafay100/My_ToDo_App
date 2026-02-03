from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
import json


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class NotificationMethod(str, Enum):
    EMAIL = "email"
    PUSH = "push"
    SMS = "sms"


class TaskBase(SQLModel):
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    due_date: Optional[datetime] = Field(default=None)
    tags: Optional[str] = Field(default=None)  # JSON string representation
    recurrence_rule: Optional[str] = Field(default=None)
    parent_task_id: Optional[UUID] = Field(default=None, foreign_key="task.id")
    user_id: UUID = Field(foreign_key="user.id")


class Task(TaskBase, table=True):
    """
    Represents a todo item managed by the user with advanced features
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    completed_at: Optional[datetime] = Field(default=None)

    def __repr__(self):
        return f"<Task(id={self.id}, title={self.title}, status={self.status}, priority={self.priority})>"

    @property
    def parsed_tags(self) -> List[str]:
        """Parse tags from JSON string to list"""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []

    def set_tags(self, tags_list: List[str]) -> None:
        """Set tags as JSON string"""
        if len(tags_list) > 10:
            raise ValueError("Cannot have more than 10 tags")
        for tag in tags_list:
            if len(tag) > 50:
                raise ValueError("Each tag cannot exceed 50 characters")
        self.tags = json.dumps(tags_list)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    @property
    def parsed_tags(self) -> List[str]:
        """Parse tags from JSON string to list"""
        if self.tags:
            try:
                return json.loads(self.tags)
            except json.JSONDecodeError:
                return []
        return []


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[str] = None
    recurrence_rule: Optional[str] = None
    parent_task_id: Optional[UUID] = None