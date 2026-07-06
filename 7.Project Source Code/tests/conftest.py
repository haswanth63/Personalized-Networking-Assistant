"""
pytest configuration and fixtures
Following the Testing Philosophy: setup test environment
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app


# ============ FIXTURES ============

@pytest.fixture
def client():
    """
    FastAPI TestClient fixture
    Allows testing API routes without running the server
    """
    return TestClient(app)


@pytest.fixture
def sample_event_description():
    """Sample event description for testing"""
    return "AI and Machine Learning Conference focusing on healthcare applications"


@pytest.fixture
def sample_user_interests():
    """Sample user interests for testing"""
    return ["artificial intelligence", "data science", "healthcare"]


@pytest.fixture
def sample_fact_query():
    """Sample fact query for testing"""
    return "Artificial Intelligence was first introduced in 1956"


@pytest.fixture
def sample_themes():
    """Sample themes for topic generation testing"""
    return ["AI", "healthcare", "data science"]


@pytest.fixture
def sample_interests():
    """Sample interests for topic generation testing"""
    return ["ethics", "machine learning", "innovation"]