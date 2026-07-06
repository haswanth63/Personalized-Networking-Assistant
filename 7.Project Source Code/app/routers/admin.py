"""
Admin Router
Admin-only endpoints for monitoring and management
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from app.services import history_logger, feedback_logger
from app.services import event_analyzer, topic_generator

router = APIRouter(tags=["Admin"], prefix="/admin")


@router.get("/stats", response_model=Dict[str, Any])
async def get_stats():
    """Get application statistics"""
    history = history_logger.load_history()
    feedback = feedback_logger.load_feedback()
    feedback_stats = feedback_logger.get_feedback_stats()
    
    return {
        "total_conversations": len(history),
        "total_feedback": len(feedback),
        "feedback_stats": feedback_stats,
        "model_status": {
            "distilbert": "loaded" if hasattr(event_analyzer, 'classifier') else "not loaded",
            "gpt2": "loaded" if hasattr(topic_generator, 'generator') else "not loaded"
        }
    }


@router.delete("/history")
async def clear_history():
    """Clear all history (admin only)"""
    success = history_logger.clear_history()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to clear history")
    return {"status": "success", "message": "History cleared"}


@router.delete("/feedback")
async def clear_feedback():
    """Clear all feedback (admin only)"""
    success = feedback_logger.clear_feedback()
    if not success:
        raise HTTPException(status_code=500, detail="Failed to clear feedback")
    return {"status": "success", "message": "Feedback cleared"}


@router.get("/models/info")
async def get_model_info():
    """Get model information"""
    return {
        "event_analyzer": {
            "model": "typeform/distilbert-base-uncased-mnli",
            "task": "zero-shot-classification",
            "loaded": hasattr(event_analyzer, 'classifier')
        },
        "topic_generator": {
            "model": "gpt2",
            "task": "text-generation",
            "loaded": hasattr(topic_generator, 'generator'),
            "max_length": 80
        }
    }