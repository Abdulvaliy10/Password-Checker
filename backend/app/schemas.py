from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    difficulty: str
    time_limit: Optional[int] = 300
    points_reward: Optional[int] = 10

class ScoreBase(BaseModel):
    score: float
    time_taken: Optional[int] = None
    answers: Optional[str] = None

class BadgeBase(BaseModel):
    name: str
    description: str
    icon: str
    points_required: int = 0
    category: Optional[str] = None

class WordOfDayBase(BaseModel):
    word: str
    meaning: str
    example_sentence: str
    pronunciation: Optional[str] = None
    difficulty: str = "medium"
    category: Optional[str] = None

# Create schemas
class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class QuizCreate(QuizBase):
    questions: str  # JSON string
    correct_answers: str  # JSON string

class ScoreCreate(ScoreBase):
    quiz_id: int

class BadgeCreate(BadgeBase):
    pass

class WordOfDayCreate(WordOfDayBase):
    date: datetime

# Response schemas
class UserResponse(UserBase):
    id: int
    points: int
    level: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    total_quizzes_completed: Optional[int] = None
    average_score: Optional[float] = None
    badges_count: Optional[int] = None

class QuizResponse(QuizBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ScoreResponse(ScoreBase):
    id: int
    user_id: int
    quiz_id: int
    completed_at: datetime
    
    class Config:
        from_attributes = True

class BadgeResponse(BadgeBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserBadgeResponse(BaseModel):
    id: int
    user_id: int
    badge_id: int
    earned_at: datetime
    badge: BadgeResponse
    
    class Config:
        from_attributes = True

class WordOfDayResponse(WordOfDayBase):
    id: int
    date: datetime
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Leaderboard schemas
class LeaderboardEntry(BaseModel):
    user_id: int
    username: str
    points: int
    level: int
    rank: int

# Quiz submission schemas
class QuizSubmission(BaseModel):
    quiz_id: int
    answers: Dict[str, Any]
    time_taken: int

# Friend schemas
class FriendRequest(BaseModel):
    friend_username: str

class FriendResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    created_at: datetime
    friend: UserResponse
    
    class Config:
        from_attributes = True

# Statistics schemas
class UserStats(BaseModel):
    total_quizzes: int
    average_score: float
    total_points: int
    level: int
    badges_count: int
    streak_days: int

# Update schemas
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    points: Optional[int] = None
    level: Optional[int] = None

class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None
    questions: Optional[str] = None
    correct_answers: Optional[str] = None
    time_limit: Optional[int] = None
    points_reward: Optional[int] = None
    is_active: Optional[bool] = None