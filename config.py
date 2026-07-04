"""
Application Configuration
Centralized configuration management
"""

import os
from pathlib import Path
from typing import List, Optional

# Try to import pydantic-settings, fallback to simple settings if not available
try:
    from pydantic_settings import BaseSettings
    USE_PYDANTIC = True
except ImportError:
    USE_PYDANTIC = False
    print("⚠️ pydantic-settings not found, using fallback configuration")


if USE_PYDANTIC:
    class Settings(BaseSettings):
        """Application settings using Pydantic"""
        
        APP_TITLE: str = "Personalized Networking Assistant"
        APP_VERSION: str = "1.0.0"
        APP_DESCRIPTION: str = "AI-powered networking assistant"
        DEBUG: bool = True
        HOST: str = "0.0.0.0"
        PORT: int = 8000
        RELOAD: bool = True
        ALLOWED_ORIGINS: List[str] = ["*"]
        ALLOWED_METHODS: List[str] = ["*"]
        ALLOWED_HEADERS: List[str] = ["*"]
        BASE_DIR: Path = Path(__file__).parent.parent
        DATA_DIR: Path = BASE_DIR / "data"
        
        # DEFAULT_THEMES must be defined here
        DEFAULT_THEMES: List[str] = [
            "artificial intelligence", "machine learning", "data science",
            "healthcare", "blockchain", "cloud computing", "cybersecurity",
            "education", "sustainability", "entrepreneurship", "fintech",
            "digital marketing", "web development", "product management"
        ]
        
        MAX_GENERATION_LENGTH: int = 80
        TEMPERATURE: float = 0.85
        TOP_P: float = 0.9
        WIKIPEDIA_USER_AGENT: str = "PersonalizedNetworkingAssistant/1.0"
        WIKIPEDIA_TIMEOUT: int = 10
        RATE_LIMIT_REQUESTS: int = 100
        RATE_LIMIT_PERIOD: int = 60
        LOG_LEVEL: str = "INFO"
        LOG_FILE: Optional[Path] = None
        
        class Config:
            env_file = ".env"
            env_file_encoding = "utf-8"
    
    settings = Settings()

else:
    # Fallback simple settings (no pydantic)
    class Settings:
        APP_TITLE = "Personalized Networking Assistant"
        APP_VERSION = "1.0.0"
        APP_DESCRIPTION = "AI-powered networking assistant"
        DEBUG = True
        HOST = "0.0.0.0"
        PORT = 8000
        RELOAD = True
        ALLOWED_ORIGINS = ["*"]
        ALLOWED_METHODS = ["*"]
        ALLOWED_HEADERS = ["*"]
        BASE_DIR = Path(__file__).parent.parent
        DATA_DIR = BASE_DIR / "data"
        
        # DEFAULT_THEMES defined here
        DEFAULT_THEMES = [
            "artificial intelligence", "machine learning", "data science",
            "healthcare", "blockchain", "cloud computing", "cybersecurity",
            "education", "sustainability", "entrepreneurship", "fintech",
            "digital marketing", "web development", "product management"
        ]
        
        MAX_GENERATION_LENGTH = 80
        TEMPERATURE = 0.85
        TOP_P = 0.9
        WIKIPEDIA_USER_AGENT = "PersonalizedNetworkingAssistant/1.0"
        WIKIPEDIA_TIMEOUT = 10
        RATE_LIMIT_REQUESTS = 100
        RATE_LIMIT_PERIOD = 60
        LOG_LEVEL = "INFO"
        LOG_FILE = None
    
    settings = Settings()


# Ensure data directory exists
settings.DATA_DIR.mkdir(exist_ok=True)

# Set file paths
HISTORY_FILE = settings.DATA_DIR / "history.json"
FEEDBACK_FILE = settings.DATA_DIR / "feedback.json"

# Export constants for easy import
DEFAULT_THEMES = settings.DEFAULT_THEMES
MAX_GENERATION_LENGTH = settings.MAX_GENERATION_LENGTH
TEMPERATURE = settings.TEMPERATURE
TOP_P = settings.TOP_P
WIKIPEDIA_USER_AGENT = settings.WIKIPEDIA_USER_AGENT
WIKIPEDIA_TIMEOUT = settings.WIKIPEDIA_TIMEOUT