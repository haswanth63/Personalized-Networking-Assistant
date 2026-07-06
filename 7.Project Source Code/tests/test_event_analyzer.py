"""
Testing the Event Analyzer Service
Testing the DistilBERT classification pipeline

Following documentation: Testing the Event Analyzer Service
Tests validate structure, not specific model outputs (avoiding brittle tests)
"""

import pytest
from app.services import event_analyzer


class TestEventAnalyzer:
    """Test suite for event analyzer service"""
    
    def test_extract_themes_returns_list(self, sample_event_description):
        """Test that extract_event_themes returns a list"""
        themes = event_analyzer.extract_event_themes(sample_event_description)
        assert isinstance(themes, list)
    
    def test_extract_themes_returns_non_empty(self, sample_event_description):
        """Test that extract_event_themes returns at least one theme"""
        themes = event_analyzer.extract_event_themes(sample_event_description)
        assert len(themes) > 0
        assert isinstance(themes[0], str)
    
    def test_extract_themes_max_count(self, sample_event_description):
        """Test that extract_event_themes returns at most 3 themes"""
        themes = event_analyzer.extract_event_themes(sample_event_description)
        # The function returns top 3 themes by default
        assert len(themes) <= 3
    
    def test_extract_themes_with_empty_description(self):
        """Test that empty description returns default themes"""
        themes = event_analyzer.extract_event_themes("")
        assert isinstance(themes, list)
        assert len(themes) > 0
        # Should return a fallback theme
        assert themes[0] is not None
    
    def test_extract_themes_with_short_description(self):
        """Test that very short description still returns something"""
        themes = event_analyzer.extract_event_themes("AI")
        assert isinstance(themes, list)
        assert len(themes) > 0
    
    def test_extract_themes_with_custom_labels(self):
        """Test that custom labels work"""
        custom_labels = ["python", "java", "javascript"]
        themes = event_analyzer.extract_event_themes(
            "Learning Python programming language",
            custom_labels
        )
        assert isinstance(themes, list)
        # Should return at least one theme from custom labels
        assert len(themes) > 0
    
    def test_extract_themes_all_themes_are_strings(self, sample_event_description):
        """Test that all returned themes are strings"""
        themes = event_analyzer.extract_event_themes(sample_event_description)
        for theme in themes:
            assert isinstance(theme, str)
            assert len(theme) > 0
    
    def test_extract_themes_no_duplicates(self, sample_event_description):
        """Test that returned themes have no duplicates"""
        themes = event_analyzer.extract_event_themes(sample_event_description)
        unique_themes = set(themes)
        assert len(unique_themes) == len(themes)