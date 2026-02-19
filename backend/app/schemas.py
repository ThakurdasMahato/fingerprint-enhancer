from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    success: bool
    message: str
    enhanced_image: Optional[str] = Field(None, description="Base64 encoded enhanced image")
    file_name: Optional[str] = Field(None, description="Enhanced file name")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")

class EnhancementStats(BaseModel):
    """Statistics about enhancement"""
    original_size: int
    enhanced_size: int
    format: str
    dimensions: tuple[int, int]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str

class ErrorResponse(BaseModel):
    """Error response model"""
    error_code: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

class ImageValidationRequest(BaseModel):
    """Request model for image validation"""
    filename: str
    size_bytes: int
    mime_type: str
    
    @validator('mime_type')
    def validate_mime_type(cls, v):
        allowed_types = ['image/jpeg', 'image/png', 'image/bmp', 'image/jpg']
        if v not in allowed_types:
            raise ValueError(f'Unsupported mime type: {v}')
        return v
