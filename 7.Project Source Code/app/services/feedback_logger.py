"""
Feedback Logger Service - User Feedback Collection
Based on your documentation: Epic 2 - Feedback Logger Service
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

from app.config import FEEDBACK_FILE


def log_feedback(suggestion: str, action: str) -> Dict:
    """
    Save user feedback for a suggestion
    
    Args:
        suggestion: The suggestion text
        action: 'like' or 'dislike'
    
    Returns:
        The feedback entry
    """
    entry = {
        "suggestion": suggestion,
        "feedback": action,
        "timestamp": datetime.now().isoformat()
    }
    
    # Load existing feedback
    feedback_data = load_feedback()
    
    # Append new entry
    feedback_data.append(entry)
    
    # Save back to file
    try:
        with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
            json.dump(feedback_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Error saving feedback: {e}")
    
    return entry


def load_feedback() -> List[Dict]:
    """
    Load all feedback entries
    
    Returns:
        List of feedback entries
    """
    if FEEDBACK_FILE.exists():
        try:
            with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return []
    return []


def get_feedback_stats() -> Dict:
    """
    Get feedback statistics
    
    Returns:
        Dict with like/dislike counts and total
    """
    feedback = load_feedback()
    likes = sum(1 for f in feedback if f.get("feedback") == "like")
    dislikes = sum(1 for f in feedback if f.get("feedback") == "dislike")
    
    return {
        "total": len(feedback),
        "likes": likes,
        "dislikes": dislikes,
        "like_rate": likes / len(feedback) if feedback else 0
    }


def clear_feedback() -> bool:
    """Clear all feedback"""
    try:
        if FEEDBACK_FILE.exists():
            with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        return True
    except Exception:
        return False