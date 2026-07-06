"""
History Logger Service - Persistent Conversation Storage
Based on your documentation: Epic 2 - History Logger Service
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import uuid

from app.config import HISTORY_FILE


def log_conversation(data: Dict) -> str:
    """
    Save a conversation to history
    
    Args:
        data: Conversation data (event, themes, suggestions)
    
    Returns:
        History entry ID
    """
    # Add timestamp and unique ID
    entry_id = str(uuid.uuid4())[:8]
    entry = {
        "id": entry_id,
        **data,
        "timestamp": datetime.now().isoformat()
    }
    
    # Load existing history
    history = load_history()
    
    # Append new entry
    history.append(entry)
    
    # Save back to file
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return entry_id
    except Exception as e:
        print(f"⚠️ Error saving history: {e}")
        return entry_id


def load_history() -> List[Dict]:
    """
    Load all conversation history
    
    Returns:
        List of history entries
    """
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return []
    return []


def get_history_entry(entry_id: str) -> Optional[Dict]:
    """Get a single history entry by ID"""
    history = load_history()
    for entry in history:
        if entry.get("id") == entry_id:
            return entry
    return None


def clear_history() -> bool:
    """Clear all history"""
    try:
        if HISTORY_FILE.exists():
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
        return True
    except Exception:
        return False