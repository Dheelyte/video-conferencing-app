"""
Configuration management using Pydantic Settings.
All environment variables are loaded from .env file.
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings.
    
    Uses Pydantic's BaseSettings to automatically load environment variables.
    This ensures type safety and validation of configuration values.
    """
    # API Settings
    PROJECT_NAME: str = "FastAPI JWT Auth"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security Settings
    SECRET_KEY: str  # REQUIRED: Must be set in .env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7     # 7 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # @field_validator("BACKEND_CORS_ORIGINS")
    # def assemble_cors_origins(cls, v):
    #     """Parse CORS origins from string or list."""
    #     if isinstance(v, str):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, list):
    #         return v
    #     raise ValueError(v)
    
    # First superuser (for database initialization)
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_FULL_NAME: str = "Admin User"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


# Create global settings instance
settings = Settings()