"""
Custom Exception Classes
Clean error handling for the application
"""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base exception for application"""
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(AppException):
    """Resource not found"""
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            detail=f"{resource} with id '{identifier}' not found",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ValidationException(AppException):
    """Validation error"""
    def __init__(self, detail: str):
        super().__init__(
            detail=detail,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class ServiceUnavailableException(AppException):
    """External service unavailable"""
    def __init__(self, service: str):
        super().__init__(
            detail=f"{service} service is temporarily unavailable",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class RateLimitException(AppException):
    """Rate limit exceeded"""
    def __init__(self):
        super().__init__(
            detail="Rate limit exceeded. Please try again later.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )