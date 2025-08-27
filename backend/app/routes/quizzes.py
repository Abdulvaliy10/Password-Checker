from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from ..database import get_db
from ..auth import get_current_active_user
from ..models import Quiz, Score, User
from ..schemas import QuizResponse, QuizCreate, QuizUpdate, QuizSubmission, ScoreResponse

router = APIRouter(prefix="/quizzes", tags=["quizzes"])

@router.get("/", response_model=List[QuizResponse])
def get_quizzes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all quizzes with optional filtering.
    
    - **skip**: Number of quizzes to skip
    - **limit**: Maximum number of quizzes to return
    - **category**: Filter by category (grammar, vocabulary, reading, etc.)
    - **difficulty**: Filter by difficulty (easy, medium, hard)
    """
    query = db.query(Quiz).filter(Quiz.is_active == True)
    
    if category:
        query = query.filter(Quiz.category == category)
    if difficulty:
        query = query.filter(Quiz.difficulty == difficulty)
    
    quizzes = query.offset(skip).limit(limit).all()
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """
    Get a specific quiz by ID.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    return quiz

@router.post("/", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
def create_quiz(
    quiz: QuizCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new quiz (admin only).
    """
    # In a real app, you'd check if user is admin
    # For now, we'll allow any authenticated user to create quizzes
    
    # Validate JSON strings
    try:
        json.loads(quiz.questions)
        json.loads(quiz.correct_answers)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON format for questions or correct_answers"
        )
    
    db_quiz = Quiz(**quiz.dict())
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.put("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: int,
    quiz_update: QuizUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a quiz (admin only).
    """
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Validate JSON strings if provided
    update_data = quiz_update.dict(exclude_unset=True)
    if "questions" in update_data:
        try:
            json.loads(update_data["questions"])
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format for questions"
            )
    
    if "correct_answers" in update_data:
        try:
            json.loads(update_data["correct_answers"])
        except json.JSONDecodeError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid JSON format for correct_answers"
            )
    
    for field, value in update_data.items():
        setattr(db_quiz, field, value)
    
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    quiz_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a quiz (admin only).
    """
    db_quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not db_quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Soft delete - just mark as inactive
    db_quiz.is_active = False
    db.commit()
    return None

@router.post("/{quiz_id}/submit", response_model=ScoreResponse)
def submit_quiz(
    quiz_id: int,
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Submit quiz answers and get score.
    """
    # Get the quiz
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id, Quiz.is_active == True).first()
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Parse quiz data
    try:
        questions = json.loads(quiz.questions)
        correct_answers = json.loads(quiz.correct_answers)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid quiz data"
        )
    
    # Calculate score
    correct_count = 0
    total_questions = len(questions)
    
    for i, question in enumerate(questions):
        question_id = str(i)
        if question_id in submission.answers:
            user_answer = submission.answers[question_id]
            correct_answer = correct_answers.get(question_id)
            if user_answer == correct_answer:
                correct_count += 1
    
    score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    
    # Calculate points earned
    points_earned = int(score_percentage / 100 * quiz.points_reward)
    
    # Update user points
    current_user.points += points_earned
    
    # Create score record
    score = Score(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score_percentage,
        time_taken=submission.time_taken,
        answers=json.dumps(submission.answers)
    )
    
    db.add(score)
    db.commit()
    db.refresh(score)
    
    return score

@router.get("/categories", response_model=List[str])
def get_quiz_categories(db: Session = Depends(get_db)):
    """
    Get all available quiz categories.
    """
    categories = db.query(Quiz.category).filter(Quiz.is_active == True).distinct().all()
    return [category[0] for category in categories]

@router.get("/difficulties", response_model=List[str])
def get_quiz_difficulties(db: Session = Depends(get_db)):
    """
    Get all available quiz difficulties.
    """
    difficulties = db.query(Quiz.difficulty).filter(Quiz.is_active == True).distinct().all()
    return [difficulty[0] for difficulty in difficulties]