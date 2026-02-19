"""
Health check endpoint tests
"""

import pytest
from datetime import datetime


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] is not None


def test_status_endpoint(client):
    """Test status endpoint"""
    response = client.get("/status")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "environment" in data
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test root endpoint"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
