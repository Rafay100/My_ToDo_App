import asyncio
from typing import Dict, Any, List
from uuid import UUID
from pydantic import BaseModel
from .todo_operations import TodoOperationsService
from ..models.task import Task


class AddTaskRequest(BaseModel):
    user_id: UUID
    title: str
    description: str = None


class ListTasksRequest(BaseModel):
    user_id: UUID
    status_filter: str = None


class UpdateTaskRequest(BaseModel):
    task_id: UUID
    title: str = None
    description: str = None
    status: str = None


class CompleteTaskRequest(BaseModel):
    task_id: UUID


class DeleteTaskRequest(BaseModel):
    task_id: UUID


class MCPServer:
    """
    MCP Server implementation for todo operations
    Following the requirements from spec.md FR-004
    """

    def __init__(self, todo_service: TodoOperationsService):
        self.todo_service = todo_service
        self.tools = {
            "add_task": self.add_task,
            "list_tasks": self.list_tasks,
            "update_task": self.update_task,
            "complete_task": self.complete_task,
            "delete_task": self.delete_task,
        }

    async def add_task(self, request: AddTaskRequest) -> Dict[str, Any]:
        """Implement add_task tool following spec.md FR-004"""
        try:
            task = self.todo_service.add_task(
                user_id=request.user_id,
                title=request.title,
                description=request.description
            )

            return {
                "task_id": str(task.id),
                "status": "created",
                "message": f"Task '{task.title}' has been created successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add task: {str(e)}"
            }

    async def list_tasks(self, request: ListTasksRequest) -> Dict[str, Any]:
        """Implement list_tasks tool following spec.md FR-004"""
        try:
            tasks = self.todo_service.list_tasks(
                user_id=request.user_id,
                status_filter=request.status_filter
            )

            task_list = []
            for task in tasks:
                task_list.append({
                    "id": str(task.id),
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "created_at": task.created_at.isoformat()
                })

            return {
                "tasks": task_list,
                "status": "success",
                "message": f"Retrieved {len(tasks)} tasks"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list tasks: {str(e)}"
            }

    async def update_task(self, request: UpdateTaskRequest) -> Dict[str, Any]:
        """Implement update_task tool following spec.md FR-004"""
        try:
            from ..models.task import TaskUpdate
            updates = TaskUpdate(
                title=request.title,
                description=request.description,
                status=request.status
            )

            task = self.todo_service.update_task(
                task_id=request.task_id,
                updates=updates
            )

            if not task:
                return {
                    "status": "error",
                    "message": f"Task with ID {request.task_id} not found"
                }

            return {
                "task_id": str(task.id),
                "status": "updated",
                "message": f"Task '{task.title}' has been updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}"
            }

    async def complete_task(self, request: CompleteTaskRequest) -> Dict[str, Any]:
        """Implement complete_task tool following spec.md FR-004"""
        try:
            task = self.todo_service.complete_task(task_id=request.task_id)

            if not task:
                return {
                    "status": "error",
                    "message": f"Task with ID {request.task_id} not found"
                }

            return {
                "task_id": str(task.id),
                "status": "completed",
                "message": f"Task '{task.title}' has been marked as completed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to complete task: {str(e)}"
            }

    async def delete_task(self, request: DeleteTaskRequest) -> Dict[str, Any]:
        """Implement delete_task tool following spec.md FR-004"""
        try:
            success = self.todo_service.delete_task(task_id=request.task_id)

            if not success:
                return {
                    "status": "error",
                    "message": f"Task with ID {request.task_id} not found"
                }

            return {
                "task_id": str(request.task_id),
                "status": "deleted",
                "message": "Task has been deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}"
            }

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool with given parameters"""
        if tool_name not in self.tools:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}"
            }

        tool_func = self.tools[tool_name]

        # Create appropriate request object based on tool name
        if tool_name == "add_task":
            request_obj = AddTaskRequest(**params)
        elif tool_name == "list_tasks":
            request_obj = ListTasksRequest(**params)
        elif tool_name == "update_task":
            request_obj = UpdateTaskRequest(**params)
        elif tool_name == "complete_task":
            request_obj = CompleteTaskRequest(**params)
        elif tool_name == "delete_task":
            request_obj = DeleteTaskRequest(**params)
        else:
            return {
                "status": "error",
                "message": f"Unknown tool: {tool_name}"
            }

        # Execute the tool
        return await tool_func(request_obj)