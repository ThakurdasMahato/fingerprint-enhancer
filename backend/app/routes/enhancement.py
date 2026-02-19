from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse
import time
import os
import uuid
from pathlib import Path

from app.logger import get_logger
from app.schemas import FileUploadResponse, EnhancementStats
from app.exceptions import FileUploadError, ImageProcessingError
from app.utils import (
    validate_image_file,
    process_fingerprint_image,
    encode_image_to_base64,
    cleanup_old_files
)
from app.config import settings

router = APIRouter(prefix="/api", tags=["Enhancement"])
logger = get_logger(__name__)

@router.post("/enhance", response_model=FileUploadResponse)
async def enhance_fingerprint(file: UploadFile = File(...)):
    """
    Enhance a fingerprint image using Gabor filters
    
    - **file**: Image file (JPEG, PNG, BMP)
    - Returns: Enhanced image as base64 string
    """
    start_time = time.time()
    temp_file_path = None
    enhanced_file_path = None
    
    try:
        # Validate file
        if not file.filename:
            raise FileUploadError("Filename is missing")
        
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Validate
        validate_image_file(file.filename, file_size, file.content_type)
        
        logger.info(f"Processing file: {file.filename}, size: {file_size} bytes")
        
        # Save temporary file
        temp_dir = Path(settings.upload_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)
        temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
        temp_file_path = temp_dir / temp_filename
        
        with open(temp_file_path, "wb") as f:
            f.write(contents)
        
        # Process image
        enhanced_file_path, stats = process_fingerprint_image(str(temp_file_path))
        
        # Encode to base64
        enhanced_image_base64 = encode_image_to_base64(enhanced_file_path)
        
        # Clean up old files periodically
        cleanup_old_files()
        
        processing_time = (time.time() - start_time) * 1000  # Convert to ms
        
        logger.info(f"Enhancement completed in {processing_time:.2f}ms")
        
        # Return response
        return FileUploadResponse(
            success=True,
            message="Image enhanced successfully",
            enhanced_image=f"data:image/jpeg;base64,{enhanced_image_base64}",
            file_name=Path(enhanced_file_path).name,
            processing_time_ms=processing_time
        )
        
    except FileUploadError as e:
        logger.warning(f"File upload validation error: {str(e)}")
        raise
    except ImageProcessingError as e:
        logger.error(f"Image processing error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during enhancement: {str(e)}", exc_info=True)
        raise ImageProcessingError(f"Unexpected error: {str(e)}")
    finally:
        # Cleanup temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file: {str(e)}")

@router.get("/download/{filename}")
async def download_enhanced_image(filename: str):
    """Download enhanced image"""
    try:
        file_path = os.path.join(settings.enhanced_dir, filename)
        
        # Security check: ensure file is in enhanced directory
        if not os.path.abspath(file_path).startswith(os.path.abspath(settings.enhanced_dir)):
            logger.warning(f"Attempted path traversal: {filename}")
            raise FileUploadError("Invalid file path")
        
        if not os.path.exists(file_path):
            raise FileUploadError("File not found")
        
        logger.info(f"Downloading file: {filename}")
        
        return FileResponse(
            path=file_path,
            media_type="image/jpeg",
            filename=filename
        )
        
    except FileUploadError:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise ImageProcessingError("Failed to download file")
