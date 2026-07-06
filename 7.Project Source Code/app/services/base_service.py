"""
Base Service Class
Following the Single Responsibility Principle
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Abstract base class for all services
    Ensures consistent interface and logging
    """
    
    def __init__(self):
        self.service_name = self.__class__.__name__
    
    @abstractmethod
    def process(self, *args, **kwargs) -> Any:
        """Main processing method - implemented by subclasses"""
        pass
    
    def log_start(self, **kwargs):
        """Log service start"""
        logger.debug(f"🔵 {self.service_name} started with {kwargs}")
    
    def log_success(self, result: Any):
        """Log successful completion"""
        logger.debug(f"✅ {self.service_name} completed successfully")
        return result
    
    def log_error(self, error: Exception):
        """Log error"""
        logger.error(f"❌ {self.service_name} failed: {str(error)}")
        return None
    
    def handle_error(self, error: Exception, default_return: Any = None) -> Any:
        """Handle errors gracefully"""
        self.log_error(error)
        return default_return