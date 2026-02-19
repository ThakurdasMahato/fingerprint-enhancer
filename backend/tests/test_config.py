"""
Configuration and utility tests
"""

import pytest
from app.config import settings
from app.exceptions import ValidationError, FileUploadError


def test_settings_load():
    """Test that settings load correctly"""
    assert settings.api_title is not None
    assert settings.api_version is not None
    assert settings.max_upload_size_mb > 0


def test_custom_exceptions():
    """Test custom exception classes"""
    
    # Test ValidationError
    exc = ValidationError("Test validation")
    assert exc.status_code == 422
    assert exc.error_code == "VALIDATION_ERROR"
    
    # Test FileUploadError
    exc = FileUploadError("Test upload")
    assert exc.status_code == 400
    assert exc.error_code == "FILE_UPLOAD_ERROR"


def test_is_production_check():
    """Test production environment check"""
    # In test environment, should be development
    assert settings.is_production is False
