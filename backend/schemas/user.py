from pydantic import BaseModel


# User schemas
class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: str

    class Config:
        from_attributes = True


# Session schemas
class Session(BaseModel):
    id: str
    user_id: str
    expires_at: int  # Timestamp in milliseconds

    class Config:
        from_attributes = True


# Authentication response
class AuthResponse(BaseModel):
    user_id: str
    username: str
