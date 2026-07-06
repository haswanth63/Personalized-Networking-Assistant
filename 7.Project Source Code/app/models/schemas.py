from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# ============ REQUEST MODELS ============

class EventInput(BaseModel):
    """Input for event theme analysis"""
    description: str
    custom_themes: Optional[List[str]] = None


class UserInterests(BaseModel):
    """User interests for conversation generation"""
    interests: List[str]
    event_description: str


class ConversationRequest(BaseModel):
    """Full conversation generation request"""
    event_description: str
    user_interests: List[str]
    max_suggestions: Optional[int] = 3


class FactCheckRequest(BaseModel):
    """Fact check request"""
    query: str


class FeedbackRequest(BaseModel):
    """User feedback request"""
    suggestion: str
    action: str  # "like" or "dislike"


# ============ RESPONSE MODELS ============

class ThemeResponse(BaseModel):
    """Theme extraction response"""
    themes: List[str]
    event_description: str


class FactCheckResponse(BaseModel):
    """Fact check response"""
    query: str
    summary: str
    verified: bool
    source_url: Optional[str] = None


class ConversationResponse(BaseModel):
    """Full conversation generation response"""
    event_description: str
    extracted_themes: List[str]
    suggestions: List[str]
    history_id: Optional[str] = None


class HistoryEntry(BaseModel):
    """History entry model"""
    id: str
    event_description: str
    themes: List[str]
    suggestions: List[str]
    timestamp: str


class FeedbackEntry(BaseModel):
    """Feedback entry model"""
    suggestion: str
    feedback: str
    timestamp: str