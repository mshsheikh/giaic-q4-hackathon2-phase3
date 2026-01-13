"""
User Service for handling user identity and authentication
"""
from typing import Dict, Any, Optional
from auth.middleware import auth_middleware
from fastapi import Request, HTTPException, status
from models.user import User  # We'll need to create this model
from database.connection import get_session_context
from services.db_conversation_service import DBConversationService
from services.db_message_service import DBMessageService
from services.db_task_service import DBTaskService


class UserService:
    """
    Service class for handling user identity propagation and authentication
    """

    @staticmethod
    async def get_current_user(request: Request) -> Optional[Dict[str, Any]]:
        """
        Get the current authenticated user from the request.

        Args:
            request: FastAPI request object

        Returns:
            User information dictionary if authenticated, None otherwise
        """
        return await auth_middleware.get_current_user(request)

    @staticmethod
    async def authenticate_user(request: Request) -> Dict[str, Any]:
        """
        Authenticate the user from the request and return user information.

        Args:
            request: FastAPI request object

        Returns:
            User information dictionary

        Raises:
            HTTPException: If authentication fails
        """
        user = await auth_middleware.get_current_user(request)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )

        return user

    @staticmethod
    async def validate_user_owns_resource(user: Dict[str, Any], resource_user_id: str) -> bool:
        """
        Validate that the authenticated user owns a specific resource.

        Args:
            user: User information dictionary
            resource_user_id: ID of the user who owns the resource

        Returns:
            True if user has access, False otherwise
        """
        return auth_middleware.validate_user_access(user, resource_user_id)

    @staticmethod
    async def propagate_user_identity_to_db_operations(user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a context for database operations that ensures user identity is propagated.

        Args:
            user_id: ID of the authenticated user
            conversation_id: Optional conversation ID to validate ownership

        Returns:
            Context dictionary with user information and validation results
        """
        context = {
            "user_id": user_id,
            "valid_user": True,
            "conversation_valid": True if conversation_id is None else False
        }

        # If a conversation ID is provided, validate that the user owns it
        if conversation_id:
            with get_session_context() as session:
                conversation = DBConversationService.get_conversation_by_id(
                    session=session,
                    conversation_id=conversation_id,
                    user_id=user_id
                )
                context["conversation_valid"] = conversation is not None

        return context

    @staticmethod
    async def validate_and_enrich_request_context(request: Request, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate the request context and enrich it with user information.

        Args:
            request: FastAPI request object
            conversation_id: Optional conversation ID to validate ownership

        Returns:
            Context dictionary with user information and validation results
        """
        # Authenticate the user
        user = await UserService.authenticate_user(request)
        user_id = user.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID in token"
            )

        # Propagate user identity to database operations
        context = await UserService.propagate_user_identity_to_db_operations(
            user_id=user_id,
            conversation_id=conversation_id
        )

        # Add user information to the context
        context["user_info"] = user

        return context