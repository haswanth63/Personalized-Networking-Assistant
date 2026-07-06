"""
API Routes - FastAPI Router Integration
Following FastAPI-Specific Features:
- Type-safe request validation
- Response model enforcement
- Automatic OpenAPI documentation
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Dict, Any

from app.models.schemas import (
    EventInput,
    UserInterests,
    ConversationRequest,
    ConversationResponse,
    FactCheckRequest,
    FactCheckResponse,
    ThemeResponse,
    FeedbackRequest,
    HistoryEntry,
    FeedbackEntry
)
from app.services import (
    event_analyzer,
    topic_generator,
    fact_checker,
    history_logger,
    feedback_logger
)
from app.dependencies import (
    check_rate_limit,
    get_request_id,
    get_current_user
)
from app.utils.validators import (
    validate_event_description,
    validate_interests,
    validate_feedback_action,
    validate_suggestion_text,
    sanitize_input
)
from app.exceptions import AppException

router = APIRouter(tags=["Conversation"])


@router.post(
    "/analyze-event",
    response_model=ThemeResponse,
    status_code=status.HTTP_200_OK,
    summary="Extract themes from event description",
    description="Uses DistilBERT zero-shot classification to extract key themes"
)
async def analyze_event(
    request: EventInput,
    request_id: str = Depends(get_request_id),
    _: bool = Depends(check_rate_limit)
):
    """
    Analyze event description and extract key themes
    """
    try:
        # Validate input
        validate_event_description(request.description)
        sanitized_desc = sanitize_input(request.description)
        
        # Extract themes
        themes = event_analyzer.extract_event_themes(
            sanitized_desc,
            request.custom_themes
        )
        
        return ThemeResponse(
            themes=themes,
            event_description=sanitized_desc
        )
        
    except AppException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze event: {str(e)}"
        )


@router.post(
    "/fact-check",
    response_model=FactCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify a fact using Wikipedia"
)
async def check_fact(
    request: FactCheckRequest,
    request_id: str = Depends(get_request_id),
    _: bool = Depends(check_rate_limit)
):
    """
    Verify a fact using Wikipedia API
    """
    try:
        sanitized_query = sanitize_input(request.query)
        
        if len(sanitized_query) < 3:
            return FactCheckResponse(
                query=sanitized_query,
                summary="Query too short to verify.",
                verified=False,
                source_url=None
            )
        
        result = fact_checker.fact_check(sanitized_query)
        
        return FactCheckResponse(
            query=result["query"],
            summary=result["summary"],
            verified=result["verified"],
            source_url=result.get("source_url")
        )
        
    except Exception as e:
        return FactCheckResponse(
            query=request.query,
            summary=f"Error during fact-check: {str(e)}",
            verified=False,
            source_url=None
        )


@router.post(
    "/generate-conversation",
    response_model=ConversationResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate conversation starters",
    description="""
    Main orchestration endpoint:
    1. Extract themes using DistilBERT
    2. Generate starters using GPT-2
    3. Log to history
    """
)
async def generate_conversation(
    request: ConversationRequest,
    request_id: str = Depends(get_request_id),
    _: bool = Depends(check_rate_limit)
):
    """
    Generate conversation starters based on event and user interests
    """
    try:
        # Validate inputs
        validate_event_description(request.event_description)
        validate_interests(request.user_interests)
        
        sanitized_desc = sanitize_input(request.event_description)
        sanitized_interests = [sanitize_input(i) for i in request.user_interests]
        
        # Step 1: Extract themes
        themes = event_analyzer.extract_event_themes(sanitized_desc)
        
        # Step 2: Generate conversation starters
        suggestions = topic_generator.generate_topics(
            themes=themes,
            user_interests=sanitized_interests,
            max_suggestions=request.max_suggestions or 3
        )
        
        # Step 3: Log to history
        history_id = history_logger.log_conversation({
            "event_description": sanitized_desc,
            "themes": themes,
            "suggestions": suggestions,
            "user_interests": sanitized_interests,
            "request_id": request_id
        })
        
        return ConversationResponse(
            event_description=sanitized_desc,
            extracted_themes=themes,
            suggestions=suggestions,
            history_id=history_id
        )
        
    except AppException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate conversation: {str(e)}"
        )


@router.post(
    "/feedback",
    status_code=status.HTTP_200_OK,
    summary="Submit feedback for a suggestion"
)
async def submit_feedback(
    request: FeedbackRequest,
    request_id: str = Depends(get_request_id),
    _: bool = Depends(check_rate_limit)
):
    """
    Submit user feedback (like/dislike) for a conversation suggestion
    """
    try:
        # Validate inputs
        validate_suggestion_text(request.suggestion)
        validate_feedback_action(request.action)
        
        sanitized_suggestion = sanitize_input(request.suggestion)
        
        entry = feedback_logger.log_feedback(
            suggestion=sanitized_suggestion,
            action=request.action
        )
        
        return {
            "status": "success",
            "feedback": entry,
            "request_id": request_id
        }
        
    except AppException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )


@router.get(
    "/history",
    response_model=Dict[str, Any],
    summary="Get conversation history"
)
async def get_history(
    limit: int = 10,
    offset: int = 0,
    request_id: str = Depends(get_request_id)
):
    """
    Get conversation history with pagination
    """
    try:
        history = history_logger.load_history()
        total = len(history)
        paginated = history[offset:offset + limit]
        
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "entries": paginated,
            "request_id": request_id
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load history: {str(e)}"
        )


@router.get(
    "/history/{entry_id}",
    response_model=Dict[str, Any],
    summary="Get specific history entry"
)
async def get_history_entry(
    entry_id: str,
    request_id: str = Depends(get_request_id)
):
    """
    Get a specific history entry by ID
    """
    try:
        entry = history_logger.get_history_entry(entry_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"History entry '{entry_id}' not found"
            )
        return entry
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history entry: {str(e)}"
        )


@router.get(
    "/feedback/stats",
    response_model=Dict[str, Any],
    summary="Get feedback statistics"
)
async def get_feedback_stats(
    request_id: str = Depends(get_request_id)
):
    """
    Get feedback statistics including likes, dislikes, and like rate
    """
    try:
        stats = feedback_logger.get_feedback_stats()
        stats["request_id"] = request_id
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get feedback stats: {str(e)}"
        )