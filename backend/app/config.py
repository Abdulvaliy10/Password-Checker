from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./english_learning.db"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS settings
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"]
    
    # App settings
    APP_NAME: str = "English Learning API"
    APP_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()