"""
Application Entry Point - Central Hub
Following the Centralized Routing Architecture pattern

This is the hub in the hub-and-spoke model:
- Assembles the application from modular components
- Registers all routers
- Applies middleware
- Sets up error handling
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import conversation, health, admin
from app.middleware import LoggingMiddleware, RequestIDMiddleware, ErrorHandlingMiddleware

# ============ CREATE FASTAPI APPLICATION ============

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ============ ADD MIDDLEWARE ============

# Order matters: Error handling first, then logging, then others
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# ============ REGISTER ROUTERS ============

# Health router - production best practice
app.include_router(health.router)

# Main conversation router - core functionality
app.include_router(conversation.router)

# Admin router - admin endpoints
app.include_router(admin.router)

# ============ ROOT ENDPOINT ============

@app.get("/")
async def root():
    """Root endpoint - quick API check"""
    return {
        "message": "Welcome to the Networking Assistant API!",
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready"
    }


@app.on_event("startup")
async def startup_event():
    """Startup tasks - preload models"""
    print("🚀 Starting Personalized Networking Assistant...")
    print(f"📚 Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔧 Health check: http://{settings.HOST}:{settings.PORT}/health")
    
    # Preload models (optional - already loaded on import)
    # This ensures models are loaded before first request


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    print("🛑 Shutting down Personalized Networking Assistant...")


# ============ ENTRY POINT ============

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )