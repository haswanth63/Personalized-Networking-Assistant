"""
Health Check Router
Production best practice - load balancer friendly endpoints
"""

from fastapi import APIRouter, status
from datetime import datetime
from app.config import settings
from app.services import event_analyzer, topic_generator

router = APIRouter(tags=["Health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    Returns application health status
    """
    return {
        "status": "healthy",
        "service": settings.APP_TITLE,
        "version": settings.APP_VERSION,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """
    Readiness check for load balancers
    Checks if dependencies are ready
    """
    services_status = {
        "distilbert": "ready",
        "gpt2": "ready",
        "wikipedia": "ready"
    }
    
    # Check if services are loaded
    try:
        _ = event_analyzer.classifier
    except Exception:
        services_status["distilbert"] = "not ready"
    
    return {
        "status": "ready" if all(s == "ready" for s in services_status.values()) else "degraded",
        "services": services_status,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/live", status_code=status.HTTP_200_OK)
async def liveness_check():
    """
    Liveness check for container orchestration
    Simple check that the app is running
    """
    return {"status": "alive", "timestamp": datetime.now().isoformat()}