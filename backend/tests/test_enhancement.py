"""
Enhancement endpoint tests
"""

import pytest
from unittest.mock import patch, MagicMock


def test_enhance_image_successful(client, sample_image_file):
    """Test successful image enhancement"""
    filename, file_io, content_type = sample_image_file
    
    response = client.post(
        "/api/enhance",
        files={"file": (filename, file_io, content_type)}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "enhanced_image" in data
    assert "file_name" in data
    assert "processing_time_ms" in data


def test_enhance_missing_file(client):
    """Test enhancement without file"""
    response = client.post("/api/enhance")
    
    assert response.status_code == 422  # Validation error


def test_enhance_invalid_file_type(client):
    """Test enhancement with invalid file type"""
    response = client.post(
        "/api/enhance",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    
    assert response.status_code == 400


def test_download_enhanced_image(client):
    """Test downloading enhanced image"""
    # This would need a real enhanced image file to test properly
    response = client.get("/api/download/nonexistent.jpg")
    
    assert response.status_code == 400  # File not found error


def test_download_path_traversal_protection(client):
    """Test that path traversal attacks are prevented"""
    response = client.get("/api/download/../../etc/passwd")
    
    assert response.status_code == 400  # Should be blocked
