from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.auth import get_current_active_user
from app.models import User, Badge, UserBadge, Score, UserLesson
from app.schemas import (
    BadgeCreate, BadgeUpdate, BadgeResponse, UserBadgeResponse,
    PaginatedResponse, MessageResponse
)

router = APIRouter(prefix="/badges", tags=["badges"])


@router.get("/", response_model=PaginatedResponse)
async def get_badges(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = Query(None),
    rarity: Optional[str] = Query(None, pattern="^(common|rare|epic|legendary)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all badges with optional filtering and pagination.
    
    - **skip**: Number of records to skip
    - **limit**: Number of records to return
    - **category**: Filter by category
    - **rarity**: Filter by rarity
    """
    query = db.query(Badge).filter(Badge.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(Badge.category == category)
    if rarity:
        query = query.filter(Badge.rarity == rarity)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    badges = query.offset(skip).limit(limit).all()
    
    return {
        "items": badges,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/my-badges", response_model=List[UserBadgeResponse])
async def get_my_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get badges earned by the current user.
    """
    user_badges = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).all()
    
    return user_badges


@router.get("/{badge_id}", response_model=BadgeResponse)
async def get_badge(
    badge_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific badge by ID.
    
    - **badge_id**: Badge ID
    """
    badge = db.query(Badge).filter(Badge.id == badge_id, Badge.is_active == True).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )
    
    return badge


@router.post("/", response_model=BadgeResponse, status_code=status.HTTP_201_CREATED)
async def create_badge(
    badge_data: BadgeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new badge (admin only).
    
    - **name**: Badge name
    - **description**: Badge description
    - **icon**: Badge icon (emoji or identifier)
    - **category**: Badge category
    - **rarity**: Badge rarity
    - **points_required**: Points required to unlock
    - **criteria_type**: Type of criteria for unlocking
    - **criteria_value**: Value needed to unlock badge
    """
    # TODO: Add admin role check
    badge = Badge(**badge_data.dict())
    db.add(badge)
    db.commit()
    db.refresh(badge)
    
    return badge


@router.put("/{badge_id}", response_model=BadgeResponse)
async def update_badge(
    badge_id: str,
    badge_data: BadgeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a badge (admin only).
    
    - **badge_id**: Badge ID
    """
    # TODO: Add admin role check
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )
    
    update_data = badge_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(badge, field, value)
    
    db.commit()
    db.refresh(badge)
    
    return badge


@router.delete("/{badge_id}", response_model=MessageResponse)
async def delete_badge(
    badge_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a badge (admin only).
    
    - **badge_id**: Badge ID
    """
    # TODO: Add admin role check
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if not badge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Badge not found"
        )
    
    # Soft delete by setting is_active to False
    badge.is_active = False
    db.commit()
    
    return {"message": "Badge deleted successfully"}


@router.post("/{badge_id}/award", response_model=UserBadgeResponse)
async def award_badge(
    badge_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Award a badge to the current user (admin only).
    
    - **badge_id**: Badge ID
    """
    # TODO: Add admin role check
    
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
    
    # Award the badge
    user_badge = UserBadge(
        user_id=current_user.id,
        badge_id=badge_id
    )
    db.add(user_badge)
    db.commit()
    db.refresh(user_badge)
    
    return user_badge


@router.get("/categories/stats", response_model=dict)
async def get_badge_category_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get statistics for badge categories.
    """
    stats = db.query(
        Badge.category,
        func.count(Badge.id).label('total_badges'),
        func.count(UserBadge.id).label('earned_badges')
    ).outerjoin(UserBadge, Badge.id == UserBadge.badge_id).filter(
        Badge.is_active == True
    ).group_by(Badge.category).all()
    
    return {
        "categories": [
            {
                "category": stat.category,
                "total_badges": stat.total_badges,
                "earned_badges": stat.earned_badges
            }
            for stat in stats
        ]
    }


@router.get("/rarity/stats", response_model=dict)
async def get_badge_rarity_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get statistics for badge rarities.
    """
    stats = db.query(
        Badge.rarity,
        func.count(Badge.id).label('total_badges'),
        func.count(UserBadge.id).label('earned_badges')
    ).outerjoin(UserBadge, Badge.id == UserBadge.badge_id).filter(
        Badge.is_active == True
    ).group_by(Badge.rarity).all()
    
    return {
        "rarities": [
            {
                "rarity": stat.rarity,
                "total_badges": stat.total_badges,
                "earned_badges": stat.earned_badges
            }
            for stat in stats
        ]
    }


@router.post("/check-achievements", response_model=List[UserBadgeResponse])
async def check_and_award_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Check and award achievements based on user progress.
    """
    awarded_badges = []
    
    # Get all active badges
    badges = db.query(Badge).filter(Badge.is_active == True).all()
    
    for badge in badges:
        # Check if user already has this badge
        existing_user_badge = db.query(UserBadge).filter(
            UserBadge.user_id == current_user.id,
            UserBadge.badge_id == badge.id
        ).first()
        
        if existing_user_badge:
            continue
        
        # Check if user meets criteria
        if badge.criteria_type == "points":
            if current_user.points >= badge.criteria_value:
                user_badge = UserBadge(
                    user_id=current_user.id,
                    badge_id=badge.id
                )
                db.add(user_badge)
                awarded_badges.append(user_badge)
        
        elif badge.criteria_type == "lessons_completed":
            completed_lessons = db.query(UserLesson).filter(
                UserLesson.user_id == current_user.id,
                UserLesson.completed == True
            ).count()
            if completed_lessons >= badge.criteria_value:
                user_badge = UserBadge(
                    user_id=current_user.id,
                    badge_id=badge.id
                )
                db.add(user_badge)
                awarded_badges.append(user_badge)
        
        elif badge.criteria_type == "games_won":
            # Count quizzes with score >= 80%
            games_won = db.query(Score).filter(
                Score.user_id == current_user.id,
                Score.score >= 80
            ).count()
            if games_won >= badge.criteria_value:
                user_badge = UserBadge(
                    user_id=current_user.id,
                    badge_id=badge.id
                )
                db.add(user_badge)
                awarded_badges.append(user_badge)
        
        elif badge.criteria_type == "streak_days":
            # TODO: Implement streak checking logic
            pass
    
    if awarded_badges:
        db.commit()
        for user_badge in awarded_badges:
            db.refresh(user_badge)
    
    return awarded_badges


@router.get("/progress/summary", response_model=dict)
async def get_badge_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a summary of badge progress for the current user.
    """
    # Get total badges
    total_badges = db.query(Badge).filter(Badge.is_active == True).count()
    
    # Get earned badges
    earned_badges = db.query(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).count()
    
    # Get badges by rarity
    rarity_stats = db.query(
        Badge.rarity,
        func.count(Badge.id).label('total'),
        func.count(UserBadge.id).label('earned')
    ).outerjoin(UserBadge, Badge.id == UserBadge.badge_id).filter(
        Badge.is_active == True
    ).group_by(Badge.rarity).all()
    
    return {
        "total_badges": total_badges,
        "earned_badges": earned_badges,
        "progress_percentage": (earned_badges / total_badges * 100) if total_badges > 0 else 0,
        "rarity_breakdown": [
            {
                "rarity": stat.rarity,
                "total": stat.total,
                "earned": stat.earned,
                "progress": (stat.earned / stat.total * 100) if stat.total > 0 else 0
            }
            for stat in rarity_stats
        ]
    }