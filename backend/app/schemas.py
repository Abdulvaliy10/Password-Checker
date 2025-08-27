from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True


# User schemas
class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseSchema):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)


class UserResponse(UserBase):
    id: str
    points: int
    level: int
    experience: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserProfile(UserResponse):
    total_lessons_completed: int = 0
    total_games_played: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    badges_count: int = 0


# Authentication schemas
class Token(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseSchema):
    username: Optional[str] = None


class LoginRequest(BaseSchema):
    username: str
    password: str


class RefreshTokenRequest(BaseSchema):
    refresh_token: str


# Quiz schemas
class QuestionBase(BaseSchema):
    question: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None


class QuizBase(BaseSchema):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(vocabulary|grammar|phrases|pronunciation)$")
    difficulty: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    time_limit: Optional[int] = None
    points_reward: int = Field(default=10, ge=0)


class QuizCreate(QuizBase):
    questions: List[Dict[str, Any]]


class QuizUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, pattern="^(vocabulary|grammar|phrases|pronunciation)$")
    difficulty: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    questions: Optional[List[Dict[str, Any]]] = None
    time_limit: Optional[int] = None
    points_reward: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class QuizResponse(QuizBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    questions_count: int = 0


class QuizDetail(QuizResponse):
    questions: List[Dict[str, Any]]


# Score schemas
class ScoreBase(BaseSchema):
    score: float = Field(..., ge=0, le=100)
    correct_answers: int = Field(..., ge=0)
    total_questions: int = Field(..., ge=0)
    time_taken: Optional[int] = Field(None, ge=0)


class ScoreCreate(ScoreBase):
    quiz_id: str


class ScoreResponse(ScoreBase):
    id: str
    user_id: str
    quiz_id: str
    completed_at: datetime
    quiz_title: Optional[str] = None


class ScoreWithUser(ScoreResponse):
    user: UserResponse


# Badge schemas
class BadgeBase(BaseSchema):
    name: str = Field(..., max_length=100)
    description: str
    icon: str = Field(..., max_length=50)
    category: str = Field(..., max_length=50)
    rarity: str = Field(default="common", pattern="^(common|rare|epic|legendary)$")
    points_required: int = Field(default=0, ge=0)
    criteria_type: Optional[str] = Field(None, max_length=50)
    criteria_value: Optional[int] = Field(None, ge=0)


class BadgeCreate(BadgeBase):
    pass


class BadgeUpdate(BaseSchema):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=50)
    rarity: Optional[str] = Field(None, pattern="^(common|rare|epic|legendary)$")
    points_required: Optional[int] = Field(None, ge=0)
    criteria_type: Optional[str] = Field(None, max_length=50)
    criteria_value: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class BadgeResponse(BadgeBase):
    id: str
    is_active: bool
    created_at: datetime


class UserBadgeResponse(BaseSchema):
    id: str
    badge: BadgeResponse
    unlocked_at: datetime


# Word of the day schemas
class WordOfDayBase(BaseSchema):
    word: str = Field(..., max_length=100)
    meaning: str
    example_sentence: str
    pronunciation: Optional[str] = Field(None, max_length=100)
    difficulty: str = Field(default="beginner", pattern="^(beginner|intermediate|advanced)$")
    category: str = Field(default="vocabulary", max_length=50)


class WordOfDayCreate(WordOfDayBase):
    date: datetime


class WordOfDayUpdate(BaseSchema):
    word: Optional[str] = Field(None, max_length=100)
    meaning: Optional[str] = None
    example_sentence: Optional[str] = None
    pronunciation: Optional[str] = Field(None, max_length=100)
    difficulty: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    category: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class WordOfDayResponse(WordOfDayBase):
    id: str
    date: datetime
    is_active: bool
    created_at: datetime


# Lesson schemas
class LessonBase(BaseSchema):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: str = Field(..., pattern="^(vocabulary|grammar|phrases|pronunciation)$")
    difficulty: str = Field(..., pattern="^(beginner|intermediate|advanced)$")
    content: Optional[Dict[str, Any]] = None
    duration: Optional[int] = Field(None, ge=0)
    points_reward: int = Field(default=5, ge=0)
    is_locked: bool = False
    prerequisites: Optional[List[str]] = None


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = Field(None, pattern="^(vocabulary|grammar|phrases|pronunciation)$")
    difficulty: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced)$")
    content: Optional[Dict[str, Any]] = None
    duration: Optional[int] = Field(None, ge=0)
    points_reward: Optional[int] = Field(None, ge=0)
    is_locked: Optional[bool] = None
    prerequisites: Optional[List[str]] = None
    is_active: Optional[bool] = None


class LessonResponse(LessonBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserLessonBase(BaseSchema):
    completed: bool = False
    progress: float = Field(default=0.0, ge=0, le=100)
    time_spent: int = Field(default=0, ge=0)


class UserLessonCreate(UserLessonBase):
    lesson_id: str


class UserLessonUpdate(BaseSchema):
    completed: Optional[bool] = None
    progress: Optional[float] = Field(None, ge=0, le=100)
    time_spent: Optional[int] = Field(None, ge=0)


class UserLessonResponse(UserLessonBase):
    id: str
    user_id: str
    lesson_id: str
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    lesson: Optional[LessonResponse] = None


# Friendship schemas
class FriendshipBase(BaseSchema):
    friend_id: str
    status: str = Field(default="pending", pattern="^(pending|accepted|blocked)$")


class FriendshipCreate(FriendshipBase):
    pass


class FriendshipUpdate(BaseSchema):
    status: str = Field(..., pattern="^(pending|accepted|blocked)$")


class FriendshipResponse(FriendshipBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    friend: Optional[UserResponse] = None


# Leaderboard schemas
class LeaderboardEntry(BaseSchema):
    rank: int
    user: UserResponse
    total_points: int
    total_lessons: int
    total_games: int
    current_streak: int


# Statistics schemas
class UserStats(BaseSchema):
    total_points: int
    total_lessons_completed: int
    total_games_played: int
    average_score: float
    current_streak: int
    longest_streak: int
    badges_count: int
    level: int
    experience: int
    experience_to_next_level: int


# API Response schemas
class PaginatedResponse(BaseSchema):
    items: List[Any]
    total: int
    page: int
    size: int
    pages: int


class MessageResponse(BaseSchema):
    message: str


class ErrorResponse(BaseSchema):
    detail: str
    error_code: Optional[str] = None