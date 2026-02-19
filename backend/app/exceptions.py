from fastapi import HTTPException, status
from typing import Any, Dict

class APIException(HTTPException):
    """Base API Exception"""
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str = "An error occurred",
        error_code: str = "UNKNOWN_ERROR"
    ):
        self.error_code = error_code
        self.detail = detail
        
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": detail
            }
        )

class ValidationError(APIException):
    """Validation error"""
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )

class FileUploadError(APIException):
    """File upload error"""
    def __init__(self, detail: str = "File upload failed"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="FILE_UPLOAD_ERROR"
        )

class ImageProcessingError(APIException):
    """Image processing error"""
    def __init__(self, detail: str = "Image processing failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="IMAGE_PROCESSING_ERROR"
        )

class NotFoundError(APIException):
    """Resource not found error"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND"
        )
