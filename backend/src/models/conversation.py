from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from .user import User


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None, max_length=255)
    user_id: UUID = Field(foreign_key="user.id")


class Conversation(ConversationBase, table=True):
    """
    Represents a collection of messages between a user and the AI agent
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")

    def __repr__(self):
        return f"<Conversation(id={self.id}, title={self.title})>"


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime