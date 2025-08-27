from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from .database import engine, Base
from .config import settings
from .routes import auth, quizzes, scores, badges, word_of_day, friends

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
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A comprehensive English Learning API with gamification features",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(quizzes.router, prefix="/api/v1")
app.include_router(scores.router, prefix="/api/v1")
app.include_router(badges.router, prefix="/api/v1")
app.include_router(word_of_day.router, prefix="/api/v1")
app.include_router(friends.router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to English Learning API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# API info endpoint
@app.get("/api/v1/info")
async def api_info():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "endpoints": {
            "authentication": "/api/v1/auth",
            "quizzes": "/api/v1/quizzes",
            "scores": "/api/v1/scores",
            "badges": "/api/v1/badges",
            "word_of_day": "/api/v1/word-of-day",
            "friends": "/api/v1/friends"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )