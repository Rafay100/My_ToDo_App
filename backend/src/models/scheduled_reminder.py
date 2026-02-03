from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class ScheduledReminderBase(SQLModel):
    task_id: UUID = Field(foreign_key="task.id")
    user_id: UUID = Field(foreign_key="user.id")
    scheduled_time: datetime = Field(index=True)  # For efficient querying
    notification_method: str = Field(default="push")  # email, push, sms


class ScheduledReminder(ScheduledReminderBase, table=True):
    """
    Represents a scheduled notification for upcoming due dates
    """
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    is_sent: bool = Field(default=False, index=True)  # For efficient querying of unsent reminders
    sent_at: Optional[datetime] = Field(default=None)

    def __repr__(self):
        return f"<ScheduledReminder(id={self.id}, task_id={self.task_id}, scheduled_time={self.scheduled_time}, is_sent={self.is_sent})>"

    def should_send_notification(self) -> bool:
        """
        Determines if the reminder should be sent
        - Has not been sent yet
        - Scheduled time has passed
        """
        return not self.is_sent and self.scheduled_time <= datetime.now()


class ScheduledReminderCreate(ScheduledReminderBase):
    pass


class ScheduledReminderRead(ScheduledReminderBase):
    id: UUID
    created_at: datetime
    is_sent: bool
    sent_at: Optional[datetime]

    def should_send_notification(self) -> bool:
        """
        Determines if the reminder should be sent
        - Has not been sent yet
        - Scheduled time has passed
        """
        return not self.is_sent and self.scheduled_time <= datetime.now()


class ScheduledReminderUpdate(SQLModel):
    scheduled_time: Optional[datetime] = None
    notification_method: Optional[str] = None
    is_sent: Optional[bool] = None
    sent_at: Optional[datetime] = None