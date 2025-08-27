#!/usr/bin/env python3
"""
Seed data script for the English Learning API.
This script populates the database with initial data for testing and development.
"""

import asyncio
from datetime import datetime, date
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Quiz, Badge, WordOfDay, UserStreak
from app.auth import get_password_hash

def create_seed_data():
    """Create seed data for the database."""
    db = SessionLocal()
    
    try:
        # Create users
        print("Creating users...")
        users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password_hash": get_password_hash("admin123"),
                "first_name": "Admin",
                "last_name": "User",
                "points": 1000,
                "level": 10,
                "experience": 950,
                "is_verified": True
            },
            {
                "username": "student1",
                "email": "student1@example.com",
                "password_hash": get_password_hash("password123"),
                "first_name": "John",
                "last_name": "Doe",
                "points": 250,
                "level": 3,
                "experience": 250,
                "is_verified": True
            },
            {
                "username": "student2",
                "email": "student2@example.com",
                "password_hash": get_password_hash("password123"),
                "first_name": "Jane",
                "last_name": "Smith",
                "points": 180,
                "level": 2,
                "experience": 180,
                "is_verified": True
            },
            {
                "username": "student3",
                "email": "student3@example.com",
                "password_hash": get_password_hash("password123"),
                "first_name": "Mike",
                "last_name": "Johnson",
                "points": 320,
                "level": 4,
                "experience": 320,
                "is_verified": True
            }
        ]
        
        for user_data in users:
            user = User(**user_data)
            db.add(user)
        db.commit()
        
        # Create quizzes
        print("Creating quizzes...")
        quizzes = [
            {
                "title": "Basic Vocabulary Quiz",
                "description": "Test your knowledge of basic English vocabulary",
                "category": "vocabulary",
                "difficulty": "beginner",
                "questions": [
                    {
                        "question": "What color is the sky on a sunny day?",
                        "options": ["Red", "Blue", "Green", "Yellow"],
                        "correct_answer": 1,
                        "explanation": "The sky appears blue due to the scattering of sunlight by the atmosphere."
                    },
                    {
                        "question": "Which animal says 'meow'?",
                        "options": ["Dog", "Cat", "Bird", "Fish"],
                        "correct_answer": 1,
                        "explanation": "Cats make a 'meow' sound to communicate with humans."
                    },
                    {
                        "question": "What do you use to write on paper?",
                        "options": ["Fork", "Pen", "Shoe", "Book"],
                        "correct_answer": 1,
                        "explanation": "A pen is a writing instrument used to apply ink to paper."
                    }
                ],
                "time_limit": 5,
                "points_reward": 10
            },
            {
                "title": "Grammar Basics",
                "description": "Learn basic English grammar rules",
                "category": "grammar",
                "difficulty": "beginner",
                "questions": [
                    {
                        "question": "Complete the sentence: 'I ___ to school every day.'",
                        "options": ["go", "goes", "going", "went"],
                        "correct_answer": 0,
                        "explanation": "Use 'go' for first person singular present tense."
                    },
                    {
                        "question": "Which word is correct? 'She ___ a beautiful dress.'",
                        "options": ["wear", "wears", "wearing", "wore"],
                        "correct_answer": 1,
                        "explanation": "Use 'wears' for third person singular present tense."
                    },
                    {
                        "question": "Choose the right form: 'They ___ playing in the park.'",
                        "options": ["is", "are", "am", "be"],
                        "correct_answer": 1,
                        "explanation": "Use 'are' for plural subjects."
                    }
                ],
                "time_limit": 8,
                "points_reward": 15
            },
            {
                "title": "Common Phrases",
                "description": "Learn everyday English phrases",
                "category": "phrases",
                "difficulty": "beginner",
                "questions": [
                    {
                        "question": "What do you say when you meet someone for the first time?",
                        "options": ["Goodbye", "Nice to meet you", "Thank you", "Please"],
                        "correct_answer": 1,
                        "explanation": "'Nice to meet you' is a common greeting when meeting someone new."
                    },
                    {
                        "question": "What do you say when someone helps you?",
                        "options": ["Sorry", "Thank you", "Please", "Goodbye"],
                        "correct_answer": 1,
                        "explanation": "'Thank you' is the polite response when someone helps you."
                    },
                    {
                        "question": "What do you say when you leave?",
                        "options": ["Hello", "Goodbye", "Please", "Thank you"],
                        "correct_answer": 1,
                        "explanation": "'Goodbye' is used when leaving or ending a conversation."
                    }
                ],
                "time_limit": 6,
                "points_reward": 12
            },
            {
                "title": "Intermediate Vocabulary",
                "description": "Test your intermediate vocabulary skills",
                "category": "vocabulary",
                "difficulty": "intermediate",
                "questions": [
                    {
                        "question": "What is a synonym for 'happy'?",
                        "options": ["Sad", "Joyful", "Angry", "Tired"],
                        "correct_answer": 1,
                        "explanation": "'Joyful' is a synonym for 'happy'."
                    },
                    {
                        "question": "What does 'enormous' mean?",
                        "options": ["Small", "Big", "Very big", "Medium"],
                        "correct_answer": 2,
                        "explanation": "'Enormous' means very big or huge."
                    },
                    {
                        "question": "What is the opposite of 'fast'?",
                        "options": ["Quick", "Slow", "Fast", "Speed"],
                        "correct_answer": 1,
                        "explanation": "'Slow' is the opposite of 'fast'."
                    }
                ],
                "time_limit": 7,
                "points_reward": 20
            }
        ]
        
        for quiz_data in quizzes:
            quiz = Quiz(**quiz_data)
            db.add(quiz)
        db.commit()
        
        # Create badges
        print("Creating badges...")
        badges = [
            {
                "name": "First Steps",
                "description": "Complete your first lesson",
                "icon": "🎯",
                "category": "beginner",
                "rarity": "common",
                "points_required": 0,
                "criteria_type": "lessons_completed",
                "criteria_value": 1
            },
            {
                "name": "Vocabulary Master",
                "description": "Learn 100 new words",
                "icon": "📚",
                "category": "vocabulary",
                "rarity": "rare",
                "points_required": 100,
                "criteria_type": "points",
                "criteria_value": 100
            },
            {
                "name": "Grammar Guru",
                "description": "Complete 10 grammar lessons",
                "icon": "📝",
                "category": "grammar",
                "rarity": "epic",
                "points_required": 200,
                "criteria_type": "lessons_completed",
                "criteria_value": 10
            },
            {
                "name": "Game Champion",
                "description": "Win 50 games",
                "icon": "🏆",
                "category": "games",
                "rarity": "legendary",
                "points_required": 500,
                "criteria_type": "games_won",
                "criteria_value": 50
            },
            {
                "name": "Perfect Score",
                "description": "Get 100% on any quiz",
                "icon": "⭐",
                "category": "achievement",
                "rarity": "rare",
                "points_required": 50,
                "criteria_type": "perfect_score",
                "criteria_value": 1
            },
            {
                "name": "Streak Master",
                "description": "Study for 7 days in a row",
                "icon": "🔥",
                "category": "streak",
                "rarity": "epic",
                "points_required": 150,
                "criteria_type": "streak_days",
                "criteria_value": 7
            },
            {
                "name": "Social Butterfly",
                "description": "Complete 5 lessons with friends",
                "icon": "🦋",
                "category": "social",
                "rarity": "rare",
                "points_required": 100,
                "criteria_type": "social_lessons",
                "criteria_value": 5
            },
            {
                "name": "Speed Learner",
                "description": "Complete 3 lessons in one day",
                "icon": "⚡",
                "category": "speed",
                "rarity": "epic",
                "points_required": 200,
                "criteria_type": "daily_lessons",
                "criteria_value": 3
            }
        ]
        
        for badge_data in badges:
            badge = Badge(**badge_data)
            db.add(badge)
        db.commit()
        
        # Create words of the day
        print("Creating words of the day...")
        words_of_day = [
            {
                "word": "Serendipity",
                "meaning": "The occurrence and development of events by chance in a happy or beneficial way",
                "example_sentence": "Finding that book was pure serendipity - I wasn't even looking for it!",
                "pronunciation": "/ˌserənˈdipədē/",
                "difficulty": "advanced",
                "category": "vocabulary",
                "date": date.today()
            },
            {
                "word": "Perseverance",
                "meaning": "Persistence in doing something despite difficulty or delay in achieving success",
                "example_sentence": "Her perseverance in learning English paid off when she got the job.",
                "pronunciation": "/ˌpərsəˈvirəns/",
                "difficulty": "intermediate",
                "category": "vocabulary",
                "date": date.today() - timedelta(days=1)
            },
            {
                "word": "Ubiquitous",
                "meaning": "Present, appearing, or found everywhere",
                "example_sentence": "Smartphones have become ubiquitous in modern society.",
                "pronunciation": "/yo͞oˈbikwədəs/",
                "difficulty": "advanced",
                "category": "vocabulary",
                "date": date.today() - timedelta(days=2)
            },
            {
                "word": "Resilient",
                "meaning": "Able to withstand or recover quickly from difficult conditions",
                "example_sentence": "Children are often more resilient than adults when facing challenges.",
                "pronunciation": "/rəˈzilyənt/",
                "difficulty": "intermediate",
                "category": "vocabulary",
                "date": date.today() - timedelta(days=3)
            },
            {
                "word": "Eloquent",
                "meaning": "Fluent or persuasive in speaking or writing",
                "example_sentence": "She gave an eloquent speech about the importance of education.",
                "pronunciation": "/ˈeləkwənt/",
                "difficulty": "intermediate",
                "category": "vocabulary",
                "date": date.today() - timedelta(days=4)
            }
        ]
        
        for word_data in words_of_day:
            word = WordOfDay(**word_data)
            db.add(word)
        db.commit()
        
        # Create user streaks
        print("Creating user streaks...")
        user_streaks = [
            {
                "user_id": db.query(User).filter(User.username == "student1").first().id,
                "current_streak": 5,
                "longest_streak": 12,
                "last_activity_date": datetime.utcnow()
            },
            {
                "user_id": db.query(User).filter(User.username == "student2").first().id,
                "current_streak": 3,
                "longest_streak": 8,
                "last_activity_date": datetime.utcnow()
            },
            {
                "user_id": db.query(User).filter(User.username == "student3").first().id,
                "current_streak": 7,
                "longest_streak": 15,
                "last_activity_date": datetime.utcnow()
            }
        ]
        
        for streak_data in user_streaks:
            streak = UserStreak(**streak_data)
            db.add(streak)
        db.commit()
        
        print("Seed data created successfully!")
        
    except Exception as e:
        print(f"Error creating seed data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_seed_data()