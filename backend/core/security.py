import logging
from typing import Optional
from urllib.parse import unquote

from core.config import settings
from db.database import get_db
from db.models.user import Session as DbSession
from fastapi import Cookie, Depends, HTTPException, Request, status
from schemas.user import AuthResponse
from sqlalchemy.orm import Session
from utils.crypto import sha256_hex

# Configure logger
logger = logging.getLogger(__name__)


def validate_origin(request: Request):
    """
    Validate the Origin header for CSRF protection.
    This mirrors what SvelteKit does on the frontend.
    """
    # Only validate non-GET requests
    if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
        origin = request.headers.get("origin")
        host = request.headers.get("host")

        # If no origin header or origin doesn't match allowed origins
        if not origin or (
            origin not in settings.CORS_ORIGINS and origin != f"http://{host}"
        ):
            logger.warning(f"CSRF check failed. Origin: {origin}, Host: {host}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="CSRF check failed"
            )


async def get_current_user(
    request: Request,
    auth_session: Optional[str] = Cookie(None, alias="auth-session"),
    db: Session = Depends(get_db),
) -> AuthResponse:
    """Verify session token and get current user"""
    # Validate Origin header for CSRF protection
    validate_origin(request)

    if not auth_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # URL-decode the cookie value to handle URL encoding
    try:
        auth_session = unquote(auth_session)
    except Exception as e:
        logger.error(f"Error decoding session token: {str(e)}")
        # Continue with the original token if decoding fails

    # Hash the session token to match how @oslojs/crypto/sha2 does it
    session_id = sha256_hex(auth_session)

    # Get session from database
    db_session = db.query(DbSession).filter(DbSession.id == session_id).first()
    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
        )

    # Check if session is expired
    if db_session.is_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired"
        )

    # Get user from database using relationship
    user = db_session.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return AuthResponse(user_id=user.id, username=user.username)


def invalidate_all_user_sessions(user_id: str, db: Session) -> int:
    """
    Invalidate all sessions for a user
    Note: In read-only mode, this is a stub that returns 0
    """
    # The frontend handles session management
    return 0
