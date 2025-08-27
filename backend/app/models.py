from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import uuid


def generate_uuid():
    """Generate a UUID for primary keys."""
    return str(uuid.uuid4())


class User(Base):
    """User model for authentication and profile management."""
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50))
    last_name = Column(String(50))
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    scores = relationship("Score", back_populates="user")
    user_badges = relationship("UserBadge", back_populates="user")
    friends = relationship("Friendship", foreign_keys="Friendship.user_id", back_populates="user")
    friend_of = relationship("Friendship", foreign_keys="Friendship.friend_id", back_populates="friend")


class Quiz(Base):
    """Quiz model for storing quiz questions and answers."""
    __tablename__ = "quizzes"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # vocabulary, grammar, phrases, pronunciation
    difficulty = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    questions = Column(JSON, nullable=False)  # Store questions as JSON
    time_limit = Column(Integer)  # Time limit in minutes
    points_reward = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    scores = relationship("Score", back_populates="quiz")


class Score(Base):
    """Score model for tracking user quiz performance."""
    __tablename__ = "scores"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(String, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score (0-100)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    time_taken = Column(Integer)  # Time taken in seconds
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="scores")
    quiz = relationship("Quiz", back_populates="scores")


class Badge(Base):
    """Badge model for gamification achievements."""
    __tablename__ = "badges"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), nullable=False)  # Emoji or icon identifier
    category = Column(String(50), nullable=False)  # beginner, vocabulary, grammar, etc.
    rarity = Column(String(20), default="common")  # common, rare, epic, legendary
    points_required = Column(Integer, default=0)
    criteria_type = Column(String(50))  # lessons_completed, games_won, streak_days, etc.
    criteria_value = Column(Integer)  # Value needed to unlock badge
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """UserBadge model for tracking which users have which badges."""
    __tablename__ = "user_badges"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    badge_id = Column(String, ForeignKey("badges.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")


class WordOfDay(Base):
    """Word of the day model for daily vocabulary learning."""
    __tablename__ = "words_of_day"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    word = Column(String(100), nullable=False)
    meaning = Column(Text, nullable=False)
    example_sentence = Column(Text, nullable=False)
    pronunciation = Column(String(100))
    difficulty = Column(String(20), default="beginner")
    category = Column(String(50), default="vocabulary")
    date = Column(DateTime(timezone=True), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Friendship(Base):
    """Friendship model for social features."""
    __tablename__ = "friendships"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    friend_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, blocked
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="friends")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friend_of")


class UserStreak(Base):
    """User streak model for tracking daily learning streaks."""
    __tablename__ = "user_streaks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Lesson(Base):
    """Lesson model for structured learning content."""
    __tablename__ = "lessons"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # vocabulary, grammar, phrases, pronunciation
    difficulty = Column(String(20), nullable=False)  # beginner, intermediate, advanced
    content = Column(JSON)  # Lesson content as JSON
    duration = Column(Integer)  # Duration in minutes
    points_reward = Column(Integer, default=5)
    is_active = Column(Boolean, default=True)
    is_locked = Column(Boolean, default=False)
    prerequisites = Column(JSON)  # List of required lesson IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserLesson(Base):
    """UserLesson model for tracking lesson completion."""
    __tablename__ = "user_lessons"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    progress = Column(Float, default=0.0)  # Progress percentage (0-100)
    time_spent = Column(Integer, default=0)  # Time spent in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())