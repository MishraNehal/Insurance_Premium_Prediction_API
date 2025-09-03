import os
from typing import List

class Settings:
    """Application settings and configuration"""
    
    # API Settings
    API_TITLE: str = "Insurance Premium Prediction API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A FastAPI application that predicts insurance premium categories"
    
    # Server Settings
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Security Settings
    ALLOWED_HOSTS: List[str] = ["*"]  # Configure appropriately for production
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Model Settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "model/model.pkl")
    MODEL_VERSION: str = os.getenv("MODEL_VERSION", "1.0.0")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

# Create settings instance
settings = Settings()

