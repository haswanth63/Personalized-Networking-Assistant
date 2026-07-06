"""
Testing API Routes with httpx TestClient
Integration tests for the complete request-response cycle

Following documentation: Testing API Routes with httpx TestClient
Validates request validation, service orchestration, and response serialization
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestAPIRoutes:
    """Test suite for API routes"""
    
    # ============ HEALTH ROUTES ============
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Welcome" in data["message"]
    
    # ============ EVENT ANALYZER ROUTE ============
    
    def test_analyze_event(self):
        """Test analyze event endpoint"""
        payload = {
            "description": "AI and Machine Learning Conference 2025"
        }
        response = client.post("/analyze-event", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "themes" in data
        assert isinstance(data["themes"], list)
        assert len(data["themes"]) > 0
    
    def test_analyze_event_empty_description(self):
        """Test analyze event with empty description (should return fallback)"""
        payload = {"description": ""}
        response = client.post("/analyze-event", json=payload)
        # Should still return something (fallback themes)
        assert response.status_code == 200
        data = response.json()
        assert "themes" in data
        assert len(data["themes"]) > 0
    
    # ============ CONVERSATION GENERATION ROUTE ============
    
    def test_generate_conversation(self):
        """Test conversation generation endpoint"""
        payload = {
            "event_description": "Tech Networking Event",
            "user_interests": ["AI", "Data Science"],
            "max_suggestions": 3
        }
        response = client.post("/generate-conversation", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "suggestions" in data
        assert isinstance(data["suggestions"], list)
        assert len(data["suggestions"]) > 0
        assert "extracted_themes" in data
    
    def test_generate_conversation_with_custom_max(self):
        """Test conversation generation with custom max suggestions"""
        payload = {
            "event_description": "Healthcare AI Conference",
            "user_interests": ["Machine Learning", "Healthcare"],
            "max_suggestions": 2
        }
        response = client.post("/generate-conversation", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert len(data["suggestions"]) <= 2
    
    def test_generate_conversation_missing_fields(self):
        """Test conversation generation with missing fields"""
        payload = {
            "event_description": "Test Event"
            # Missing user_interests
        }
        response = client.post("/generate-conversation", json=payload)
        # Should return 422 validation error
        assert response.status_code == 422
    
    # ============ FACT CHECK ROUTE ============
    
    def test_fact_check(self):
        """Test fact check endpoint"""
        payload = {"query": "Python programming language"}
        response = client.post("/fact-check", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "summary" in data
        assert "verified" in data
    
    def test_fact_check_empty_query(self):
        """Test fact check with empty query"""
        payload = {"query": ""}
        response = client.post("/fact-check", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["verified"] is False
    
    def test_fact_check_short_query(self):
        """Test fact check with very short query"""
        payload = {"query": "AI"}
        response = client.post("/fact-check", json=payload)
        assert response.status_code == 200
        data = response.json()
        # Should still work but might not be verified
        assert "summary" in data
    
    # ============ FEEDBACK ROUTE ============
    
    def test_submit_feedback_like(self):
        """Test submitting like feedback"""
        payload = {
            "suggestion": "This is a great conversation starter!",
            "action": "like"
        }
        response = client.post("/feedback", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_submit_feedback_dislike(self):
        """Test submitting dislike feedback"""
        payload = {
            "suggestion": "This suggestion could be better.",
            "action": "dislike"
        }
        response = client.post("/feedback", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_submit_feedback_invalid_action(self):
        """Test submitting feedback with invalid action"""
        payload = {
            "suggestion": "Test suggestion",
            "action": "invalid"
        }
        response = client.post("/feedback", json=payload)
        # Should return validation error
        assert response.status_code == 422
    
    # ============ HISTORY ROUTES ============
    
    def test_get_history(self):
        """Test getting conversation history"""
        response = client.get("/history")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "entries" in data
        assert isinstance(data["entries"], list)
    
    def test_get_history_with_pagination(self):
        """Test getting history with pagination"""
        response = client.get("/history?limit=5&offset=0")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 5
        assert data["offset"] == 0
    
    # ============ ADMIN ROUTES ============
    
    def test_admin_stats(self):
        """Test admin stats endpoint"""
        response = client.get("/admin/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_conversations" in data
        assert "total_feedback" in data
        assert "feedback_stats" in data
    
    def test_model_info(self):
        """Test model info endpoint"""
        response = client.get("/admin/models/info")
        assert response.status_code == 200
        data = response.json()
        assert "event_analyzer" in data
        assert "topic_generator" in data
    
    # ============ INVALID REQUESTS ============
    
    def test_invalid_endpoint(self):
        """Test invalid endpoint returns 404"""
        response = client.get("/invalid-endpoint")
        assert response.status_code == 404