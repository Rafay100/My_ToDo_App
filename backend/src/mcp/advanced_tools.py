"""
MCP Tools for Advanced Features
Implements MCP tools for advanced todo features: recurring tasks, due dates, priorities, tags
"""
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field
from dapr.ext.mcp import MCTools
from dapr.clients import DaprClient

# Import models
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPriority
from ..models.task_template import TaskTemplate, TaskTemplateCreate
from ..models.scheduled_reminder import ScheduledReminder, ScheduledReminderCreate


class TaskQuery(BaseModel):
    """Query parameters for advanced task operations"""
    priority: Optional[str] = None
    tag: Optional[str] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    status: Optional[str] = None
    search: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "asc"


class AdvancedTodoMCPTools:
    """
    MCP Tools for advanced todo features
    Implements tools for recurring tasks, due dates, priorities, tags, and search
    """

    def __init__(self):
        self.client = DaprClient()
        self.tools = MCTools()

    def register_tools(self):
        """Register all advanced todo tools with MCP"""
        self.tools.register_tool(
            name="create_advanced_task",
            description="Create a task with advanced features like due date, priority, tags, and recurrence",
            parameters={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "Task priority"},
                    "due_date": {"type": "string", "format": "date-time", "description": "Due date for the task"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Tags for categorization"},
                    "recurrence_rule": {"type": "string", "description": "RRULE for recurring tasks"},
                    "user_id": {"type": "string", "description": "ID of the user creating the task"}
                },
                "required": ["title", "user_id"]
            },
            handler=self.create_advanced_task
        )

        self.tools.register_tool(
            name="update_task_advanced",
            description="Update a task with advanced features like due date, priority, tags",
            parameters={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to update"},
                    "title": {"type": "string", "description": "New task title"},
                    "description": {"type": "string", "description": "New task description"},
                    "status": {"type": "string", "enum": ["pending", "in-progress", "completed"], "description": "New task status"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "New task priority"},
                    "due_date": {"type": "string", "format": "date-time", "description": "New due date for the task"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "New tags for categorization"},
                    "recurrence_rule": {"type": "string", "description": "New RRULE for recurring tasks"}
                },
                "required": ["task_id"]
            },
            handler=self.update_task_advanced
        )

        self.tools.register_tool(
            name="search_tasks_advanced",
            description="Search and filter tasks by advanced criteria like priority, tags, due dates",
            parameters={
                "type": "object",
                "properties": {
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"], "description": "Filter by priority"},
                    "tag": {"type": "string", "description": "Filter by tag"},
                    "due_date_from": {"type": "string", "format": "date-time", "description": "Filter tasks with due date after this"},
                    "due_date_to": {"type": "string", "format": "date-time", "description": "Filter tasks with due date before this"},
                    "status": {"type": "string", "enum": ["pending", "in-progress", "completed"], "description": "Filter by status"},
                    "search": {"type": "string", "description": "Full-text search in title and description"},
                    "sort_by": {"type": "string", "enum": ["created_at", "due_date", "priority", "title"], "description": "Field to sort by"},
                    "sort_order": {"type": "string", "enum": ["asc", "desc"], "description": "Sort order"},
                    "page": {"type": "integer", "description": "Page number for pagination"},
                    "limit": {"type": "integer", "description": "Number of items per page"}
                }
            },
            handler=self.search_tasks_advanced
        )

        self.tools.register_tool(
            name="create_recurring_task_template",
            description="Create a template for recurring tasks",
            parameters={
                "type": "object",
                "properties": {
                    "base_task_id": {"type": "string", "description": "ID of the base task to use as template"},
                    "recurrence_rule": {"type": "string", "description": "RRULE for recurrence pattern"},
                    "ends_on": {"type": "string", "format": "date-time", "description": "When recurrence should stop"},
                    "occurrence_count": {"type": "integer", "description": "Maximum number of occurrences"},
                    "user_id": {"type": "string", "description": "ID of the user creating the template"}
                },
                "required": ["base_task_id", "recurrence_rule", "user_id"]
            },
            handler=self.create_recurring_task_template
        )

        self.tools.register_tool(
            name="set_task_reminder",
            description="Set a reminder for a task based on due date",
            parameters={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task"},
                    "user_id": {"type": "string", "description": "ID of the user"},
                    "notification_method": {"type": "string", "enum": ["email", "push", "sms"], "description": "Method of notification"},
                    "user_id": {"type": "string", "description": "ID of the user setting the reminder"}
                },
                "required": ["task_id", "user_id"]
            },
            handler=self.set_task_reminder
        )

    async def create_advanced_task(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a task with advanced features"""
        try:
            # This would normally interact with the database
            # For this implementation, we'll return a mock response
            task_data = {
                "id": "mock-task-id-" + str(hash(json.dumps(params)) % 10000),
                "title": params.get("title"),
                "description": params.get("description", ""),
                "status": "pending",
                "priority": params.get("priority", "medium"),
                "due_date": params.get("due_date"),
                "tags": json.dumps(params.get("tags", [])),
                "recurrence_rule": params.get("recurrence_rule"),
                "user_id": params.get("user_id"),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            # In a real implementation, this would save to the database
            print(f"Created advanced task: {task_data}")

            # Publish task creation event
            await self.publish_task_event("created", task_data)

            return {
                "success": True,
                "task": task_data,
                "message": "Advanced task created successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create advanced task"
            }

    async def update_task_advanced(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update a task with advanced features"""
        try:
            # This would normally update the database
            # For this implementation, we'll return a mock response
            update_data = {k: v for k, v in params.items() if k != "task_id"}

            task_data = {
                "id": params.get("task_id"),
                "title": update_data.get("title"),
                "description": update_data.get("description"),
                "status": update_data.get("status", "pending"),
                "priority": update_data.get("priority", "medium"),
                "due_date": update_data.get("due_date"),
                "tags": json.dumps(update_data.get("tags", [])),
                "recurrence_rule": update_data.get("recurrence_rule"),
                "updated_at": datetime.now().isoformat()
            }

            # In a real implementation, this would update the database
            print(f"Updated advanced task: {task_data}")

            # Publish task update event
            await self.publish_task_event("updated", task_data)

            return {
                "success": True,
                "task": task_data,
                "message": "Advanced task updated successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update advanced task"
            }

    async def search_tasks_advanced(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Search and filter tasks by advanced criteria"""
        try:
            # This would normally query the database with filters
            # For this implementation, we'll return mock results
            query = TaskQuery(**{k: v for k, v in params.items() if v is not None})

            # Mock search results
            mock_tasks = [
                {
                    "id": "mock-search-result-1",
                    "title": "Sample Task",
                    "description": "This is a sample task for demonstration",
                    "status": "pending",
                    "priority": "high",
                    "due_date": "2026-03-15T10:00:00Z",
                    "tags": json.dumps(["work", "important"]),
                    "recurrence_rule": None,
                    "user_id": params.get("user_id", "mock-user"),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            ]

            return {
                "success": True,
                "tasks": mock_tasks,
                "total": len(mock_tasks),
                "filters_applied": params,
                "message": f"Found {len(mock_tasks)} tasks matching criteria"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tasks": [],
                "message": "Failed to search tasks"
            }

    async def create_recurring_task_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a template for recurring tasks"""
        try:
            # Validate recurrence parameters
            if not params.get("ends_on") and not params.get("occurrence_count"):
                return {
                    "success": False,
                    "error": "Either 'ends_on' or 'occurrence_count' must be specified to prevent infinite recurrence",
                    "message": "Invalid recurrence configuration"
                }

            template_data = {
                "id": "mock-template-id-" + str(hash(json.dumps(params)) % 10000),
                "base_task_id": params.get("base_task_id"),
                "recurrence_rule": params.get("recurrence_rule"),
                "ends_on": params.get("ends_on"),
                "occurrence_count": params.get("occurrence_count"),
                "user_id": params.get("user_id"),
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            # In a real implementation, this would save to the database
            print(f"Created recurring task template: {template_data}")

            return {
                "success": True,
                "template": template_data,
                "message": "Recurring task template created successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create recurring task template"
            }

    async def set_task_reminder(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Set a reminder for a task based on due date"""
        try:
            # Validate that the task has a due date
            # In a real implementation, we'd fetch the task to verify
            task_id = params.get("task_id")
            user_id = params.get("user_id")
            notification_method = params.get("notification_method", "push")

            # Calculate reminder time (e.g., 1 hour before due date)
            # This is a simplified calculation
            reminder_time = datetime.now().isoformat()  # In reality, this would be based on the task's due date

            reminder_data = {
                "id": "mock-reminder-id-" + str(hash(task_id + user_id) % 10000),
                "task_id": task_id,
                "user_id": user_id,
                "scheduled_time": reminder_time,
                "notification_method": notification_method,
                "is_sent": False,
                "created_at": datetime.now().isoformat()
            }

            # In a real implementation, this would save to the database
            print(f"Created task reminder: {reminder_data}")

            return {
                "success": True,
                "reminder": reminder_data,
                "message": "Task reminder set successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to set task reminder"
            }

    async def publish_task_event(self, event_type: str, task_data: Dict[str, Any]):
        """Publish a task event to the event system via Dapr"""
        try:
            # In a real implementation, this would use Dapr client to publish to Kafka
            event_payload = {
                "event_type": event_type,
                "task_data": task_data,
                "timestamp": datetime.now().isoformat(),
                "correlation_id": f"event-{hash(str(task_data)) % 10000}"
            }

            print(f"Publishing task event: {event_type} for task {task_data.get('id')}")

            # This would normally publish to Kafka via Dapr pub/sub
            # await self.client.publish_event(
            #     pubsub_name='kafka-pubsub',
            #     topic_name='task-events',
            #     data=json.dumps(event_payload)
            # )

        except Exception as e:
            print(f"Error publishing task event: {str(e)}")


# Global instance for use in the application
advanced_todo_tools = AdvancedTodoMCPTools()