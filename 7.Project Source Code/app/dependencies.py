"""
Dependency Injection
Following the Service Layer Design Principles - explicit dependencies
"""

from fastapi import Request, HTTPException
from typing import Optional

from app.services import (
    event_analyzer,
    topic_generator,
    fact_checker,
    history_logger,
    feedback_logger
)
from app.exceptions import RateLimitException


# ============ SERVICE DEPENDENCIES ============

def get_event_analyzer():
    """Get event analyzer service instance"""
    return event_analyzer


def get_topic_generator():
    """Get topic generator service instance"""
    return topic_generator


def get_fact_checker():
    """Get fact checker service instance"""
    return fact_checker


def get_history_logger():
    """Get history logger service instance"""
    return history_logger


def get_feedback_logger():
    """Get feedback logger service instance"""
    return feedback_logger


# ============ RATE LIMITING DEPENDENCY ============

# Simple in-memory rate limiting (for demonstration)
# In production, use Redis or similar
_rate_limit_store = {}


def check_rate_limit(request: Request):
    """
    Rate limiting dependency
    Simple implementation - can be enhanced with Redis
    """
    client_ip = request.client.host if request.client else "unknown"
    request_count = _rate_limit_store.get(client_ip, 0)
    
    if request_count > 100:  # 100 requests limit
        raise RateLimitException()
    
    _rate_limit_store[client_ip] = request_count + 1
    return True


# ============ REQUEST ID DEPENDENCY ============

def get_request_id(request: Request) -> str:
    """Get or generate request ID for tracing"""
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        import uuid
        request_id = str(uuid.uuid4())[:8]
    return request_id


# ============ AUTH DEPENDENCY (Future) ============

async def get_current_user(request: Request) -> Optional[dict]:
    """
    Authentication dependency (placeholder for future)
    Currently returns None for public access
    """
    # Future: Validate JWT token
    return None