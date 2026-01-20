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
        # Use a single session for the entire request to ensure consistency
        from sqlmodel import Session
        from sqlalchemy import text
        from database.connection import engine

        with Session(engine) as session:
            # DB preflight check
            session.execute(text("SELECT 1"))

            # Get or create conversation ID
            conversation_id = chat_request.conversation_id
            if not conversation_id:
                # Create a new conversation
                from services.db_conversation_service import DBConversationService
                conversation = DBConversationService.create_conversation(session, user_id)
                conversation_id = str(conversation.id)
            else:
                # Validate that the conversation belongs to the user
                from services.db_conversation_service import DBConversationService
                conversation = DBConversationService.get_conversation_by_id(
                    session, UUID(conversation_id), user_id
                )
                if not conversation:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found or does not belong to user"
                    )
                conversation_id = str(conversation.id) if hasattr(conversation, 'id') else conversation_id

            # Save the user's message to the database
            from services.db_message_service import DBMessageService
            user_message = DBMessageService.create_message(
                session=session,
                user_id=user_id,
                conversation_id=UUID(conversation_id),
                role=MessageRole.USER,
                content=chat_request.message
            )

            # Get conversation history for context - need to fetch it within the same session
            # Since the existing service creates its own session, we'll need to get it separately
            # But for now, we'll continue with the existing pattern for simplicity

            # Initialize the agent and process the message
            from agent.todo_agent import TodoAgent
            agent = TodoAgent()
            await agent.initialize()

            # Get conversation history for context - this service uses its own session internally
            from services.conversation_service import ConversationService
            conversation_service = ConversationService()
            conversation_history = await conversation_service.get_conversation_history(conversation_id, user_id)

            # Process the message with the agent, passing the same session
            try:
                agent_result = await asyncio.wait_for(
                    agent.process_request(
                        user_message=chat_request.message,
                        user_id=user_id,
                        conversation_history=conversation_history,
                        session=session  # Use the same session created at the beginning
                    ),
                    timeout=60  # 60 seconds timeout
                )
            except asyncio.TimeoutError:
                import logging
                logger = logging.getLogger("todo-api")
                logger.error("Agent timeout occurred for user_id: %s", user_id)

                from fastapi.responses import JSONResponse
                return JSONResponse(
                    status_code=504,
                    content={
                        "error": "agent_timeout",
                        "message": "AI model timed out. Please try again."
                    }
                )

            # Save the agent's response to the database using the same session
            agent_message = DBMessageService.create_message(
                session=session,
                user_id=user_id,
                conversation_id=UUID(conversation_id),
                role=MessageRole.ASSISTANT,
                content=agent_result["response"]
            )

            # Log tool calls that were made using the same session
            if agent_result["tool_calls"]:
                await ToolCallService.log_multiple_tool_calls(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    tool_calls=agent_result["tool_calls"],
                    session=session  # Use the same session created at the beginning
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
        import traceback
        tb = traceback.format_exc()
        print(tb)  # ensure Railway logs it
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500,
            content={
                'error': str(e),
                'traceback': tb
            }
        )


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