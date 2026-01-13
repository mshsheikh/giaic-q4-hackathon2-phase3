"""
Authentication Router for the Todo AI Chatbot
"""
from fastapi import APIRouter, Request, Response, HTTPException, status
from fastapi.responses import JSONResponse
from auth.logout_handler import logout_handler
from auth.middleware import auth_middleware
from auth.session_manager import session_manager
from typing import Dict, Any


router = APIRouter(tags=["auth"])


@router.post("/logout")
async def logout_endpoint(request: Request, response: Response) -> Dict[str, Any]:
    """
    Logout endpoint to end the user's session.
    """
    try:
        # Get the current user's token to revoke
        user = await auth_middleware.get_current_user(request)
        token_to_revoke = None

        # Get token from either header or cookie
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token_to_revoke = auth_header.split(" ")[1]
        else:
            token_to_revoke = request.cookies.get(auth_middleware.config.AUTH_COOKIE_NAME)

        # Perform logout
        result = logout_handler.logout_user(response=response, token=token_to_revoke)

        return result

    except Exception as e:
        # Handle any errors during logout
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": f"Error during logout: {str(e)}"
            }
        )
        return response


@router.get("/session-status")
async def session_status(request: Request) -> Dict[str, Any]:
    """
    Check the status of the current user session.
    """
    try:
        user = await auth_middleware.get_current_user(request)

        if user:
            return {
                "authenticated": True,
                "user": {
                    "user_id": user.get("user_id"),
                    "email": user.get("email"),
                    "name": user.get("name")
                },
                "expires_at": user.get("exp")
            }
        else:
            return {
                "authenticated": False,
                "message": "No active session"
            }

    except Exception as e:
        return {
            "authenticated": False,
            "error": str(e)
        }


@router.post("/refresh-session")
async def refresh_session(request: Request, response: Response) -> Dict[str, Any]:
    """
    Refresh the user's session token if it's close to expiration.
    """
    try:
        # Get the current token from request
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            current_token = auth_header.split(" ")[1]
        else:
            current_token = request.cookies.get(auth_middleware.config.AUTH_COOKIE_NAME)

        if not current_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No token provided"
            )

        # Try to refresh the token
        new_token = session_manager.refresh_session_token(current_token)

        if new_token and new_token != current_token:
            # Set the new token in the response
            response.set_cookie(
                key=auth_middleware.config.AUTH_COOKIE_NAME,
                value=new_token,
                httponly=True,
                secure=auth_middleware.config.SECURE_COOKIES,
                samesite="lax"
            )

            return {
                "success": True,
                "message": "Session refreshed successfully",
                "token_refreshed": True
            }
        else:
            return {
                "success": True,
                "message": "Session is still valid, no refresh needed",
                "token_refreshed": False
            }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error refreshing session: {str(e)}"
        }