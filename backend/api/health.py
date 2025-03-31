"""
Health check and session endpoints.

This module provides endpoints for system health checking and
session management functionality.
"""
import logging
from typing import Any

from core.security import get_current_user
from fastapi import APIRouter, Cookie, Depends, Request, Response
from schemas.user import AuthResponse

# Configure logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, Any]:
    """
    Simple health check endpoint.

    Returns:
        Dictionary with status information
    """
    logger.debug("Health check requested")
    return {"status": "ok", "version": "0.1.0"}


@router.get("/session/refresh")
async def refresh_session(
    request: Request,
    response: Response,
    auth_session: str | None = Cookie(None, alias="auth-session"),
    user: AuthResponse = Depends(get_current_user),
) -> dict[str, Any]:
    """
    Endpoint to refresh the session cookie.

    The frontend is responsible for updating the session in the database.
    This endpoint just ensures the cookie is still valid and returns the user.

    Args:
        request: The request object
        response: The response object
        auth_session: The session cookie
        user: The authenticated user

    Returns:
        Dictionary with status and user information
    """
    logger.info(f"Session refresh for user {user.user_id}")

    # The mere fact that this endpoint returns successfully means
    # the session is valid (get_current_user dependency validates it)
    return {
        "status": "ok",
        "user": {"user_id": user.user_id, "username": user.username},
    }
