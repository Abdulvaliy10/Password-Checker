from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from ..auth import get_current_active_user
from ..models import Badge, UserBadge, User
from ..schemas import BadgeResponse, BadgeCreate, UserBadgeResponse

router = APIRouter(prefix="/badges", tags=["badges"])

@router.get("/", response_model=List[BadgeResponse])
def get_badges(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all badges with optional filtering.
    
    - **skip**: Number of badges to skip
    - **limit**: Maximum number of badges to return
    - **category**: Filter by category (achievement, milestone, special)
    """
    query = db.query(Badge).filter(Badge.is_active == True)
    
    if category:
        query = query.filter(Badge.category == category)
    
    badges = query.offset(skip).limit(limit).all()
    return badges

@router.get("/{badge_id}", response_model=BadgeResponse)
def get_badge(badge_id: int, db: Session = Depends(get_db)):
    """
    Get a specific badge by ID.
    """
    badge = db.query(Badge).filter(Badge.id == badge_id, Badge.is_active == True).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )
    return badge

@router.post("/", response_model=BadgeResponse, status_code=status.HTTP_201_CREATED)
def create_badge(
    badge: BadgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new badge (admin only).
    """
    # Check if badge name already exists
    existing_badge = db.query(Badge).filter(Badge.name == badge.name).first()
    if existing_badge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Badge name already exists"
        )
    
    db_badge = Badge(**badge.dict())
    db.add(db_badge)
    db.commit()
    db.refresh(db_badge)
    return db_badge

@router.get("/user/earned", response_model=List[UserBadgeResponse])
def get_user_badges(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get badges earned by current user.
    
    - **skip**: Number of badges to skip
    - **limit**: Maximum number of badges to return
    """
    user_badges = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).order_by(UserBadge.earned_at.desc()).offset(skip).limit(limit).all()
    
    return user_badges

@router.get("/user/available", response_model=List[BadgeResponse])
def get_available_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get badges that the current user can earn.
    """
    # Get all badges
    all_badges = db.query(Badge).filter(Badge.is_active == True).all()
    
    # Get user's earned badges
    earned_badge_ids = db.query(UserBadge.badge_id).filter(
        UserBadge.user_id == current_user.id
    ).all()
    earned_badge_ids = [badge_id[0] for badge_id in earned_badge_ids]
    
    # Filter out already earned badges
    available_badges = [badge for badge in all_badges if badge.id not in earned_badge_ids]
    
    return available_badges

@router.post("/user/{badge_id}/award", response_model=UserBadgeResponse)
def award_badge_to_user(
    badge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Award a badge to the current user (admin only).
    """
    # Check if badge exists
    badge = db.query(Badge).filter(Badge.id == badge_id, Badge.is_active == True).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )
    
    # Check if user already has this badge
    existing_user_badge = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id,
        UserBadge.badge_id == badge_id
    ).first()
    
    if existing_user_badge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this badge"
        )
    
    # Check if user meets requirements
    if current_user.points < badge.points_required:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User needs {badge.points_required} points to earn this badge"
        )
    
    # Award the badge
    user_badge = UserBadge(
        user_id=current_user.id,
        badge_id=badge_id
    )
    db.add(user_badge)
    db.commit()
    db.refresh(user_badge)
    
    return user_badge

@router.get("/categories", response_model=List[str])
def get_badge_categories(db: Session = Depends(get_db)):
    """
    Get all available badge categories.
    """
    categories = db.query(Badge.category).filter(
        Badge.is_active == True,
        Badge.category.isnot(None)
    ).distinct().all()
    return [category[0] for category in categories]

@router.get("/user/{user_id}", response_model=List[UserBadgeResponse])
def get_user_badges_by_id(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get badges earned by a specific user.
    
    - **user_id**: ID of the user
    - **skip**: Number of badges to skip
    - **limit**: Maximum number of badges to return
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_badges = db.query(UserBadge).filter(
        UserBadge.user_id == user_id
    ).order_by(UserBadge.earned_at.desc()).offset(skip).limit(limit).all()
    
    return user_badges

@router.delete("/user/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user_badge(
    badge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove a badge from the current user (admin only).
    """
    user_badge = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id,
        UserBadge.badge_id == badge_id
    ).first()
    
    if not user_badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User badge not found"
        )
    
    db.delete(user_badge)
    db.commit()
    return None