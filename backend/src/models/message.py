from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from .conversation import Conversation


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageBase(SQLModel):
    role: MessageRole
    content: str = Field(nullable=False)
    conversation_id: UUID = Field(foreign_key="conversation.id")
    metadata_: Optional[dict] = Field(default=None, alias="metadata")


class Message(MessageBase, table=True):
    """
    Represents an individual message in a conversation
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationship to conversation
    conversation: Conversation = Relationship(back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, conversation_id={self.conversation_id})>"


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: UUID
    created_at: datetime