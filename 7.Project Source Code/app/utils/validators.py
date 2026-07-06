"""
Custom Validators
Type-safe request validation for FastAPI
"""

from typing import List, Optional
from app.exceptions import ValidationException


def validate_event_description(description: str) -> bool:
    """
    Validate event description is not empty and has minimum length
    """
    if not description or len(description.strip()) < 10:
        raise ValidationException(
            "Event description must be at least 10 characters long"
        )
    return True


def validate_interests(interests: List[str]) -> bool:
    """
    Validate interests list
    """
    if not interests:
        raise ValidationException("Interests list cannot be empty")
    
    if any(len(interest.strip()) < 2 for interest in interests):
        raise ValidationException("Each interest must be at least 2 characters")
    
    return True


def validate_feedback_action(action: str) -> bool:
    """
    Validate feedback action
    """
    valid_actions = ["like", "dislike"]
    if action not in valid_actions:
        raise ValidationException(
            f"Feedback action must be one of: {', '.join(valid_actions)}"
        )
    return True


def validate_suggestion_text(text: str) -> bool:
    """
    Validate suggestion text for feedback
    """
    if not text or len(text.strip()) < 3:
        raise ValidationException("Suggestion text must be at least 3 characters")
    return True


def sanitize_input(text: str) -> str:
    """
    Sanitize user input
    Remove harmful characters
    """
    import re
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()