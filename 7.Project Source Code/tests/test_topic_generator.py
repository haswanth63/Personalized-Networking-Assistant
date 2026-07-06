"""
Testing the Topic Generator Service
Testing GPT-2 conversation generation

Following documentation: Testing the Topic Generator Service
Tests validate structure and post-processing logic
"""

import pytest
from app.services import topic_generator


class TestTopicGenerator:
    """Test suite for topic generator service"""
    
    def test_generate_topics_returns_list(self, sample_themes, sample_interests):
        """Test that generate_topics returns a list"""
        suggestions = topic_generator.generate_topics(
            sample_themes,
            sample_interests
        )
        assert isinstance(suggestions, list)
    
    def test_generate_topics_returns_non_empty(self, sample_themes, sample_interests):
        """Test that generate_topics returns at least one suggestion"""
        suggestions = topic_generator.generate_topics(
            sample_themes,
            sample_interests
        )
        assert len(suggestions) > 0
    
    def test_generate_topics_all_suggestions_are_strings(self, sample_themes, sample_interests):
        """Test that all suggestions are strings"""
        suggestions = topic_generator.generate_topics(
            sample_themes,
            sample_interests
        )
        for suggestion in suggestions:
            assert isinstance(suggestion, str)
            assert len(suggestion) > 10  # Should be meaningful length
    
    def test_generate_topics_with_empty_themes(self, sample_interests):
        """Test that empty themes still generates suggestions"""
        suggestions = topic_generator.generate_topics(
            [],
            sample_interests
        )
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
    
    def test_generate_topics_with_empty_interests(self, sample_themes):
        """Test that empty interests still generates suggestions"""
        suggestions = topic_generator.generate_topics(
            sample_themes,
            []
        )
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
    
    def test_generate_topics_with_max_suggestions(self, sample_themes, sample_interests):
        """Test that max_suggestions parameter works"""
        max_count = 2
        suggestions = topic_generator.generate_topics(
            sample_themes,
            sample_interests,
            max_suggestions=max_count
        )
        # Should return at most max_count suggestions
        assert len(suggestions) <= max_count
    
    def test_generate_topics_no_duplicate_suggestions(self, sample_themes, sample_interests):
        """Test that generated suggestions are unique"""
        suggestions = topic_generator.generate_topics(
            sample_themes,
            sample_interests,
            max_suggestions=5
        )
        # Check for duplicates
        unique_suggestions = set(suggestions)
        assert len(unique_suggestions) == len(suggestions)
    
    def test_generate_topics_handles_special_characters(self):
        """Test that special characters are handled properly"""
        themes = ["AI & ML", "Healthcare (public)"]
        interests = ["data ethics", "patient safety"]
        suggestions = topic_generator.generate_topics(themes, interests)
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0