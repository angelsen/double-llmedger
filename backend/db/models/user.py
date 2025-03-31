"""
User and session models for authentication.

These models match the schema used by the frontend Lucia auth system,
providing a compatible data layer for authentication services.
"""
from datetime import datetime, timedelta

from db.database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    """User model matching the schema used by Lucia auth."""
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    sessions: Mapped[list["Session"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Session(Base):
    """Session model matching the schema used by Lucia auth."""
    __tablename__ = "session"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("user.id"), nullable=False)
    # Store as Integer timestamp to match Drizzle schema
    expires_at: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationship to user
    user: Mapped[User] = relationship("User", back_populates="sessions")

    @property
    def expires_at_datetime(self) -> datetime:
        """Convert timestamp to datetime object."""
        # The SQLite timestamp is stored as seconds since epoch by Drizzle ORM
        try:
            return datetime.fromtimestamp(self.expires_at)  # Already in seconds
        except (ValueError, TypeError) as e:
            # If the conversion fails, log the error and return a far future date
            # to prevent sessions from being marked as expired incorrectly
            print(f"Error converting timestamp {self.expires_at}: {e}")
            return datetime.now() + timedelta(days=30)

    @property
    def is_expired(self) -> bool:
        """Check if session is expired."""
        try:
            now = datetime.now()
            return now > self.expires_at_datetime
        except Exception as e:
            # If there's any error in comparison, log it and consider the session valid
            print(f"Error checking session expiration: {e}")
            return False
