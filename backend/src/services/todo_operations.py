from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate, MessageRole
from ..models.user import User


class TodoOperationsService:
    """Service for todo operations"""

    def __init__(self, session: Session):
        self.session = session

    def add_task(self, user_id: UUID, title: str, description: Optional[str] = None) -> Task:
        """Add a new task for a user"""
        task = Task(
            title=title,
            description=description,
            user_id=user_id
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def list_tasks(self, user_id: UUID, status_filter: Optional[str] = None) -> List[Task]:
        """List tasks for a user, optionally filtered by status"""
        query = select(Task).where(Task.user_id == user_id)

        if status_filter:
            try:
                status = TaskStatus(status_filter.lower())
                query = query.where(Task.status == status)
            except ValueError:
                # If invalid status, ignore the filter
                pass

        tasks = self.session.exec(query).all()
        return tasks

    def update_task(self, task_id: UUID, updates: TaskUpdate) -> Optional[Task]:
        """Update an existing task"""
        task = self.session.get(Task, task_id)
        if not task:
            return None

        # Apply updates
        for field, value in updates.dict(exclude_unset=True).items():
            setattr(task, field, value)

        # If status is being updated to completed, set completed_at
        if updates.status == TaskStatus.COMPLETED and task.status != TaskStatus.COMPLETED:
            from datetime import datetime
            task.completed_at = datetime.now()
        elif updates.status == TaskStatus.ACTIVE:
            task.completed_at = None

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def complete_task(self, task_id: UUID) -> Optional[Task]:
        """Mark a task as completed"""
        task = self.session.get(Task, task_id)
        if not task:
            return None

        task.status = TaskStatus.COMPLETED
        from datetime import datetime
        task.completed_at = datetime.now()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: UUID) -> bool:
        """Delete a task"""
        task = self.session.get(Task, task_id)
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