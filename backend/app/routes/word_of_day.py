from datetime import datetime, date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.auth import get_current_active_user
from app.models import User, WordOfDay
from app.schemas import (
    WordOfDayCreate, WordOfDayUpdate, WordOfDayResponse,
    PaginatedResponse, MessageResponse
)

router = APIRouter(prefix="/word-of-day", tags=["word of day"])


@router.get("/today", response_model=WordOfDayResponse)
async def get_todays_word(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get today's word of the day.
    """
    today = date.today()
    word_of_day = db.query(WordOfDay).filter(
        WordOfDay.date == today,
        WordOfDay.is_active == True
    ).first()
    
    if not word_of_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No word of the day found for today"
        )
    
    return word_of_day


@router.get("/", response_model=PaginatedResponse)
async def get_words_of_day(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    difficulty: Optional[str] = Query(None, pattern="^(beginner|intermediate|advanced)$"),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get words of the day with optional filtering and pagination.
    
    - **skip**: Number of records to skip
    - **limit**: Number of records to return
    - **difficulty**: Filter by difficulty
    - **category**: Filter by category
    """
    query = db.query(WordOfDay).filter(WordOfDay.is_active == True)
    
    # Apply filters
    if difficulty:
        query = query.filter(WordOfDay.difficulty == difficulty)
    if category:
        query = query.filter(WordOfDay.category == category)
    
    # Order by date (newest first)
    query = query.order_by(WordOfDay.date.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    words = query.offset(skip).limit(limit).all()
    
    return {
        "items": words,
        "total": total,
        "page": skip // limit + 1,
        "size": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{word_id}", response_model=WordOfDayResponse)
async def get_word_of_day(
    word_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific word of the day by ID.
    
    - **word_id**: Word of the day ID
    """
    word = db.query(WordOfDay).filter(
        WordOfDay.id == word_id,
        WordOfDay.is_active == True
    ).first()
    
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word of the day not found"
        )
    
    return word


@router.post("/", response_model=WordOfDayResponse, status_code=status.HTTP_201_CREATED)
async def create_word_of_day(
    word_data: WordOfDayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new word of the day (admin only).
    
    - **word**: The word
    - **meaning**: Word meaning
    - **example_sentence**: Example sentence
    - **pronunciation**: Pronunciation guide
    - **difficulty**: Difficulty level
    - **category**: Word category
    - **date**: Date for the word
    """
    # TODO: Add admin role check
    
    # Check if word already exists for the given date
    existing_word = db.query(WordOfDay).filter(
        WordOfDay.date == word_data.date
    ).first()
    
    if existing_word:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word of the day already exists for this date"
        )
    
    word = WordOfDay(**word_data.dict())
    db.add(word)
    db.commit()
    db.refresh(word)
    
    return word


@router.put("/{word_id}", response_model=WordOfDayResponse)
async def update_word_of_day(
    word_id: str,
    word_data: WordOfDayUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a word of the day (admin only).
    
    - **word_id**: Word of the day ID
    """
    # TODO: Add admin role check
    
    word = db.query(WordOfDay).filter(WordOfDay.id == word_id).first()
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word of the day not found"
        )
    
    update_data = word_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(word, field, value)
    
    db.commit()
    db.refresh(word)
    
    return word


@router.delete("/{word_id}", response_model=MessageResponse)
async def delete_word_of_day(
    word_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a word of the day (admin only).
    
    - **word_id**: Word of the day ID
    """
    # TODO: Add admin role check
    
    word = db.query(WordOfDay).filter(WordOfDay.id == word_id).first()
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word of the day not found"
        )
    
    # Soft delete by setting is_active to False
    word.is_active = False
    db.commit()
    
    return {"message": "Word of the day deleted successfully"}


@router.get("/calendar/{year}/{month}", response_model=List[WordOfDayResponse])
async def get_monthly_words(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all words of the day for a specific month.
    
    - **year**: Year
    - **month**: Month (1-12)
    """
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid month. Must be between 1 and 12."
        )
    
    # Get first and last day of the month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month + 1, 1) - timedelta(days=1)
    
    words = db.query(WordOfDay).filter(
        WordOfDay.date >= first_day,
        WordOfDay.date <= last_day,
        WordOfDay.is_active == True
    ).order_by(WordOfDay.date).all()
    
    return words


@router.get("/stats/summary", response_model=dict)
async def get_word_of_day_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get statistics for words of the day.
    """
    # Get total words
    total_words = db.query(WordOfDay).filter(WordOfDay.is_active == True).count()
    
    # Get words by difficulty
    difficulty_stats = db.query(
        WordOfDay.difficulty,
        func.count(WordOfDay.id).label('count')
    ).filter(WordOfDay.is_active == True).group_by(WordOfDay.difficulty).all()
    
    # Get words by category
    category_stats = db.query(
        WordOfDay.category,
        func.count(WordOfDay.id).label('count')
    ).filter(WordOfDay.is_active == True).group_by(WordOfDay.category).all()
    
    return {
        "total_words": total_words,
        "difficulty_breakdown": [
            {
                "difficulty": stat.difficulty,
                "count": stat.count
            }
            for stat in difficulty_stats
        ],
        "category_breakdown": [
            {
                "category": stat.category,
                "count": stat.count
            }
            for stat in category_stats
        ]
    }


@router.get("/random", response_model=WordOfDayResponse)
async def get_random_word(
    difficulty: Optional[str] = Query(None, pattern="^(beginner|intermediate|advanced)$"),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a random word of the day.
    
    - **difficulty**: Optional difficulty filter
    - **category**: Optional category filter
    """
    query = db.query(WordOfDay).filter(WordOfDay.is_active == True)
    
    # Apply filters
    if difficulty:
        query = query.filter(WordOfDay.difficulty == difficulty)
    if category:
        query = query.filter(WordOfDay.category == category)
    
    # Get random word
    word = query.order_by(func.random()).first()
    
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No words found with the specified criteria"
        )
    
    return word