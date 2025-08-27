#!/usr/bin/env python3
"""
Simple script to create database tables.
"""

from app.database import engine, Base
from app.models import User, Quiz, Score, Badge, UserBadge, WordOfDay, Friendship, UserStreak, Lesson, UserLesson

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_tables()