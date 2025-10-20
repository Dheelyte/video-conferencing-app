"""
Pydantic schemas for JWT tokens.
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Token(BaseModel):
    """Schema for token response after login."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for decoded JWT token payload."""
    sub: Optional[str] = None
    exp: Optional[int] = None
    type: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request."""
    refresh_token: str