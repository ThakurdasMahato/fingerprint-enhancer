from fastapi import APIRouter
from datetime import datetime

from app.logger import get_logger
from app.config import settings
from app.schemas import HealthResponse

router = APIRouter(tags=["Health"])
logger = get_logger(__name__)

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check requested")
    return HealthResponse(
        status="healthy",
        version=settings.api_version
    )

@router.get("/status")
async def status():
    """Get API status"""
    return {
        "status": "running",
        "environment": settings.fastapi_env,
        "debug": settings.debug,
        "timestamp": datetime.utcnow().isoformat()
    }
