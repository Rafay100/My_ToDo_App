from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
import json


class TaskEventType(str, Enum):
    CREATED = "created"
    UPDATED = "updated"
    STATUS_CHANGED = "status_changed"
    DELETED = "deleted"
    COMPLETED = "completed"
    REOPENED = "reopened"


class TaskEventBase(SQLModel):
    task_id: UUID = Field(foreign_key="task.id", index=True)
    event_type: TaskEventType = Field(index=True)  # For efficient querying
    payload: str = Field(sa_column_kwargs={"server_default": "'{}'"})  # JSON string
    correlation_id: UUID = Field(default_factory=uuid4)  # For tracking related events
    causation_id: Optional[UUID] = Field(default=None)  # For tracking causality


class TaskEvent(TaskEventBase, table=True):
    """
    Immutable record of task lifecycle events for event sourcing
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False, index=True)  # For chronological queries

    def __repr__(self):
        return f"<TaskEvent(id={self.id}, task_id={self.task_id}, event_type={self.event_type}, timestamp={self.timestamp})>"

    @property
    def parsed_payload(self) -> Dict[str, Any]:
        """
        Parse the payload from JSON string to dictionary
        """
        try:
            return json.loads(self.payload) if self.payload else {}
        except json.JSONDecodeError:
            return {}

    def set_payload(self, data: Dict[str, Any]) -> None:
        """
        Set the payload as a JSON string
        """
        self.payload = json.dumps(data)


class TaskEventCreate(TaskEventBase):
    pass


class TaskEventRead(TaskEventBase):
    id: UUID
    timestamp: datetime

    @property
    def parsed_payload(self) -> Dict[str, Any]:
        """
        Parse the payload from JSON string to dictionary
        """
        try:
            return json.loads(self.payload) if self.payload else {}
        except json.JSONDecodeError:
            return {}