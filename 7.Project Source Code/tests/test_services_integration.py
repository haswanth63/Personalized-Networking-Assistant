"""
Integration Tests
Testing services together
"""

import pytest
from app.services import event_analyzer, topic_generator, fact_checker
from app.services import history_logger, feedback_logger


class TestServicesIntegration:
    """Test services working together"""
    
    def test_full_pipeline(self):
        """Test the full pipeline: analyze -> generate -> log"""
        # Step 1: Analyze event
        event_desc = "AI and Machine Learning Conference for Healthcare"
        themes = event_analyzer.extract_event_themes(event_desc)
        assert isinstance(themes, list)
        assert len(themes) > 0
        
        # Step 2: Generate topics
        interests = ["data science", "patient safety"]
        suggestions = topic_generator.generate_topics(themes, interests)
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # Step 3: Log to history
        history_id = history_logger.log_conversation({
            "event_description": event_desc,
            "themes": themes,
            "suggestions": suggestions,
            "user_interests": interests
        })
        assert history_id is not None
        
        # Step 4: Log feedback
        feedback_entry = feedback_logger.log_feedback(
            suggestion=suggestions[0],
            action="like"
        )
        assert feedback_entry is not None
        assert feedback_entry.get("feedback") == "like"
    
    def test_fact_check_with_generated_content(self):
        """Test fact checking generated content"""
        # Generate some content
        themes = ["artificial intelligence"]
        interests = ["machine learning"]
        suggestions = topic_generator.generate_topics(themes, interests)
        
        if suggestions:
            # Fact check one suggestion
            first_suggestion = suggestions[0]
            # Extract a key phrase (simplified)
            key_phrase = "AI" if "AI" in first_suggestion else "machine learning"
            result = fact_checker.fact_check(key_phrase)
            assert isinstance(result, dict)
            assert "summary" in result