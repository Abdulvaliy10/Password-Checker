from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.auth import get_current_active_user
from app.models import User, Quiz, Score
from app.schemas import (
    QuizCreate, QuizUpdate, QuizResponse, QuizDetail,
    ScoreCreate, ScoreResponse, PaginatedResponse
)

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.get("/", response_model=PaginatedResponse)
async def get_quizzes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None, pattern="^(vocabulary|grammar|phrases|pronunciation)$"),
    difficulty: Optional[str] = Query(None, pattern="^(beginner|intermediate|advanced)$"),
    search: Optional[str] = Query(None, min_length=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all quizzes with optional filtering and pagination.
    
    - **skip**: Number of records to skip
    - **limit**: Number of records to return
    - **category**: Filter by category
    - **difficulty**: Filter by difficulty
    - **search**: Search in title and description
    """
    query = db.query(Quiz).filter(Quiz.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(Quiz.category == category)
    if difficulty:
        query = query.filter(Quiz.difficulty == difficulty)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Quiz.title.ilike(search_term)) | (Quiz.description.ilike(search_term))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    quizzes = query.offset(skip).limit(limit).all()
    
    # Add questions count to each quiz
    for quiz in quizzes:
        quiz.questions_count = len(quiz.questions) if quiz.questions else 0
    
    return {
        "items": quizzes,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{quiz_id}", response_model=QuizDetail)
async def get_quiz(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific quiz by ID.
    
    - **quiz_id**: Quiz ID
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    quiz.questions_count = len(quiz.questions) if quiz.questions else 0
    return quiz


@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    quiz_data: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new quiz (admin only).
    
    - **title**: Quiz title
    - **description**: Quiz description
    - **category**: Quiz category
    - **difficulty**: Quiz difficulty
    - **questions**: List of questions
    - **time_limit**: Optional time limit in minutes
    - **points_reward**: Points awarded for completion
    """
    # TODO: Add admin role check
    quiz = Quiz(**quiz_data.dict())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    quiz.questions_count = len(quiz.questions) if quiz.questions else 0
    return quiz


@router.put("/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: str,
    quiz_data: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a quiz (admin only).
    
    - **quiz_id**: Quiz ID
    """
    # TODO: Add admin role check
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    update_data = quiz_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(quiz, field, value)
    
    db.commit()
    db.refresh(quiz)
    
    quiz.questions_count = len(quiz.questions) if quiz.questions else 0
    return quiz


@router.delete("/{quiz_id}", response_model=dict)
async def delete_quiz(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a quiz (admin only).
    
    - **quiz_id**: Quiz ID
    """
    # TODO: Add admin role check
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Soft delete by setting is_active to False
    quiz.is_active = False
    db.commit()
    
    return {"message": "Quiz deleted successfully"}


@router.post("/{quiz_id}/submit", response_model=ScoreResponse)
async def submit_quiz_score(
    quiz_id: str,
    score_data: ScoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Submit a quiz score.
    
    - **quiz_id**: Quiz ID
    - **score**: Percentage score (0-100)
    - **correct_answers**: Number of correct answers
    - **total_questions**: Total number of questions
    - **time_taken**: Time taken in seconds (optional)
    """
    # Verify quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Create score record
    score = Score(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score_data.score,
        correct_answers=score_data.correct_answers,
        total_questions=score_data.total_questions,
        time_taken=score_data.time_taken
    )
    db.add(score)
    
    # Award points to user
    if score_data.score >= 60:  # Minimum 60% to get points
        points_earned = int((score_data.score / 100) * quiz.points_reward)
        current_user.points += points_earned
        
        # Update experience and level
        current_user.experience += points_earned
        new_level = (current_user.experience // 100) + 1
        if new_level > current_user.level:
            current_user.level = new_level
    
    db.commit()
    db.refresh(score)
    
    return score


@router.get("/{quiz_id}/scores", response_model=List[ScoreResponse])
async def get_quiz_scores(
    quiz_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all scores for a specific quiz.
    
    - **quiz_id**: Quiz ID
    """
    scores = db.query(Score).filter(Score.quiz_id == quiz_id).all()
    return scores


@router.get("/categories/stats", response_model=dict)
async def get_quiz_category_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get statistics for quiz categories.
    """
    stats = db.query(
        Quiz.category,
        func.count(Quiz.id).label('total_quizzes'),
        func.avg(Score.score).label('average_score')
    ).outerjoin(Score, Quiz.id == Score.quiz_id).filter(
        Quiz.is_active == True
    ).group_by(Quiz.category).all()
    
    return {
        "categories": [
            {
                "category": stat.category,
                "total_quizzes": stat.total_quizzes,
                "average_score": float(stat.average_score) if stat.average_score else 0
            }
            for stat in stats
        ]
    }


@router.get("/difficulty/stats", response_model=dict)
async def get_quiz_difficulty_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get statistics for quiz difficulties.
    """
    stats = db.query(
        Quiz.difficulty,
        func.count(Quiz.id).label('total_quizzes'),
        func.avg(Score.score).label('average_score')
    ).outerjoin(Score, Quiz.id == Score.quiz_id).filter(
        Quiz.is_active == True
    ).group_by(Quiz.difficulty).all()
    
    return {
        "difficulties": [
            {
                "difficulty": stat.difficulty,
                "total_quizzes": stat.total_quizzes,
                "average_score": float(stat.average_score) if stat.average_score else 0
            }
            for stat in stats
        ]
    }