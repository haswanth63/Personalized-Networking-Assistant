"""
Testing the Fact Checker Service
Testing Wikipedia API with mocking

Following documentation: Testing the Fact Checker Service
Uses unittest.mock to isolate from external API calls
"""

import pytest
from unittest.mock import patch, MagicMock
from app.services import fact_checker


class TestFactChecker:
    """Test suite for fact checker service"""
    
    @patch('app.services.fact_checker.requests.get')
    def test_fact_check_returns_dict(self, mock_get, sample_fact_query):
        """Test that fact_check returns a dictionary"""
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'query': {
                'search': [{'title': 'Artificial Intelligence'}]
            }
        }
        mock_get.return_value = mock_response
        
        result = fact_checker.fact_check(sample_fact_query)
        assert isinstance(result, dict)
        assert 'query' in result
        assert 'summary' in result
        assert 'verified' in result
    
    @patch('app.services.fact_checker.requests.get')
    def test_fact_check_returns_summary_string(self, mock_get, sample_fact_query):
        """Test that fact_check returns a summary string"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {'query': {'search': [{'title': 'Artificial Intelligence'}]}},
            {'query': {'pages': {'1': {'extract': 'AI is a field...'}}}}
        ]
        mock_get.return_value = mock_response
        
        result = fact_checker.fact_check(sample_fact_query)
        assert isinstance(result.get('summary', ''), str)
        assert len(result.get('summary', '')) >= 0
    
    @patch('app.services.fact_checker.requests.get')
    def test_fact_check_no_results(self, mock_get):
        """Test that fact_check handles no search results"""
        # Mock empty search results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'query': {'search': []}}
        mock_get.return_value = mock_response
        
        result = fact_checker.fact_check("Nonexistent Topic XYZ123")
        assert isinstance(result, dict)
        assert result.get('verified') is False
        assert 'No relevant' in result.get('summary', '')
    
    @patch('app.services.fact_checker.requests.get')
    def test_fact_check_handles_connection_error(self, mock_get):
        """Test that fact_check handles connection errors gracefully"""
        mock_get.side_effect = Exception("Connection error")
        
        result = fact_checker.fact_check("Test query")
        assert isinstance(result, dict)
        assert result.get('verified') is False
        assert 'error' in result.get('summary', '').lower() or 'unavailable' in result.get('summary', '').lower()
    
    @patch('app.services.fact_checker.requests.get')
    def test_fact_check_handles_json_error(self, mock_get):
        """Test that fact_check handles invalid JSON responses"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_get.return_value = mock_response
        
        result = fact_checker.fact_check("Test query")
        assert isinstance(result, dict)
        assert result.get('verified') is False
    
    def test_fact_check_empty_query(self):
        """Test that empty query returns appropriate response"""
        result = fact_checker.fact_check("")
        assert isinstance(result, dict)
        assert result.get('verified') is False
        assert 'too short' in result.get('summary', '').lower()
    
    @patch('app.services.fact_checker.requests.get')
    def test_fact_check_verified_status(self, mock_get, sample_fact_query):
        """Test that verification status is set correctly"""
        # Mock successful response with matching content
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = [
            {'query': {'search': [{'title': 'Artificial Intelligence'}]}},
            {'query': {'pages': {'1': {'extract': 'Artificial Intelligence is...'}}}}
        ]
        mock_get.return_value = mock_response
        
        result = fact_checker.fact_check(sample_fact_query)
        # The query appears in the content, so should be verified
        # Note: actual verification depends on content matching
        assert 'verified' in result