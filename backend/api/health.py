from typing import Optional

from core.security import get_current_user
from fastapi import APIRouter, Cookie, Depends, Request, Response
from schemas.user import AuthResponse

router = APIRouter()


@router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "version": "0.1.0"}


@router.get("/session/refresh")
async def refresh_session(
    request: Request,
    response: Response,
    auth_session: Optional[str] = Cookie(None, alias="auth-session"),
    user: AuthResponse = Depends(get_current_user),
):
    """
    Endpoint to refresh the session cookie.
    The frontend is responsible for updating the session in the database.
    This endpoint just ensures the cookie is still valid and returns the user.
    """
    # The mere fact that this endpoint returns successfully means
    # the session is valid (get_current_user dependency validates it)
    return {
        "status": "ok",
        "user": {"user_id": user.user_id, "username": user.username},
    }
