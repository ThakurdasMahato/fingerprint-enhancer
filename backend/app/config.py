from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    """Application settings from environment variables and .env file"""
    
    # Environment
    fastapi_env: str = Field(default="development", alias="FASTAPI_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Server
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=int(os.environ.get("PORT", 5000)), alias="API_PORT")
    
    # File Upload
    max_upload_size_mb: int = Field(default=50, alias="MAX_UPLOAD_SIZE_MB")
    upload_dir: str = Field(default="./uploads", alias="UPLOAD_DIR")
    enhanced_dir: str = Field(default="./enhanced", alias="ENHANCED_DIR")
    
    # CORS
    cors_origins: list[str] = Field(
        default=["http://localhost:3000", "https://fingerprint-enhancer-we.vercel.app"],
        alias="CORS_ORIGINS"
    )
    
    # API
    api_title: str = Field(default="Fingerprint Enhancer API", alias="API_TITLE")
    api_version: str = Field(default="1.0.0", alias="API_VERSION")
    api_description: str = Field(
        default="Advanced fingerprint image enhancement service",
        alias="API_DESCRIPTION"
    )
    
    # File Cleanup
    file_retention_hours: int = Field(default=24, alias="FILE_RETENTION_HOURS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def is_production(self) -> bool:
        return self.fastapi_env.lower() == "production"

# Global settings instance
settings = Settings()