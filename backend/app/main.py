from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.config import settings
from app.routes import auth, quizzes, badges, word_of_day, leaderboard

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

# Create FastAPI app
app = FastAPI(
    title="English Learning API",
    description="A comprehensive API for the English Learning platform with authentication, quizzes, badges, and gamification features.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.status_code}
    )

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(quizzes.router, prefix="/api/v1")
app.include_router(badges.router, prefix="/api/v1")
app.include_router(word_of_day.router, prefix="/api/v1")
app.include_router(leaderboard.router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to English Learning API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    """Get API information and available endpoints."""
    return {
        "name": "English Learning API",
        "version": "1.0.0",
        "description": "A comprehensive API for English learning with gamification features",
        "endpoints": {
            "authentication": {
                "register": "POST /api/v1/auth/register",
                "login": "POST /api/v1/auth/login",
                "refresh": "POST /api/v1/auth/refresh",
                "me": "GET /api/v1/auth/me"
            },
            "quizzes": {
                "list": "GET /api/v1/quizzes/",
                "detail": "GET /api/v1/quizzes/{id}",
                "submit": "POST /api/v1/quizzes/{id}/submit"
            },
            "badges": {
                "list": "GET /api/v1/badges/",
                "my_badges": "GET /api/v1/badges/my-badges",
                "check_achievements": "POST /api/v1/badges/check-achievements"
            },
            "word_of_day": {
                "today": "GET /api/v1/word-of-day/today",
                "list": "GET /api/v1/word-of-day/"
            },
            "leaderboard": {
                "global": "GET /api/v1/leaderboard/",
                "my_position": "GET /api/v1/leaderboard/my-position",
                "stats": "GET /api/v1/leaderboard/stats"
            }
        },
        "features": [
            "JWT Authentication",
            "Quiz Management",
            "Badge System",
            "Word of the Day",
            "Leaderboards",
            "Gamification",
            "Progress Tracking"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )