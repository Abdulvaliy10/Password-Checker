#!/usr/bin/env python3
"""
Simple script to run the English Learning API
"""

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Starting English Learning API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 ReDoc Documentation: http://localhost:8000/redoc")
    print("💚 Health Check: http://localhost:8000/health")
    print("=" * 50)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )