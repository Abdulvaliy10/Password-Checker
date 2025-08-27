from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.database import get_db
from app.auth import get_current_active_user
from app.models import User, Score, UserLesson, UserBadge, UserStreak
from app.schemas import LeaderboardEntry, UserStats

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("/", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the global leaderboard by total points.
    
    - **limit**: Number of top users to return
    """
    # Get users with their stats, ordered by total points
    leaderboard = db.query(
        User,
        func.coalesce(func.sum(Score.score), 0).label('total_points'),
        func.count(UserLesson.id).label('total_lessons'),
        func.count(Score.id).label('total_games'),
        func.coalesce(UserStreak.current_streak, 0).label('current_streak')
    ).outerjoin(Score, User.id == Score.user_id).outerjoin(
        UserLesson, User.id == UserLesson.user_id
    ).outerjoin(UserStreak, User.id == UserStreak.user_id).filter(
        User.is_active == True
    ).group_by(User.id, UserStreak.current_streak).order_by(
        desc('total_points')
    ).limit(limit).all()
    
    # Format response
    result = []
    for rank, (user, total_points, total_lessons, total_games, current_streak) in enumerate(leaderboard, 1):
        result.append({
            "rank": rank,
            "user": user,
            "total_points": int(total_points),
            "total_lessons": total_lessons,
            "total_games": total_games,
            "current_streak": current_streak
        })
    
    return result


@router.get("/by-lessons", response_model=List[LeaderboardEntry])
async def get_leaderboard_by_lessons(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get leaderboard by completed lessons.
    
    - **limit**: Number of top users to return
    """
    leaderboard = db.query(
        User,
        func.coalesce(func.sum(Score.score), 0).label('total_points'),
        func.count(UserLesson.id).label('total_lessons'),
        func.count(Score.id).label('total_games'),
        func.coalesce(UserStreak.current_streak, 0).label('current_streak')
    ).outerjoin(Score, User.id == Score.user_id).outerjoin(
        UserLesson, User.id == UserLesson.user_id
    ).outerjoin(UserStreak, User.id == UserStreak.user_id).filter(
        User.is_active == True,
        UserLesson.completed == True
    ).group_by(User.id, UserStreak.current_streak).order_by(
        desc('total_lessons')
    ).limit(limit).all()
    
    result = []
    for rank, (user, total_points, total_lessons, total_games, current_streak) in enumerate(leaderboard, 1):
        result.append({
            "rank": rank,
            "user": user,
            "total_points": int(total_points),
            "total_lessons": total_lessons,
            "total_games": total_games,
            "current_streak": current_streak
        })
    
    return result


@router.get("/by-streak", response_model=List[LeaderboardEntry])
async def get_leaderboard_by_streak(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get leaderboard by current learning streak.
    
    - **limit**: Number of top users to return
    """
    leaderboard = db.query(
        User,
        func.coalesce(func.sum(Score.score), 0).label('total_points'),
        func.count(UserLesson.id).label('total_lessons'),
        func.count(Score.id).label('total_games'),
        func.coalesce(UserStreak.current_streak, 0).label('current_streak')
    ).outerjoin(Score, User.id == Score.user_id).outerjoin(
        UserLesson, User.id == UserLesson.user_id
    ).outerjoin(UserStreak, User.id == UserStreak.user_id).filter(
        User.is_active == True
    ).group_by(User.id, UserStreak.current_streak).order_by(
        desc('current_streak')
    ).limit(limit).all()
    
    result = []
    for rank, (user, total_points, total_lessons, total_games, current_streak) in enumerate(leaderboard, 1):
        result.append({
            "rank": rank,
            "user": user,
            "total_points": int(total_points),
            "total_lessons": total_lessons,
            "total_games": total_games,
            "current_streak": current_streak
        })
    
    return result


@router.get("/by-badges", response_model=List[LeaderboardEntry])
async def get_leaderboard_by_badges(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get leaderboard by number of badges earned.
    
    - **limit**: Number of top users to return
    """
    leaderboard = db.query(
        User,
        func.coalesce(func.sum(Score.score), 0).label('total_points'),
        func.count(UserLesson.id).label('total_lessons'),
        func.count(Score.id).label('total_games'),
        func.coalesce(UserStreak.current_streak, 0).label('current_streak'),
        func.count(UserBadge.id).label('badges_count')
    ).outerjoin(Score, User.id == Score.user_id).outerjoin(
        UserLesson, User.id == UserLesson.user_id
    ).outerjoin(UserStreak, User.id == UserStreak.user_id).outerjoin(
        UserBadge, User.id == UserBadge.user_id
    ).filter(
        User.is_active == True
    ).group_by(User.id, UserStreak.current_streak).order_by(
        desc('badges_count')
    ).limit(limit).all()
    
    result = []
    for rank, (user, total_points, total_lessons, total_games, current_streak, badges_count) in enumerate(leaderboard, 1):
        result.append({
            "rank": rank,
            "user": user,
            "total_points": int(total_points),
            "total_lessons": total_lessons,
            "total_games": total_games,
            "current_streak": current_streak
        })
    
    return result


@router.get("/my-position", response_model=dict)
async def get_my_position(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the current user's position in the leaderboard.
    """
    # Get user's total points
    user_points = db.query(func.coalesce(func.sum(Score.score), 0)).filter(
        Score.user_id == current_user.id
    ).scalar()
    
    # Count users with more points
    position = db.query(User).join(Score, User.id == Score.user_id).filter(
        User.is_active == True
    ).group_by(User.id).having(
        func.sum(Score.score) > user_points
    ).count() + 1
    
    # Get total active users
    total_users = db.query(User).filter(User.is_active == True).count()
    
    return {
        "position": position,
        "total_users": total_users,
        "total_points": int(user_points),
        "percentage": (position / total_users * 100) if total_users > 0 else 0
    }


@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get detailed statistics for the current user.
    """
    # Get total points
    total_points = db.query(func.coalesce(func.sum(Score.score), 0)).filter(
        Score.user_id == current_user.id
    ).scalar()
    
    # Get completed lessons
    total_lessons_completed = db.query(UserLesson).filter(
        UserLesson.user_id == current_user.id,
        UserLesson.completed == True
    ).count()
    
    # Get total games played
    total_games_played = db.query(Score).filter(
        Score.user_id == current_user.id
    ).count()
    
    # Get average score
    average_score = db.query(func.avg(Score.score)).filter(
        Score.user_id == current_user.id
    ).scalar() or 0
    
    # Get current streak
    user_streak = db.query(UserStreak).filter(
        UserStreak.user_id == current_user.id
    ).first()
    current_streak = user_streak.current_streak if user_streak else 0
    longest_streak = user_streak.longest_streak if user_streak else 0
    
    # Get badges count
    badges_count = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).count()
    
    # Calculate experience to next level
    experience_to_next_level = 100 - (current_user.experience % 100)
    
    return {
        "total_points": int(total_points),
        "total_lessons_completed": total_lessons_completed,
        "total_games_played": total_games_played,
        "average_score": float(average_score),
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "badges_count": badges_count,
        "level": current_user.level,
        "experience": current_user.experience,
        "experience_to_next_level": experience_to_next_level
    }


@router.get("/weekly", response_model=List[LeaderboardEntry])
async def get_weekly_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get weekly leaderboard (points earned in the last 7 days).
    
    - **limit**: Number of top users to return
    """
    from datetime import datetime, timedelta
    
    # Calculate date 7 days ago
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    leaderboard = db.query(
        User,
        func.coalesce(func.sum(Score.score), 0).label('weekly_points'),
        func.count(UserLesson.id).label('weekly_lessons'),
        func.count(Score.id).label('weekly_games'),
        func.coalesce(UserStreak.current_streak, 0).label('current_streak')
    ).outerjoin(Score, User.id == Score.user_id).outerjoin(
        UserLesson, User.id == UserLesson.user_id
    ).outerjoin(UserStreak, User.id == UserStreak.user_id).filter(
        User.is_active == True,
        Score.completed_at >= week_ago
    ).group_by(User.id, UserStreak.current_streak).order_by(
        desc('weekly_points')
    ).limit(limit).all()
    
    result = []
    for rank, (user, weekly_points, weekly_lessons, weekly_games, current_streak) in enumerate(leaderboard, 1):
        result.append({
            "rank": rank,
            "user": user,
            "total_points": int(weekly_points),
            "total_lessons": weekly_lessons,
            "total_games": weekly_games,
            "current_streak": current_streak
        })
    
    return result


@router.get("/monthly", response_model=List[LeaderboardEntry])
async def get_monthly_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get monthly leaderboard (points earned in the last 30 days).
    
    - **limit**: Number of top users to return
    """
    from datetime import datetime, timedelta
    
    # Calculate date 30 days ago
    month_ago = datetime.utcnow() - timedelta(days=30)
    
    leaderboard = db.query(
        User,
        func.coalesce(func.sum(Score.score), 0).label('monthly_points'),
        func.count(UserLesson.id).label('monthly_lessons'),
        func.count(Score.id).label('monthly_games'),
        func.coalesce(UserStreak.current_streak, 0).label('current_streak')
    ).outerjoin(Score, User.id == Score.user_id).outerjoin(
        UserLesson, User.id == UserLesson.user_id
    ).outerjoin(UserStreak, User.id == UserStreak.user_id).filter(
        User.is_active == True,
        Score.completed_at >= month_ago
    ).group_by(User.id, UserStreak.current_streak).order_by(
        desc('monthly_points')
    ).limit(limit).all()
    
    result = []
    for rank, (user, monthly_points, monthly_lessons, monthly_games, current_streak) in enumerate(leaderboard, 1):
        result.append({
            "rank": rank,
            "user": user,
            "total_points": int(monthly_points),
            "total_lessons": monthly_lessons,
            "total_games": monthly_games,
            "current_streak": current_streak
        })
    
    return result