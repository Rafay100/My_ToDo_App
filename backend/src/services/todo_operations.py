from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.models import User, Todo  # Use existing models
from ..models.task_update import TaskUpdate  # Use our custom model
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole


class TodoOperationsService:
    """Service for todo operations"""

    def __init__(self, session: Session):
        self.session = session

    def add_task(self, user_id: UUID, title: str, description: Optional[str] = None) -> Todo:
        """Add a new task for a user using existing Todo model"""
        task = Todo(
            title=title,
            user_id=user_id,
            is_completed=False  # Default to not completed
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def list_tasks(self, user_id: UUID, status_filter: Optional[str] = None) -> List[Todo]:
        """List tasks for a user, optionally filtered by status using existing Todo model"""
        query = select(Todo).where(Todo.user_id == user_id)

        # Note: The existing Todo model doesn't have a status field, only is_completed
        # So we'll adapt to the existing schema
        if status_filter:
            try:
                # Convert status filter to boolean for is_completed
                if status_filter.lower() in ['completed', 'true']:
                    query = query.where(Todo.is_completed == True)
                elif status_filter.lower() in ['active', 'false', 'pending']:
                    query = query.where(Todo.is_completed == False)
            except ValueError:
                # If invalid status, ignore the filter
                pass

        tasks = self.session.exec(query).all()
        return tasks

    def update_task(self, task_id: UUID, updates: TaskUpdate) -> Optional[Todo]:
        """Update an existing task using existing Todo model"""
        task = self.session.get(Todo, task_id)
        if not task:
            return None

        # Apply updates - only update title if provided
        if updates.title:
            task.title = updates.title

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def complete_task(self, task_id: UUID) -> Optional[Todo]:
        """Mark a task as completed using existing Todo model"""
        task = self.session.get(Todo, task_id)
        if not task:
            return None

        task.is_completed = True

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task using existing Todo model"""
        task = self.session.get(Todo, task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def create_conversation(self, user_id: UUID, title: Optional[str] = None) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            title=title,
            user_id=user_id
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_conversation_messages(self, conversation_id: UUID) -> List[Message]:
        """Get all messages in a conversation"""
        query = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        messages = self.session.exec(query).all()
        return messages

    def add_message(self, conversation_id: UUID, role: MessageRole, content: str, metadata: Optional[dict] = None) -> Message:
        """Add a message to a conversation"""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata_=metadata
        )
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message