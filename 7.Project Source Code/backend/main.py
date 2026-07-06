from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
import uuid
import os

# Import all services
from models import (
    UserProfile, EventContext, NetworkingSession, 
    GeneratedStarter, WikipediaFactCheck, LogEntry, Feedback,
    ActionType, VerificationStatus
)
from database import db
from theme_classifier import theme_classifier
from conversation_generator import conversation_generator
from wikipedia_service import WikipediaService

# Initialize FastAPI
app = FastAPI(
    title="Personalised Networking Assistant API",
    description="""
    AI-powered networking assistant with:
    - Theme extraction using DistilBERT
    - Conversation generation using GPT-2
    - Fact-checking using Wikipedia API
    - Comprehensive logging and feedback system
    """,
    version="2.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
wiki_service = WikipediaService()

# ==================== HELPER FUNCTIONS ====================
def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_log_entry(session_id: Optional[str], action_type: ActionType, payload: dict):
    """Create a log entry"""
    log = {
        "LogID": generate_id("LOG"),
        "SessionID": session_id,
        "ActionType": action_type.value,
        "PayloadJSON": payload,
        "Timestamp": datetime.now().isoformat()
    }
    return db.create("logs", log)

# ==================== USER ROUTES ====================
@app.post("/users", response_model=dict)
async def create_user(user: UserProfile):
    """Create a new user profile"""
    user_dict = user.dict()
    user_dict["UserID"] = generate_id("USR")
    user_dict["created_at"] = datetime.now().isoformat()
    user_dict["updated_at"] = datetime.now().isoformat()
    
    result = db.create("users", user_dict)
    create_log_entry(None, ActionType.USER_UPDATE, {"action": "create_user", "user_id": result["UserID"]})
    return {"status": "success", "data": result}

@app.get("/users", response_model=List[dict])
async def get_all_users():
    """Get all user profiles"""
    return db.read_all("users")

@app.get("/users/{user_id}", response_model=dict)
async def get_user(user_id: str):
    """Get a specific user by ID"""
    user = db.read_by_id("users", "UserID", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: str, updates: dict):
    """Update a user profile"""
    updated = db.update("users", "UserID", user_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    create_log_entry(None, ActionType.USER_UPDATE, {"action": "update_user", "user_id": user_id})
    return {"status": "success", "data": updated}

@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user profile"""
    deleted = db.delete("users", "UserID", user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success", "message": "User deleted"}

# ==================== EVENT ROUTES (Enhanced with AI) ====================
@app.post("/events", response_model=dict)
async def create_event(event: EventContext, auto_analyze: bool = True):
    """Create a new event context with automatic theme extraction"""
    event_dict = event.dict()
    event_dict["EventID"] = generate_id("EVT")
    event_dict["created_at"] = datetime.now().isoformat()
    
    # AI-powered theme extraction using DistilBERT
    if auto_analyze or event_dict["AnalyzedThemes"] == "auto":
        try:
            themes = theme_classifier.get_theme_summary(event_dict["EventDescription"])
            event_dict["AnalyzedThemes"] = themes
            print(f"✅ Themes extracted: {themes}")
        except Exception as e:
            print(f"⚠️ Theme extraction failed: {e}")
            event_dict["AnalyzedThemes"] = "general networking, professional development"
    
    result = db.create("events", event_dict)
    create_log_entry(None, ActionType.EVENT_UPDATE, {
        "action": "create_event", 
        "event_id": result["EventID"],
        "themes": result["AnalyzedThemes"]
    })
    
    return {"status": "success", "data": result}

@app.get("/events", response_model=List[dict])
async def get_all_events():
    """Get all events"""
    return db.read_all("events")

@app.get("/events/{event_id}", response_model=dict)
async def get_event(event_id: str):
    """Get a specific event by ID"""
    event = db.read_by_id("events", "EventID", event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.post("/events/analyze", response_model=dict)
async def analyze_event_themes(event_description: str):
    """Extract themes from an event description using DistilBERT"""
    themes = theme_classifier.extract_themes(event_description, top_k=5)
    summary = theme_classifier.get_theme_summary(event_description)
    return {
        "status": "success",
        "themes": themes,
        "summary": summary,
        "model": "distilbert-base-uncased-mnli"
    }

# ==================== SESSION ROUTES ====================
@app.post("/sessions", response_model=dict)
async def create_session(user_id: str, event_id: str):
    """Create a new networking session"""
    user = db.read_by_id("users", "UserID", user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    event = db.read_by_id("events", "EventID", event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    session = {
        "SessionID": generate_id("SES"),
        "UserID": user_id,
        "EventID": event_id,
        "SessionTimestamp": datetime.now().isoformat()
    }
    
    result = db.create("sessions", session)
    create_log_entry(result["SessionID"], ActionType.SESSION_CREATE, 
                     {"user_id": user_id, "event_id": event_id})
    return {"status": "success", "data": result}

@app.get("/sessions", response_model=List[dict])
async def get_all_sessions():
    """Get all sessions"""
    return db.read_all("sessions")

@app.get("/sessions/{session_id}", response_model=dict)
async def get_session(session_id: str):
    """Get a specific session by ID"""
    session = db.read_by_id("sessions", "SessionID", session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.get("/sessions/user/{user_id}", response_model=List[dict])
async def get_user_sessions(user_id: str):
    """Get all sessions for a specific user"""
    return db.read_by_field("sessions", "UserID", user_id)

# ==================== STARTER GENERATION ROUTE (GPT-2) ====================
@app.post("/sessions/{session_id}/generate-starter", response_model=dict)
async def generate_starter(
    session_id: str, 
    style: str = "professional",
    custom_prompt: Optional[str] = None
):
    """
    Generate a personalized conversation starter using GPT-2
    
    Styles: professional, casual, icebreaker, expert
    """
    # Get session
    session = db.read_by_id("sessions", "SessionID", session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get user and event
    user = db.read_by_id("users", "UserID", session["UserID"])
    event = db.read_by_id("events", "EventID", session["EventID"])
    
    if not user or not event:
        raise HTTPException(status_code=404, detail="User or Event not found")
    
    # Generate starter using GPT-2
    starter_text, prompt_used = conversation_generator.generate_starter(
        user_bio=user["BioText"],
        event_description=event["EventDescription"],
        event_themes=event["AnalyzedThemes"],
        style=style,
        custom_prompt=custom_prompt
    )
    
    # Save the generated starter
    starter = {
        "StarterID": generate_id("STR"),
        "SessionID": session_id,
        "StarterText": starter_text,
        "ContextPromptUsed": prompt_used,
        "Style": style,
        "created_at": datetime.now().isoformat()
    }
    
    result = db.create("starters", starter)
    
    # Log the action
    create_log_entry(session_id, ActionType.GENERATE_STARTER, 
                     {"starter_id": result["StarterID"], "session_id": session_id, "style": style})
    
    return {
        "status": "success", 
        "data": result,
        "model": conversation_generator.get_model_info()
    }

@app.get("/sessions/{session_id}/starters", response_model=List[dict])
async def get_session_starters(session_id: str):
    """Get all generated starters for a session"""
    return db.read_by_field("starters", "SessionID", session_id)

# ==================== FACT-CHECK ROUTE ====================
@app.post("/sessions/{session_id}/fact-check", response_model=dict)
async def fact_check_statement(session_id: str, query_text: str):
    """Fact-check a statement using Wikipedia API"""
    session = db.read_by_id("sessions", "SessionID", session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    verification_result = await wiki_service.verify_fact(query_text)
    
    fact_check = {
        "FactCheckID": generate_id("FCT"),
        "SessionID": session_id,
        "VerifiedQueryText": query_text,
        "VerificationStatus": verification_result["status"],
        "WikipediaSourceURL": verification_result.get("url"),
        "created_at": datetime.now().isoformat()
    }
    
    result = db.create("factchecks", fact_check)
    create_log_entry(session_id, ActionType.FACT_CHECK, 
                     {"fact_check_id": result["FactCheckID"], "query": query_text})
    
    return {"status": "success", "data": result, "verification": verification_result}

@app.get("/sessions/{session_id}/factchecks", response_model=List[dict])
async def get_session_factchecks(session_id: str):
    """Get all fact-checks for a session"""
    return db.read_by_field("factchecks", "SessionID", session_id)

# ==================== FEEDBACK ROUTES ====================
@app.post("/feedback", response_model=dict)
async def create_feedback(feedback_data: dict):
    """Submit feedback for a generated starter"""
    feedback_data["FeedbackID"] = generate_id("FDB")
    feedback_data["created_at"] = datetime.now().isoformat()
    
    result = db.create("feedbacks", feedback_data)
    create_log_entry(None, ActionType.FEEDBACK, 
                     {"feedback_id": result["FeedbackID"], "starter_id": feedback_data.get("StarterID")})
    return {"status": "success", "data": result}

@app.get("/feedback/starter/{starter_id}", response_model=List[dict])
async def get_feedback_by_starter(starter_id: str):
    """Get all feedback for a specific starter"""
    return db.read_by_field("feedbacks", "StarterID", starter_id)

@app.get("/feedback/all", response_model=List[dict])
async def get_all_feedback():
    """Get all feedback entries"""
    return db.read_all("feedbacks")

@app.get("/feedback/stats", response_model=dict)
async def get_feedback_stats():
    """Get overall feedback statistics"""
    feedbacks = db.read_all("feedbacks")
    
    if not feedbacks:
        return {"total": 0, "average_rating": 0, "distribution": {}}
    
    ratings = [f.get("Rating", 0) for f in feedbacks]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0
    
    types = {}
    for f in feedbacks:
        fb_type = f.get("FeedbackType", "unknown")
        types[fb_type] = types.get(fb_type, 0) + 1
    
    return {
        "total": len(feedbacks),
        "average_rating": round(avg_rating, 2),
        "distribution": types
    }

# ==================== LOG ROUTES ====================
@app.get("/logs", response_model=List[dict])
async def get_all_logs():
    """Get all system logs"""
    return db.read_all("logs")

@app.get("/logs/session/{session_id}", response_model=List[dict])
async def get_session_logs(session_id: str):
    """Get logs for a specific session"""
    return db.read_by_field("logs", "SessionID", session_id)

# ==================== HEALTH CHECK ====================
@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint with service status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "theme_classifier": "loaded" if theme_classifier else "error",
            "conversation_generator": conversation_generator.get_model_info(),
            "wikipedia_service": "loaded",
            "database": "connected"
        }
    }

# ==================== SYSTEM INFO ====================
@app.get("/system/info", response_model=dict)
async def system_info():
    """Get system information"""
    import torch
    return {
        "python_version": "3.11+",
        "framework": "FastAPI",
        "ai_models": {
            "theme_extraction": "typeform/distilbert-base-uncased-mnli",
            "conversation_generation": conversation_generator.model_name
        },
        "gpu_available": torch.cuda.is_available(),
        "gpu_device": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None"
    }

# ==================== RUN THE APP ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)