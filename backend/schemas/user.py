"""
Pydantic schemas for user-related data structures.

This module defines the data models for user entities, used for
request validation and response serialization.
"""

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base schema with common user fields."""
    username: str = Field(..., min_length=3, max_length=50,
                          description="Username between 3 and 50 characters")

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    """User response schema with ID."""
    id: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "user_123",
                "username": "johndoe"
            }
        }
    )


# Session schemas
class Session(BaseModel):
    """Session data schema."""
    id: str
    user_id: str
    expires_at: int  # Timestamp in milliseconds

    model_config = ConfigDict(from_attributes=True)


# Authentication response
class AuthResponse(BaseModel):
    """Schema for authentication response data."""
    user_id: str
    username: str
