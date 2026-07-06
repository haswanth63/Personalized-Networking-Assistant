"""
Custom Middleware
Cross-cutting concerns: logging, timing, error handling
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs request details and response time
    """
    
    async def dispatch(self, request: Request, call_next):
        # Start timer
        start_time = time.time()
        
        # Log request
        logger.info(f"→ {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(f"← {request.method} {request.url.path} → {response.status_code} ({duration:.2f}s)")
        
        # Add timing header
        response.headers["X-Response-Time"] = f"{duration:.2f}s"
        
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Adds Request ID to every request for tracing
    """
    
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            import uuid
            request_id = str(uuid.uuid4())[:8]
        
        # Add to request state
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handler for uncaught exceptions
    """
    
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return Response(
                content=f'{{"error": "Internal server error", "request_id": "{getattr(request.state, "request_id", "unknown")}"}}',
                status_code=500,
                media_type="application/json"
            )