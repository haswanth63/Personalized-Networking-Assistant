"""
Event Analyzer Service - Theme Extraction using DistilBERT
Based on your documentation: Epic 2 - Event Analyzer Service
"""

from transformers import pipeline
from typing import List
from app.config import DEFAULT_THEMES

# Load model once at startup (intentional design for performance)
print("Loading DistilBERT zero-shot classifier...")
classifier = pipeline(
    "zero-shot-classification",
    model="typeform/distilbert-base-uncased-mnli"
)
print("✅ DistilBERT loaded successfully!")


def extract_event_themes(
    event_description: str,
    candidate_labels: List[str] = None
) -> List[str]:
    """
    Extract top themes from event description using zero-shot classification
    
    Args:
        event_description: The event description text
        candidate_labels: Optional list of themes to check against
    
    Returns:
        List of top 3 themes with highest scores
    """
    if candidate_labels is None:
        candidate_labels = DEFAULT_THEMES
    
    # Handle empty description
    if not event_description or len(event_description.strip()) < 10:
        return ["general networking", "professional development"]
    
    try:
        # Perform zero-shot classification
        result = classifier(
            event_description,
            candidate_labels=candidate_labels,
            multi_label=True
        )
        
        # Get top 3 themes with score > 0.2 threshold
        top_themes = []
        for label, score in zip(result['labels'][:3], result['scores'][:3]):
            if score > 0.2:
                top_themes.append(label)
        
        return top_themes if top_themes else ["general networking"]
        
    except Exception as e:
        print(f"⚠️ Theme extraction error: {e}")
        # Fallback: simple keyword matching
        return _keyword_extraction(event_description)


def _keyword_extraction(text: str) -> List[str]:
    """Fallback method: simple keyword-based extraction"""
    text_lower = text.lower()
    found_themes = []
    
    for theme in DEFAULT_THEMES:
        if theme in text_lower:
            found_themes.append(theme)
    
    return found_themes[:3] if found_themes else ["general networking"]