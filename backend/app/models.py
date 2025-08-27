from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    scores = relationship("Score", back_populates="user")
    user_badges = relationship("UserBadge", back_populates="user")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # grammar, vocabulary, reading, etc.
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    questions = Column(Text, nullable=False)  # JSON string of questions
    correct_answers = Column(Text, nullable=False)  # JSON string of correct answers
    time_limit = Column(Integer, default=300)  # seconds
    points_reward = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    scores = relationship("Score", back_populates="quiz")

class Score(Base):
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)  # percentage score
    time_taken = Column(Integer)  # seconds
    answers = Column(Text)  # JSON string of user answers
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="scores")
    quiz = relationship("Quiz", back_populates="scores")

class Badge(Base):
    __tablename__ = "badges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=False)  # icon filename or URL
    points_required = Column(Integer, default=0)
    category = Column(String(50))  # achievement, milestone, special
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")

class UserBadge(Base):
    __tablename__ = "user_badges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="user_badges")
    badge = relationship("Badge", back_populates="user_badges")

class WordOfDay(Base):
    __tablename__ = "words_of_day"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False)
    meaning = Column(Text, nullable=False)
    example_sentence = Column(Text, nullable=False)
    pronunciation = Column(String(100))
    difficulty = Column(String(20), default="medium")
    category = Column(String(50))  # vocabulary, grammar, idiom
    date = Column(DateTime, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Friend(Base):
    __tablename__ = "friends"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending, accepted, blocked
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())