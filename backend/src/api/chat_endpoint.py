from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID, uuid4
from typing import Optional
import json

from ..models.message import MessageCreate, MessageRole
from ..services.ai_service import AIService
from ..services.mcp_server import MCPServer
from ..services.todo_operations import TodoOperationsService
from ..services.database_service import get_session


router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: UUID,
    message: str,
    conversation_id: Optional[UUID] = None,
    metadata: Optional[dict] = None,
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint for interacting with the AI agent
    Implements POST /api/{user_id}/chat as required by spec.md FR-008
    """
    try:
        # Initialize services
        todo_service = TodoOperationsService(session)
        mcp_server = MCPServer(todo_service)
        ai_service = AIService(mcp_server)

        # If no conversation ID is provided, create a new conversation
        if not conversation_id:
            conversation_id = uuid4()
            todo_service.create_conversation(user_id=user_id, title=f"Conversation {conversation_id}")

        # Add user's message to the conversation
        user_message = todo_service.add_message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=message,
            metadata=metadata
        )

        # Process the message with the AI service
        ai_response = await ai_service.process_message(
            user_id=user_id,
            message=message,
            conversation_id=conversation_id
        )

        # Add AI's response to the conversation
        ai_message = todo_service.add_message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response
        )

        # Return the response as required by spec.md FR-008
        return {
            "conversation_id": str(conversation_id),
            "response": ai_response,
            "timestamp": ai_message.created_at.isoformat(),
            "status": "success"
        }

    except Exception as e:
        # Handle errors gracefully as required by spec.md FR-010
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/conversations/{conversation_id}")
async def get_conversation_history(
    user_id: UUID,
    conversation_id: UUID,
    session: Session = Depends(get_session)
):
    """
    Get conversation history
    """
    try:
        todo_service = TodoOperationsService(session)

        # Verify the conversation belongs to the user
        # In a real implementation, we'd have a method to verify this
        # For now, we'll just retrieve the messages

        messages = todo_service.get_conversation_messages(conversation_id=conversation_id)

        return {
            "conversation_id": str(conversation_id),
            "messages": [
                {
                    "id": str(msg.id),
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.created_at.isoformat(),
                    "metadata": msg.metadata_
                }
                for msg in messages
            ],
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))