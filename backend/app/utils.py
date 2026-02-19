import os
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple

from app.logger import get_logger
from app.config import settings
from app.exceptions import ImageProcessingError, FileUploadError

logger = get_logger(__name__)

def ensure_directories_exist():
    """Ensure upload and enhanced directories exist"""
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.enhanced_dir).mkdir(parents=True, exist_ok=True)
    logger.info(f"Directories ensured: {settings.upload_dir}, {settings.enhanced_dir}")

def validate_image_file(filename: str, size_bytes: int, mime_type: str) -> bool:
    """Validate image file"""
    max_size = settings.max_upload_size_mb * 1024 * 1024
    
    if size_bytes > max_size:
        raise FileUploadError(f"File size exceeds {settings.max_upload_size_mb}MB limit")
    
    allowed_mimes = ['image/jpeg', 'image/png', 'image/bmp', 'image/jpg']
    if mime_type not in allowed_mimes:
        raise FileUploadError(f"Unsupported file type: {mime_type}")
    
    return True

def process_fingerprint_image(image_path: str) -> Tuple[str, dict]:
    """
    Enhanced fingerprint image using Gabor filters
    
    Args:
        image_path: Path to input image
        
    Returns:
        Tuple of (output_path, enhancement_stats)
    """
    try:
        # Import here to avoid circular imports
        from fingerprint_enhancer.fingerprint_image_enhancer import FingerprintImageEnhancer
        
        logger.info(f"Starting image enhancement: {image_path}")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ImageProcessingError("Failed to read image file")
        
        original_height, original_width = img.shape[:2]
        
        # Convert to grayscale if necessary
        if len(img.shape) > 2:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Create enhancer and process
        enhancer = FingerprintImageEnhancer()
        enhancer.enhance(img, invert_output=True)
        
        # Generate output path
        filename = Path(image_path).stem
        output_path = os.path.join(
            settings.enhanced_dir,
            f"enhanced_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        
        # Save enhanced image
        enhancer.save_enhanced_image(output_path)
        
        # Get file statistics
        enhanced_size = os.path.getsize(output_path)
        original_size = os.path.getsize(image_path)
        
        stats = {
            "original_size": original_size,
            "enhanced_size": enhanced_size,
            "format": "JPEG",
            "dimensions": (original_width, original_height)
        }
        
        logger.info(f"Image enhancement completed: {output_path}")
        
        return output_path, stats
        
    except Exception as e:
        logger.error(f"Image processing error: {str(e)}", exc_info=True)
        raise ImageProcessingError(f"Image processing failed: {str(e)}")

def cleanup_old_files():
    """Remove files older than FILE_RETENTION_HOURS"""
    try:
        cutoff_time = datetime.now() - timedelta(hours=settings.file_retention_hours)
        
        for dir_path in [settings.upload_dir, settings.enhanced_dir]:
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        logger.debug(f"Deleted old file: {file_path}")
    except Exception as e:
        logger.warning(f"Error during file cleanup: {str(e)}")

def encode_image_to_base64(image_path: str) -> str:
    """Encode image to base64 string"""
    import base64
    
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()
        return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        logger.error(f"Error encoding image to base64: {str(e)}")
        raise ImageProcessingError("Failed to encode image")
