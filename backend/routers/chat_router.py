"""
Chat API Router for the Todo AI Chatbot
"""
from fastapi import APIRouter, HTTPException, status, Request
from typing import List, Optional
from uuid import UUID
from schemas.chat_schemas import ChatRequest, ChatResponse, ToolCall
from services.conversation_service import ConversationService
from services.db_message_service import DBMessageService
from services.tool_call_service import ToolCallService
from database.connection import get_session_context
from models.message import MessageRole
from auth.user_service import UserService
from agent.conversation_handler import ConversationHandler
from agent.todo_agent import TodoAgent
from datetime import datetime
import asyncio


router = APIRouter(tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(request: Request, user_id: str, chat_request: ChatRequest):
    """
    Chat endpoint for the Todo AI Chatbot.

    Accepts a natural language message from the user and returns the
    TodoAgent's response along with any tool calls that were made.
    """
    try:
        # DB preflight check
        try:
            from sqlalchemy import text
            with get_session_context() as session:
                session.execute(text("SELECT 1"))
        except Exception as db_error:
            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={"error": "db_unavailable", "message": "Database is currently unavailable"}
            )

        # Authentication intentionally bypassed for Hackathon Phase 3 chat endpoint
        # user_id from path is accepted as the acting user for stateless architecture
        auth_user = {"user_id": user_id}

        # Validate and enrich the request context with user identity
        # Using the user_id from path as the authenticated user
        context = {
            "user_id": user_id,
            "valid_user": True,
            "conversation_valid": True if chat_request.conversation_id is None else False,
            "user_info": {"user_id": user_id}
        }

        # Get or create conversation ID
        conversation_id = chat_request.conversation_id
        if not conversation_id:
            # Create a new conversation and get its ID within the session
            from database.connection import get_session_context
            from services.db_conversation_service import DBConversationService
            with get_session_context() as session:
                conversation = DBConversationService.create_conversation(session, user_id)
                conversation_id = str(conversation.id)
                session.refresh(conversation)  # Refresh to ensure attributes are loaded
        else:
            # Validate that the conversation belongs to the user
            conversation_service = ConversationService()
            conversation = await conversation_service.get_conversation_by_id(conversation_id, user_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or does not belong to user"
                )
            conversation_id = str(conversation.id) if hasattr(conversation, 'id') else conversation_id

        # Save the user's message to the database
        message_service = DBMessageService()

        # Create the user message
        with get_session_context() as session:
            user_message = message_service.create_message(
                session=session,
                user_id=user_id,
                conversation_id=UUID(conversation_id),
                role=MessageRole.USER,
                content=chat_request.message
            )

        # Initialize the agent and process the message
        agent = TodoAgent()
        await agent.initialize()

        # Get conversation history for context
        conversation_service = ConversationService()
        conversation_history = await conversation_service.get_conversation_history(conversation_id, user_id)

        # Process the message with the agent
        agent_result = await agent.process_request(
            user_message=chat_request.message,
            user_id=user_id,
            conversation_history=conversation_history
        )

        # Save the agent's response to the database
        with get_session_context() as session:
            agent_message = message_service.create_message(
                session=session,
                user_id=user_id,
                conversation_id=UUID(conversation_id),
                role=MessageRole.ASSISTANT,
                content=agent_result["response"]
            )

        # Log tool calls that were made
        if agent_result["tool_calls"]:
            await ToolCallService.log_multiple_tool_calls(
                user_id=user_id,
                conversation_id=conversation_id,
                tool_calls=agent_result["tool_calls"]
            )

        # Format tool calls for the response
        tool_calls = []
        for tool_call in agent_result["tool_calls"]:
            tool_calls.append(ToolCall(
                tool_name=tool_call.get("tool_name", ""),
                parameters=tool_call.get("parameters", {}),
                result=tool_call.get("result", {}),
                timestamp=datetime.utcnow()
            ))

        # Prepare the response
        response = ChatResponse(
            success=True,
            conversation_id=conversation_id,
            response=agent_result["response"],
            tool_calls=tool_calls,
            error=None
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        import logging
        logger = logging.getLogger("todo-api")
        logger.exception("Unhandled exception in chat endpoint: %s", e)
        # Handle any other exceptions - ensure conversation_id is a string or None converted to ""
        safe_conversation_id = chat_request.conversation_id or ""
        # Handle any other exceptions
        error_response = ChatResponse(
            success=False,
            conversation_id=safe_conversation_id,
            response="",
            tool_calls=[],
            error={
                "code": "INTERNAL_ERROR",
                "message": "An internal server error occurred"
            }
        )
        return error_response


@router.get("/test-db")
async def test_db_endpoint():
    """
    Test endpoint to check database connectivity.
    """
    try:
        from sqlalchemy import text
        from database.connection import get_session_context

        with get_session_context() as session:
            session.execute(text("SELECT 1"))

        return {"db": "ok"}
    except Exception as e:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500,
            content={"error": "db_unavailable", "message": "Database is currently unavailable"}
        )