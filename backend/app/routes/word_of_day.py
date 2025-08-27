from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date
from ..database import get_db
from ..auth import get_current_active_user
from ..models import WordOfDay, User
from ..schemas import WordOfDayResponse, WordOfDayCreate

router = APIRouter(prefix="/word-of-day", tags=["word of day"])

@router.get("/", response_model=WordOfDayResponse)
def get_todays_word(db: Session = Depends(get_db)):
    """
    Get today's word of the day.
    """
    today = date.today()
    
    word_of_day = db.query(WordOfDay).filter(
        func.date(WordOfDay.date) == today,
        WordOfDay.is_active == True
    ).first()
    
    if not word_of_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No word of the day found for today"
        )
    
    return word_of_day

@router.get("/{word_date}", response_model=WordOfDayResponse)
def get_word_by_date(word_date: date, db: Session = Depends(get_db)):
    """
    Get word of the day for a specific date.
    
    - **word_date**: Date in YYYY-MM-DD format
    """
    word_of_day = db.query(WordOfDay).filter(
        func.date(WordOfDay.date) == word_date,
        WordOfDay.is_active == True
    ).first()
    
    if not word_of_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No word of the day found for {word_date}"
        )
    
    return word_of_day

@router.get("/history", response_model=List[WordOfDayResponse])
def get_word_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get recent words of the day.
    
    - **skip**: Number of words to skip
    - **limit**: Maximum number of words to return
    """
    words = db.query(WordOfDay).filter(
        WordOfDay.is_active == True
    ).order_by(WordOfDay.date.desc()).offset(skip).limit(limit).all()
    
    return words

@router.post("/", response_model=WordOfDayResponse, status_code=status.HTTP_201_CREATED)
def create_word_of_day(
    word: WordOfDayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new word of the day (admin only).
    """
    # Check if word already exists for this date
    existing_word = db.query(WordOfDay).filter(
        func.date(WordOfDay.date) == func.date(word.date)
    ).first()
    
    if existing_word:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word of the day already exists for this date"
        )
    
    db_word = WordOfDay(**word.dict())
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word

@router.put("/{word_id}", response_model=WordOfDayResponse)
def update_word_of_day(
    word_id: int,
    word_update: WordOfDayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a word of the day (admin only).
    """
    db_word = db.query(WordOfDay).filter(WordOfDay.id == word_id).first()
    if not db_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word of the day not found"
        )
    
    # Check if the new date conflicts with another word
    if word_update.date != db_word.date:
        existing_word = db.query(WordOfDay).filter(
            func.date(WordOfDay.date) == func.date(word_update.date),
            WordOfDay.id != word_id
        ).first()
        
        if existing_word:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Word of the day already exists for this date"
            )
    
    # Update the word
    for field, value in word_update.dict().items():
        setattr(db_word, field, value)
    
    db.commit()
    db.refresh(db_word)
    return db_word

@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word_of_day(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a word of the day (admin only).
    """
    db_word = db.query(WordOfDay).filter(WordOfDay.id == word_id).first()
    if not db_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word of the day not found"
        )
    
    # Soft delete
    db_word.is_active = False
    db.commit()
    return None

@router.get("/random", response_model=WordOfDayResponse)
def get_random_word(db: Session = Depends(get_db)):
    """
    Get a random word of the day from history.
    """
    word = db.query(WordOfDay).filter(
        WordOfDay.is_active == True
    ).order_by(func.random()).first()
    
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No words of the day found"
        )
    
    return word

@router.get("/search", response_model=List[WordOfDayResponse])
def search_words(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Search words of the day by word or meaning.
    
    - **q**: Search query
    - **skip**: Number of results to skip
    - **limit**: Maximum number of results to return
    """
    search_term = f"%{q}%"
    
    words = db.query(WordOfDay).filter(
        WordOfDay.is_active == True,
        (WordOfDay.word.ilike(search_term) | 
         WordOfDay.meaning.ilike(search_term) |
         WordOfDay.example_sentence.ilike(search_term))
    ).order_by(WordOfDay.date.desc()).offset(skip).limit(limit).all()
    
    return words

@router.get("/categories", response_model=List[str])
def get_word_categories(db: Session = Depends(get_db)):
    """
    Get all available word categories.
    """
    categories = db.query(WordOfDay.category).filter(
        WordOfDay.is_active == True,
        WordOfDay.category.isnot(None)
    ).distinct().all()
    return [category[0] for category in categories]

@router.get("/difficulties", response_model=List[str])
def get_word_difficulties(db: Session = Depends(get_db)):
    """
    Get all available word difficulties.
    """
    difficulties = db.query(WordOfDay.difficulty).filter(
        WordOfDay.is_active == True
    ).distinct().all()
    return [difficulty[0] for difficulty in difficulties]