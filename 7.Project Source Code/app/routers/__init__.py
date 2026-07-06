"""
Routers Package
Hub-and-spoke routing architecture
"""

from app.routers import conversation
from app.routers import health
from app.routers import admin

__all__ = [
    'conversation',
    'health',
    'admin'
]