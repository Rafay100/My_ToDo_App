from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class TaskTemplateBase(SQLModel):
    base_task_id: UUID = Field(foreign_key="task.id")
    recurrence_rule: str = Field(min_length=1)  # RFC 5545 format
    ends_on: Optional[datetime] = Field(default=None)
    occurrence_count: Optional[int] = Field(default=None, ge=1)  # Greater than or equal to 1
    user_id: UUID = Field(foreign_key="user.id")


class TaskTemplate(TaskTemplateBase, table=True):
    """
    Defines recurrence patterns for generating recurring task instances
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)
    is_active: bool = Field(default=True)

    def __repr__(self):
        return f"<TaskTemplate(id={self.id}, base_task_id={self.base_task_id}, recurrence_rule={self.recurrence_rule})>"

    def is_valid_recurrence(self) -> bool:
        """
        Validates that the recurrence configuration is valid
        - Either ends_on or occurrence_count must be specified (not infinite recurrences)
        """
        return self.ends_on is not None or self.occurrence_count is not None


class TaskTemplateCreate(TaskTemplateBase):
    pass


class TaskTemplateRead(TaskTemplateBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    def is_valid_recurrence(self) -> bool:
        """
        Validates that the recurrence configuration is valid
        - Either ends_on or occurrence_count must be specified (not infinite recurrences)
        """
        return self.ends_on is not None or self.occurrence_count is not None


class TaskTemplateUpdate(SQLModel):
    recurrence_rule: Optional[str] = None
    ends_on: Optional[datetime] = None
    occurrence_count: Optional[int] = None
    is_active: Optional[bool] = None