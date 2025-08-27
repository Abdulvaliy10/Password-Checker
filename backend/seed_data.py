#!/usr/bin/env python3
"""
Seed data script for English Learning API
Run this script to populate the database with initial data
"""

import json
import sys
import os
from datetime import datetime, date, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import User, Quiz, Badge, WordOfDay, Score, UserBadge
from app.auth import get_password_hash

def create_sample_users():
    """Create sample users"""
    users_data = [
        {
            "username": "alice",
            "email": "alice@example.com",
            "password": "password123",
            "points": 150,
            "level": 2
        },
        {
            "username": "bob",
            "email": "bob@example.com",
            "password": "password123",
            "points": 75,
            "level": 1
        },
        {
            "username": "charlie",
            "email": "charlie@example.com",
            "password": "password123",
            "points": 300,
            "level": 4
        },
        {
            "username": "diana",
            "email": "diana@example.com",
            "password": "password123",
            "points": 200,
            "level": 3
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password_hash=get_password_hash(user_data["password"]),
            points=user_data["points"],
            level=user_data["level"]
        )
        users.append(user)
    
    return users

def create_sample_quizzes():
    """Create sample quizzes"""
    quizzes_data = [
        {
            "title": "Basic Grammar Quiz",
            "description": "Test your knowledge of basic English grammar",
            "category": "grammar",
            "difficulty": "easy",
            "questions": json.dumps([
                {
                    "id": "0",
                    "question": "Which of the following is a correct sentence?",
                    "options": [
                        "I am going to the store.",
                        "I going to the store.",
                        "I goes to the store.",
                        "I go to the store yesterday."
                    ],
                    "type": "multiple_choice"
                },
                {
                    "id": "1",
                    "question": "Choose the correct form of the verb: She ___ to school every day.",
                    "options": ["go", "goes", "going", "went"],
                    "type": "multiple_choice"
                }
            ]),
            "correct_answers": json.dumps({
                "0": "0",
                "1": "1"
            }),
            "time_limit": 300,
            "points_reward": 10
        },
        {
            "title": "Vocabulary Builder",
            "description": "Learn new English vocabulary words",
            "category": "vocabulary",
            "difficulty": "medium",
            "questions": json.dumps([
                {
                    "id": "0",
                    "question": "What does 'ubiquitous' mean?",
                    "options": [
                        "Rare and unusual",
                        "Present everywhere",
                        "Very expensive",
                        "Extremely small"
                    ],
                    "type": "multiple_choice"
                },
                {
                    "id": "1",
                    "question": "Choose the synonym for 'enormous':",
                    "options": ["tiny", "huge", "average", "small"],
                    "type": "multiple_choice"
                }
            ]),
            "correct_answers": json.dumps({
                "0": "1",
                "1": "1"
            }),
            "time_limit": 240,
            "points_reward": 15
        },
        {
            "title": "Reading Comprehension",
            "description": "Test your reading comprehension skills",
            "category": "reading",
            "difficulty": "hard",
            "questions": json.dumps([
                {
                    "id": "0",
                    "question": "Read the passage and answer: What is the main idea?",
                    "passage": "The Industrial Revolution was a period of major industrialization and innovation during the late 18th and early 19th centuries. The Industrial Revolution began in Great Britain and quickly spread throughout the world.",
                    "options": [
                        "The Industrial Revolution was only in Great Britain",
                        "The Industrial Revolution was a time of change and innovation",
                        "The Industrial Revolution happened in the 20th century",
                        "The Industrial Revolution was not important"
                    ],
                    "type": "multiple_choice"
                }
            ]),
            "correct_answers": json.dumps({
                "0": "1"
            }),
            "time_limit": 600,
            "points_reward": 20
        }
    ]
    
    quizzes = []
    for quiz_data in quizzes_data:
        quiz = Quiz(**quiz_data)
        quizzes.append(quiz)
    
    return quizzes

def create_sample_badges():
    """Create sample badges"""
    badges_data = [
        {
            "name": "First Steps",
            "description": "Complete your first quiz",
            "icon": "first-steps.png",
            "points_required": 0,
            "category": "achievement"
        },
        {
            "name": "Quiz Master",
            "description": "Complete 10 quizzes",
            "icon": "quiz-master.png",
            "points_required": 100,
            "category": "milestone"
        },
        {
            "name": "Perfect Score",
            "description": "Get 100% on any quiz",
            "icon": "perfect-score.png",
            "points_required": 50,
            "category": "achievement"
        },
        {
            "name": "Vocabulary Expert",
            "description": "Complete 5 vocabulary quizzes",
            "icon": "vocabulary-expert.png",
            "points_required": 75,
            "category": "special"
        },
        {
            "name": "Grammar Guru",
            "description": "Complete 5 grammar quizzes",
            "icon": "grammar-guru.png",
            "points_required": 75,
            "category": "special"
        },
        {
            "name": "Speed Demon",
            "description": "Complete a quiz in under 2 minutes",
            "icon": "speed-demon.png",
            "points_required": 25,
            "category": "achievement"
        }
    ]
    
    badges = []
    for badge_data in badges_data:
        badge = Badge(**badge_data)
        badges.append(badge)
    
    return badges

def create_sample_words_of_day():
    """Create sample words of the day"""
    words_data = [
        {
            "word": "Serendipity",
            "meaning": "The occurrence and development of events by chance in a happy or beneficial way",
            "example_sentence": "Finding that perfect job was pure serendipity.",
            "pronunciation": "/ˌserənˈdipədē/",
            "difficulty": "hard",
            "category": "vocabulary",
            "date": date.today()
        },
        {
            "word": "Perseverance",
            "meaning": "Persistence in doing something despite difficulty or delay in achieving success",
            "example_sentence": "Her perseverance in learning English paid off when she got the job.",
            "pronunciation": "/ˌpərsəˈvirəns/",
            "difficulty": "medium",
            "category": "vocabulary",
            "date": date.today() - timedelta(days=1)
        },
        {
            "word": "Eloquent",
            "meaning": "Fluent or persuasive in speaking or writing",
            "example_sentence": "The speaker was so eloquent that everyone was moved by her words.",
            "pronunciation": "/ˈeləkwənt/",
            "difficulty": "medium",
            "category": "vocabulary",
            "date": date.today() - timedelta(days=2)
        },
        {
            "word": "Resilient",
            "meaning": "Able to withstand or recover quickly from difficult conditions",
            "example_sentence": "Children are often more resilient than adults think.",
            "pronunciation": "/rəˈzilyənt/",
            "difficulty": "medium",
            "category": "vocabulary",
            "date": date.today() - timedelta(days=3)
        },
        {
            "word": "Ubiquitous",
            "meaning": "Present, appearing, or found everywhere",
            "example_sentence": "Smartphones have become ubiquitous in modern society.",
            "pronunciation": "/yo͞oˈbikwədəs/",
            "difficulty": "hard",
            "category": "vocabulary",
            "date": date.today() - timedelta(days=4)
        }
    ]
    
    words = []
    for word_data in words_data:
        word = WordOfDay(**word_data)
        words.append(word)
    
    return words

def create_sample_scores(users, quizzes):
    """Create sample scores"""
    scores_data = [
        {"user": users[0], "quiz": quizzes[0], "score": 85.0, "time_taken": 180},
        {"user": users[0], "quiz": quizzes[1], "score": 90.0, "time_taken": 200},
        {"user": users[1], "quiz": quizzes[0], "score": 75.0, "time_taken": 250},
        {"user": users[2], "quiz": quizzes[0], "score": 100.0, "time_taken": 150},
        {"user": users[2], "quiz": quizzes[1], "score": 95.0, "time_taken": 180},
        {"user": users[2], "quiz": quizzes[2], "score": 80.0, "time_taken": 450},
        {"user": users[3], "quiz": quizzes[0], "score": 88.0, "time_taken": 200},
        {"user": users[3], "quiz": quizzes[1], "score": 92.0, "time_taken": 220}
    ]
    
    scores = []
    for score_data in scores_data:
        score = Score(
            user_id=score_data["user"].id,
            quiz_id=score_data["quiz"].id,
            score=score_data["score"],
            time_taken=score_data["time_taken"],
            answers=json.dumps({"0": "0", "1": "1"})
        )
        scores.append(score)
    
    return scores

def create_sample_user_badges(users, badges):
    """Create sample user badges"""
    user_badges_data = [
        {"user": users[0], "badge": badges[0]},  # First Steps
        {"user": users[0], "badge": badges[2]},  # Perfect Score
        {"user": users[1], "badge": badges[0]},  # First Steps
        {"user": users[2], "badge": badges[0]},  # First Steps
        {"user": users[2], "badge": badges[1]},  # Quiz Master
        {"user": users[2], "badge": badges[2]},  # Perfect Score
        {"user": users[2], "badge": badges[3]},  # Vocabulary Expert
        {"user": users[3], "badge": badges[0]},  # First Steps
        {"user": users[3], "badge": badges[2]},  # Perfect Score
    ]
    
    user_badges = []
    for ub_data in user_badges_data:
        user_badge = UserBadge(
            user_id=ub_data["user"].id,
            badge_id=ub_data["badge"].id
        )
        user_badges.append(user_badge)
    
    return user_badges

def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Create users
        print("👥 Creating users...")
        users = create_sample_users()
        for user in users:
            db.add(user)
        db.commit()
        print(f"✅ Created {len(users)} users")
        
        # Create quizzes
        print("📝 Creating quizzes...")
        quizzes = create_sample_quizzes()
        for quiz in quizzes:
            db.add(quiz)
        db.commit()
        print(f"✅ Created {len(quizzes)} quizzes")
        
        # Create badges
        print("🏆 Creating badges...")
        badges = create_sample_badges()
        for badge in badges:
            db.add(badge)
        db.commit()
        print(f"✅ Created {len(badges)} badges")
        
        # Create words of the day
        print("📚 Creating words of the day...")
        words = create_sample_words_of_day()
        for word in words:
            db.add(word)
        db.commit()
        print(f"✅ Created {len(words)} words of the day")
        
        # Create scores
        print("📊 Creating scores...")
        scores = create_sample_scores(users, quizzes)
        for score in scores:
            db.add(score)
        db.commit()
        print(f"✅ Created {len(scores)} scores")
        
        # Create user badges
        print("🎖️ Creating user badges...")
        user_badges = create_sample_user_badges(users, badges)
        for user_badge in user_badges:
            db.add(user_badge)
        db.commit()
        print(f"✅ Created {len(user_badges)} user badges")
        
        print("🎉 Database seeding completed successfully!")
        print("\n📋 Sample data created:")
        print(f"   • {len(users)} users")
        print(f"   • {len(quizzes)} quizzes")
        print(f"   • {len(badges)} badges")
        print(f"   • {len(words)} words of the day")
        print(f"   • {len(scores)} scores")
        print(f"   • {len(user_badges)} user badges")
        
        print("\n🔑 Sample login credentials:")
        for user in users:
            print(f"   • Username: {user.username}, Password: password123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()