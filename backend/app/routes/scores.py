from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from ..database import get_db
from ..auth import get_current_active_user
from ..models import Score, User, Quiz, UserBadge
from ..schemas import ScoreResponse, UserStats

router = APIRouter(prefix="/scores", tags=["scores"])

@router.get("/", response_model=List[ScoreResponse])
def get_user_scores(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's scores.
    
    - **skip**: Number of scores to skip
    - **limit**: Maximum number of scores to return
    """
    scores = db.query(Score).filter(
        Score.user_id == current_user.id
    ).order_by(desc(Score.completed_at)).offset(skip).limit(limit).all()
    
    return scores

@router.get("/stats", response_model=UserStats)
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's statistics.
    """
    # Get total quizzes completed
    total_quizzes = db.query(func.count(Score.id)).filter(
        Score.user_id == current_user.id
    ).scalar()
    
    # Get average score
    avg_score_result = db.query(func.avg(Score.score)).filter(
        Score.user_id == current_user.id
    ).scalar()
    average_score = float(avg_score_result) if avg_score_result else 0.0
    
    # Get badges count
    badges_count = db.query(func.count(UserBadge.id)).filter(
        UserBadge.user_id == current_user.id
    ).scalar()
    
    # Calculate level based on points (simple formula: level = points // 100 + 1)
    level = (current_user.points // 100) + 1
    
    # Calculate streak days (simplified - in real app you'd track daily activity)
    # For now, we'll return a placeholder
    streak_days = 0
    
    return UserStats(
        total_quizzes=total_quizzes,
        average_score=average_score,
        total_points=current_user.points,
        level=level,
        badges_count=badges_count,
        streak_days=streak_days
    )

@router.get("/leaderboard", response_model=List[dict])
def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get global leaderboard.
    
    - **limit**: Number of top users to return
    """
    # Get top users by points
    top_users = db.query(
        User.id,
        User.username,
        User.points,
        func.count(Score.id).label('total_quizzes')
    ).outerjoin(Score, User.id == Score.user_id).filter(
        User.is_active == True
    ).group_by(User.id).order_by(
        desc(User.points)
    ).limit(limit).all()
    
    leaderboard = []
    for i, user in enumerate(top_users, 1):
        leaderboard.append({
            "rank": i,
            "user_id": user.id,
            "username": user.username,
            "points": user.points,
            "total_quizzes": user.total_quizzes
        })
    
    return leaderboard

@router.get("/quiz/{quiz_id}", response_model=List[ScoreResponse])
def get_quiz_scores(
    quiz_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all scores for a specific quiz.
    
    - **quiz_id**: ID of the quiz
    - **skip**: Number of scores to skip
    - **limit**: Maximum number of scores to return
    """
    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    scores = db.query(Score).filter(
        Score.quiz_id == quiz_id
    ).order_by(desc(Score.score)).offset(skip).limit(limit).all()
    
    return scores

@router.get("/recent", response_model=List[ScoreResponse])
def get_recent_scores(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get recent scores from all users.
    
    - **limit**: Number of recent scores to return
    """
    scores = db.query(Score).order_by(
        desc(Score.completed_at)
    ).limit(limit).all()
    
    return scores

@router.get("/user/{user_id}", response_model=List[ScoreResponse])
def get_user_scores_by_id(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get scores for a specific user by ID.
    
    - **user_id**: ID of the user
    - **skip**: Number of scores to skip
    - **limit**: Maximum number of scores to return
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    scores = db.query(Score).filter(
        Score.user_id == user_id
    ).order_by(desc(Score.completed_at)).offset(skip).limit(limit).all()
    
    return scores