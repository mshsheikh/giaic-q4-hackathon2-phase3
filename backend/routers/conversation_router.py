"""
Conversation Management API Router
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query, Request
from typing import List, Optional
from uuid import UUID
from backend.services.conversation_management_service import ConversationManagementService
from backend.services.db_conversation_service import DBConversationService
from backend.services.db_message_service import DBMessageService
from backend.database.connection import get_session_context
from backend.schemas.conversation_management_schemas import (
    ConversationCreateRequest,
    ConversationCreateResponse,
    ConversationListResponse,
    ConversationGetResponse,
    ConversationUpdateRequest,
    ConversationUpdateResponse,
    ConversationDeleteResponse
)
from backend.auth.user_service import UserService
from backend.logging.config import log_with_context
from backend.middleware.correlation_id_middleware import get_correlation_id
from backend.services.circuit_breaker import circuit_breaker
import logging


router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationCreateResponse)
async def create_conversation(
    request: ConversationCreateRequest,
    current_user: dict = Depends(UserService.get_current_user)
):
    """
    Create a new conversation for the authenticated user
    """
    correlation_id = get_correlation_id(request)

    logger = logging.getLogger()
    log_data = log_with_context(
        request=request,
        correlation_id=correlation_id,
        user_id=current_user.get("user_id"),
        operation="create_conversation"
    )
    logger.info("Creating new conversation", extra=log_data)

    try:
        service = ConversationManagementService()

        # Use circuit breaker for the operation
        @circuit_breaker("create_conversation")
        def create_operation():
            with get_session_context() as session:
                return service.create_conversation(
                    session=session,
                    user_id=current_user.get("user_id"),
                    name=request.name,
                    description=request.description
                )

        result = create_operation()

        return ConversationCreateResponse(
            success=True,
            conversation=result,
            error=None
        )
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}", extra=log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating conversation: {str(e)}"
        )


@router.get("/", response_model=ConversationListResponse)
async def list_user_conversations(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    current_user: dict = Depends(UserService.get_current_user)
):
    """
    List all conversations for the authenticated user
    """
    correlation_id = get_correlation_id(request)

    logger = logging.getLogger()
    log_data = log_with_context(
        correlation_id=correlation_id,
        user_id=current_user.get("user_id"),
        operation="list_conversations",
        skip=skip,
        limit=limit
    )
    logger.info("Listing user conversations", extra=log_data)

    try:
        service = ConversationManagementService()

        # Use circuit breaker for the operation
        @circuit_breaker("list_conversations")
        def list_operation():
            with get_session_context() as session:
                return service.get_user_conversations(
                    session=session,
                    user_id=current_user.get("user_id"),
                    skip=skip,
                    limit=limit
                )

        conversations, total_count = list_operation()

        return ConversationListResponse(
            success=True,
            conversations=conversations,
            total_count=total_count,
            skip=skip,
            limit=limit,
            error=None
        )
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}", extra=log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing conversations: {str(e)}"
        )


@router.get("/{conversation_id}", response_model=ConversationGetResponse)
async def get_conversation(
    request: Request,
    conversation_id: str,
    current_user: dict = Depends(UserService.get_current_user)
):
    """
    Get a specific conversation by ID
    """
    correlation_id = get_correlation_id(request)

    logger = logging.getLogger()
    log_data = log_with_context(
        correlation_id=correlation_id,
        user_id=current_user.get("user_id"),
        conversation_id=conversation_id,
        operation="get_conversation"
    )
    logger.info("Getting conversation", extra=log_data)

    try:
        service = ConversationManagementService()

        # Use circuit breaker for the operation
        @circuit_breaker("get_conversation")
        def get_operation():
            with get_session_context() as session:
                conversation = service.get_conversation_by_id(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=current_user.get("user_id")
                )

                if not conversation:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found or does not belong to user"
                    )

                # Also get conversation messages
                messages = service.get_conversation_messages(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=current_user.get("user_id")
                )

                return conversation, messages

        conversation, messages = get_operation()

        return ConversationGetResponse(
            success=True,
            conversation=conversation,
            messages=messages,
            error=None
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}", extra=log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting conversation: {str(e)}"
        )


@router.put("/{conversation_id}", response_model=ConversationUpdateResponse)
async def update_conversation(
    conversation_id: str,
    request: ConversationUpdateRequest,
    current_user: dict = Depends(UserService.get_current_user)
):
    """
    Update a specific conversation by ID
    """
    correlation_id = get_correlation_id(request)

    logger = logging.getLogger()
    log_data = log_with_context(
        request=request,
        correlation_id=correlation_id,
        user_id=current_user.get("user_id"),
        conversation_id=conversation_id,
        operation="update_conversation"
    )
    logger.info("Updating conversation", extra=log_data)

    try:
        service = ConversationManagementService()

        # Use circuit breaker for the operation
        @circuit_breaker("update_conversation")
        def update_operation():
            with get_session_context() as session:
                return service.update_conversation(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=current_user.get("user_id"),
                    name=request.name,
                    description=request.description
                )

        result = update_operation()

        return ConversationUpdateResponse(
            success=True,
            conversation=result,
            error=None
        )
    except Exception as e:
        logger.error(f"Error updating conversation: {str(e)}", extra=log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating conversation: {str(e)}"
        )


@router.delete("/{conversation_id}", response_model=ConversationDeleteResponse)
async def delete_conversation(
    request: Request,
    conversation_id: str,
    current_user: dict = Depends(UserService.get_current_user)
):
    """
    Delete a specific conversation by ID
    """
    correlation_id = get_correlation_id(request)

    logger = logging.getLogger()
    log_data = log_with_context(
        correlation_id=correlation_id,
        user_id=current_user.get("user_id"),
        conversation_id=conversation_id,
        operation="delete_conversation"
    )
    logger.info("Deleting conversation", extra=log_data)

    try:
        service = ConversationManagementService()

        # Use circuit breaker for the operation
        @circuit_breaker("delete_conversation")
        def delete_operation():
            with get_session_context() as session:
                return service.delete_conversation(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=current_user.get("user_id")
                )

        success = delete_operation()

        return ConversationDeleteResponse(
            success=success,
            error=None
        )
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}", extra=log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )


@router.post("/{conversation_id}/reset", response_model=ConversationGetResponse)
async def reset_conversation(
    request: Request,
    conversation_id: str,
    current_user: dict = Depends(UserService.get_current_user)
):
    """
    Reset a conversation by clearing all messages while keeping the conversation
    """
    correlation_id = get_correlation_id(request)

    logger = logging.getLogger()
    log_data = log_with_context(
        correlation_id=correlation_id,
        user_id=current_user.get("user_id"),
        conversation_id=conversation_id,
        operation="reset_conversation"
    )
    logger.info("Resetting conversation", extra=log_data)

    try:
        service = ConversationManagementService()

        # Use circuit breaker for the operation
        @circuit_breaker("reset_conversation")
        def reset_operation():
            with get_session_context() as session:
                # First verify the conversation belongs to the user
                conversation = service.get_conversation_by_id(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=current_user.get("user_id")
                )

                if not conversation:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Conversation not found or does not belong to user"
                    )

                # Clear all messages in the conversation
                service.clear_conversation_messages(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=current_user.get("user_id")
                )

                # Return the conversation with no messages
                return conversation, []

        conversation, messages = reset_operation()

        return ConversationGetResponse(
            success=True,
            conversation=conversation,
            messages=messages,
            error=None
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error resetting conversation: {str(e)}", extra=log_data)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error resetting conversation: {str(e)}"
        )