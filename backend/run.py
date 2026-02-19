#!/usr/bin/env python
"""
FastAPI Application Entry Point
"""

import uvicorn
import os
from app.config import settings

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.api_port))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )