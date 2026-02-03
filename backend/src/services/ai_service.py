from typing import Dict, Any, Optional
from uuid import UUID
import openai
from pydantic import BaseModel
from .mcp_server import MCPServer
from .todo_operations import TodoOperationsService


class AIRequest(BaseModel):
    user_id: UUID
    message: str
    conversation_id: Optional[UUID] = None


class AIService:
    """
    AI Service using OpenAI Agents SDK
    Implements the agent definition, tool binding, and intent interpretation
    """

    def __init__(self, mcp_server: MCPServer):
        self.mcp_server = mcp_server
        self.client = openai.OpenAI()

        # Define the tools that the agent can use
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "title": {"type": "string", "description": "The task title"},
                            "description": {"type": "string", "description": "The task description"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List all tasks for a user, optionally filtered by status",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user's ID"},
                            "status_filter": {"type": "string", "description": "Filter by status (active, completed)"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The task ID"},
                            "title": {"type": "string", "description": "The new task title"},
                            "description": {"type": "string", "description": "The new task description"},
                            "status": {"type": "string", "description": "The new status (active, completed)"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The task ID to complete"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "string", "description": "The task ID to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    async def process_message(self, user_id: UUID, message: str, conversation_id: Optional[UUID] = None) -> str:
        """
        Process a user message using the AI agent and return a response
        """
        try:
            # Create a chat completion with function calling
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",  # Using a model that supports function calling
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful todo management assistant. "
                            "Interpret the user's natural language request and call the appropriate function. "
                            "If the user wants to add a task, call add_task. "
                            "If the user wants to list tasks, call list_tasks. "
                            "If the user wants to update a task, call update_task. "
                            "If the user wants to complete a task, call complete_task. "
                            "If the user wants to delete a task, call delete_task. "
                            "Always respond in a friendly, helpful tone."
                        )
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                tools=self.tools,
                tool_choice="auto"
            )

            # Check if the model wanted to call a function
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Process the tool calls
                tool_responses = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = eval(tool_call.function.arguments)

                    # Convert string IDs to UUIDs where needed
                    if 'user_id' in function_args:
                        function_args['user_id'] = UUID(function_args['user_id'])
                    if 'task_id' in function_args:
                        function_args['task_id'] = UUID(function_args['task_id'])

                    # Execute the tool
                    tool_response = await self.mcp_server.execute_tool(function_name, function_args)
                    tool_responses.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(tool_response)
                    })

                # Get the final response from the model based on tool results
                final_response = self.client.chat.completions.create(
                    model="gpt-4-turbo-preview",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful todo management assistant. "
                                "Provide a clear, friendly response to the user based on the results of the tools you called. "
                                "Summarize what was done and confirm the action to the user."
                            )
                        },
                        {
                            "role": "user",
                            "content": message
                        },
                        response_message,
                    ] + tool_responses
                )

                return final_response.choices[0].message.content
            else:
                # If no tool was called, return the model's response directly
                return response_message.content or "I'm not sure how to help with that. Could you rephrase your request?"

        except Exception as e:
            # Return a user-friendly error message
            return f"I encountered an error processing your request: {str(e)}. Please try again."

    def interpret_intent(self, message: str) -> Dict[str, Any]:
        """
        Simple intent interpretation to determine what action the user wants to perform
        """
        message_lower = message.lower()

        # Simple heuristics for intent detection
        if any(word in message_lower for word in ['add', 'create', 'make', 'new']):
            return {"intent": "add_task", "confidence": 0.8}
        elif any(word in message_lower for word in ['list', 'show', 'view', 'get', 'see']):
            return {"intent": "list_tasks", "confidence": 0.8}
        elif any(word in message_lower for word in ['update', 'change', 'modify', 'edit']):
            return {"intent": "update_task", "confidence": 0.8}
        elif any(word in message_lower for word in ['complete', 'done', 'finish', 'mark']):
            return {"intent": "complete_task", "confidence": 0.8}
        elif any(word in message_lower for word in ['delete', 'remove', 'cancel']):
            return {"intent": "delete_task", "confidence": 0.8}
        else:
            return {"intent": "unknown", "confidence": 0.5}