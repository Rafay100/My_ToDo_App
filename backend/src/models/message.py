from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageBase(SQLModel):
    conversation_id: UUID = Field(foreign_key="conversation.id")
    role: MessageRole
    content: str = Field(nullable=False)


class Message(MessageBase, table=True):
    """
    Represents an individual message in a conversation
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"


class MessageCreate(MessageBase):
    pass