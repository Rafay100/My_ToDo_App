"""
Official MCP Server implementation using the MCP SDK
Following the requirements from spec.md FR-004
"""
import asyncio
from typing import Dict, Any, List, Optional
from uuid import UUID
from pydantic import BaseModel
from mcp.server import Server
from mcp.types import Tool, ToolCallFinishedResult, TextContent, Diagnostic
import json

from .todo_operations import TodoOperationsService


class MCPOfficialServer:
    """
    MCP Server implementation using the official MCP SDK
    """

    def __init__(self, todo_service: TodoOperationsService):
        self.todo_service = todo_service
        self.server = Server("todo-mcp-server")

        # Register tools
        self._register_tools()

    def _register_tools(self):
        """Register MCP tools with the server"""

        @self.server.tool("add_task")
        async def add_task_handler(arguments: Dict[str, Any]) -> List[TextContent]:
            """Add a new task to the user's todo list"""
            try:
                user_id = UUID(arguments.get("user_id"))
                title = arguments.get("title", "")
                description = arguments.get("description", "")

                if not title:
                    return [TextContent(
                        type="text",
                        text="Error: Missing required parameter 'title'"
                    )]

                task = self.todo_service.add_task(
                    user_id=user_id,
                    title=title,
                    description=description
                )

                return [TextContent(
                    type="text",
                    text=f"Task '{task.title}' has been created successfully with ID: {task.id}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error adding task: {str(e)}"
                )]

        @self.server.tool("list_tasks")
        async def list_tasks_handler(arguments: Dict[str, Any]) -> List[TextContent]:
            """List tasks for a user, optionally filtered by status"""
            try:
                user_id = UUID(arguments.get("user_id"))

                status_filter = arguments.get("status_filter")

                tasks = self.todo_service.list_tasks(
                    user_id=user_id,
                    status_filter=status_filter
                )

                if not tasks:
                    return [TextContent(
                        type="text",
                        text="No tasks found for this user."
                    )]

                task_list = "\n".join([
                    f"- {task.title} ({task.status.value}) - ID: {task.id}"
                    for task in tasks
                ])

                return [TextContent(
                    type="text",
                    text=f"Found {len(tasks)} tasks:\n{task_list}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error listing tasks: {str(e)}"
                )]

        @self.server.tool("update_task")
        async def update_task_handler(arguments: Dict[str, Any]) -> List[TextContent]:
            """Update an existing task"""
            try:
                from ..models.task import TaskUpdate

                task_id = UUID(arguments.get("task_id"))

                # Build update object
                update_data = {}
                if "title" in arguments:
                    update_data["title"] = arguments["title"]
                if "description" in arguments:
                    update_data["description"] = arguments["description"]
                if "status" in arguments:
                    update_data["status"] = arguments["status"]

                updates = TaskUpdate(**update_data)

                task = self.todo_service.update_task(
                    task_id=task_id,
                    updates=updates
                )

                if not task:
                    return [TextContent(
                        type="text",
                        text=f"Error: Task with ID {task_id} not found"
                    )]

                return [TextContent(
                    type="text",
                    text=f"Task '{task.title}' has been updated successfully"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error updating task: {str(e)}"
                )]

        @self.server.tool("complete_task")
        async def complete_task_handler(arguments: Dict[str, Any]) -> List[TextContent]:
            """Mark a task as completed"""
            try:
                task_id = UUID(arguments.get("task_id"))

                task = self.todo_service.complete_task(task_id=task_id)

                if not task:
                    return [TextContent(
                        type="text",
                        text=f"Error: Task with ID {task_id} not found"
                    )]

                return [TextContent(
                    type="text",
                    text=f"Task '{task.title}' has been marked as completed"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error completing task: {str(e)}"
                )]

        @self.server.tool("delete_task")
        async def delete_task_handler(arguments: Dict[str, Any]) -> List[TextContent]:
            """Delete a task"""
            try:
                task_id = UUID(arguments.get("task_id"))

                success = self.todo_service.delete_task(task_id=task_id)

                if not success:
                    return [TextContent(
                        type="text",
                        text=f"Error: Task with ID {task_id} not found"
                    )]

                return [TextContent(
                    type="text",
                    text="Task has been deleted successfully"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error deleting task: {str(e)}"
                )]

    async def run(self, host: str = "localhost", port: int = 8080):
        """Start the MCP server"""
        from mcp.server.stdio import stdio_server

        async with stdio_server(self.server) as make_socket:
            await make_socket()