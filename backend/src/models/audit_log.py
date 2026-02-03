from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
import json


class AuditLogBase(SQLModel):
    event_type: str = Field(index=True)  # For efficient querying
    entity_id: Optional[UUID] = Field(default=None, index=True)  # For efficient querying
    entity_type: str = Field(index=True)  # For efficient querying
    user_id: Optional[UUID] = Field(default=None, foreign_key="user.id", index=True)  # For efficient querying
    action: str
    old_values: Optional[str] = Field(default=None)  # JSON string
    new_values: Optional[str] = Field(default=None)  # JSON string
    metadata: Optional[str] = Field(default=None)  # JSON string


class AuditLog(AuditLogBase, table=True):
    """
    Persistent log of all system events for compliance and debugging
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now, nullable=False, index=True)  # For chronological queries

    def __repr__(self):
        return f"<AuditLog(id={self.id}, event_type={self.event_type}, entity_type={self.entity_type}, action={self.action})>"

    @property
    def parsed_old_values(self) -> Dict[str, Any]:
        """
        Parse old_values from JSON string to dictionary
        """
        try:
            return json.loads(self.old_values) if self.old_values else {}
        except json.JSONDecodeError:
            return {}

    @property
    def parsed_new_values(self) -> Dict[str, Any]:
        """
        Parse new_values from JSON string to dictionary
        """
        try:
            return json.loads(self.new_values) if self.new_values else {}
        except json.JSONDecodeError:
            return {}

    @property
    def parsed_metadata(self) -> Dict[str, Any]:
        """
        Parse metadata from JSON string to dictionary
        """
        try:
            return json.loads(self.metadata) if self.metadata else {}
        except json.JSONDecodeError:
            return {}

    def set_old_values(self, data: Dict[str, Any]) -> None:
        """
        Set old_values as a JSON string
        """
        self.old_values = json.dumps(data)

    def set_new_values(self, data: Dict[str, Any]) -> None:
        """
        Set new_values as a JSON string
        """
        self.new_values = json.dumps(data)

    def set_metadata(self, data: Dict[str, Any]) -> None:
        """
        Set metadata as a JSON string
        """
        self.metadata = json.dumps(data)


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: UUID
    timestamp: datetime

    @property
    def parsed_old_values(self) -> Dict[str, Any]:
        """
        Parse old_values from JSON string to dictionary
        """
        try:
            return json.loads(self.old_values) if self.old_values else {}
        except json.JSONDecodeError:
            return {}

    @property
    def parsed_new_values(self) -> Dict[str, Any]:
        """
        Parse new_values from JSON string to dictionary
        """
        try:
            return json.loads(self.new_values) if self.new_values else {}
        except json.JSONDecodeError:
            return {}

    @property
    def parsed_metadata(self) -> Dict[str, Any]:
        """
        Parse metadata from JSON string to dictionary
        """
        try:
            return json.loads(self.metadata) if self.metadata else {}
        except json.JSONDecodeError:
            return {}