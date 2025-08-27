# English Learning API Backend

A comprehensive FastAPI backend for an English Learning website with gamification features, authentication, and social features.

## 🚀 Features

- **Authentication**: JWT-based authentication with refresh tokens
- **Quizzes**: Multiple choice quizzes with scoring and time tracking
- **Gamification**: Points system, levels, and badges
- **Word of the Day**: Daily vocabulary words with examples
- **Social Features**: Friend system with requests and blocking
- **Leaderboards**: Global and user-specific rankings
- **Statistics**: User progress tracking and analytics

## 🛠️ Tech Stack

- **Python 3.8+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database (can be easily switched to PostgreSQL)
- **JWT** - Authentication tokens
- **Pydantic** - Data validation
- **Alembic** - Database migrations (optional)

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication logic
│   └── routes/              # API routes
│       ├── __init__.py
│       ├── auth.py          # Authentication endpoints
│       ├── quizzes.py       # Quiz management
│       ├── scores.py        # Score tracking
│       ├── badges.py        # Badge system
│       ├── word_of_day.py   # Word of the day
│       └── friends.py       # Social features
├── requirements.txt         # Python dependencies
├── seed_data.py            # Database seeding script
└── README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python -m app.main
```

### 3. Seed the Database

```bash
python seed_data.py
```

### 4. Access the API

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

### Quizzes
- `GET /api/v1/quizzes/` - Get all quizzes
- `GET /api/v1/quizzes/{id}` - Get specific quiz
- `POST /api/v1/quizzes/` - Create new quiz
- `POST /api/v1/quizzes/{id}/submit` - Submit quiz answers
- `GET /api/v1/quizzes/categories` - Get quiz categories
- `GET /api/v1/quizzes/difficulties` - Get quiz difficulties

### Scores & Statistics
- `GET /api/v1/scores/` - Get user scores
- `GET /api/v1/scores/stats` - Get user statistics
- `GET /api/v1/scores/leaderboard` - Get global leaderboard
- `GET /api/v1/scores/recent` - Get recent scores

### Badges
- `GET /api/v1/badges/` - Get all badges
- `GET /api/v1/badges/user/earned` - Get user's earned badges
- `GET /api/v1/badges/user/available` - Get available badges
- `POST /api/v1/badges/user/{id}/award` - Award badge to user

### Word of the Day
- `GET /api/v1/word-of-day/` - Get today's word
- `GET /api/v1/word-of-day/history` - Get word history
- `GET /api/v1/word-of-day/random` - Get random word
- `GET /api/v1/word-of-day/search` - Search words

### Friends
- `GET /api/v1/friends/` - Get user's friends
- `POST /api/v1/friends/request` - Send friend request
- `POST /api/v1/friends/{id}/accept` - Accept friend request
- `GET /api/v1/friends/suggestions` - Get friend suggestions

## 🔐 Authentication

The API uses JWT tokens for authentication:

1. **Register** or **Login** to get access and refresh tokens
2. Include the access token in the `Authorization` header:
   ```
   Authorization: Bearer <your_access_token>
   ```
3. Use the refresh token to get a new access token when it expires

### Sample Authentication Flow

```bash
# Register a new user
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'

# Use the access token
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <your_access_token>"
```

## 🎮 Gamification Features

### Points System
- Users earn points by completing quizzes
- Points are awarded based on quiz performance
- Level progression based on total points

### Badges
- **Achievement Badges**: First quiz, perfect scores, etc.
- **Milestone Badges**: Complete X quizzes, reach X points
- **Special Badges**: Category-specific achievements

### Leaderboards
- Global leaderboard showing top users
- User-specific statistics and rankings

## 📊 Database Models

### Core Models
- **User**: Username, email, password, points, level
- **Quiz**: Title, questions, answers, category, difficulty
- **Score**: User performance on quizzes
- **Badge**: Achievement definitions
- **UserBadge**: User-badge relationships
- **WordOfDay**: Daily vocabulary words
- **Friend**: Social relationships

## 🔧 Configuration

Environment variables can be set in a `.env` file:

```env
DATABASE_URL=sqlite:///./english_learning.db
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALLOWED_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

## 🧪 Testing

### Sample Data

The seed script creates sample data including:
- 4 test users (alice, bob, charlie, diana)
- 3 sample quizzes (grammar, vocabulary, reading)
- 6 badges with different requirements
- 5 words of the day
- Sample scores and user badges

### Test Credentials

```
Username: alice, Password: password123
Username: bob, Password: password123
Username: charlie, Password: password123
Username: diana, Password: password123
```

## 🚀 Production Deployment

### 1. Environment Setup
```bash
# Set production environment variables
export DATABASE_URL="postgresql://user:password@localhost/english_learning"
export SECRET_KEY="your-secure-secret-key"
export ALLOWED_ORIGINS=["https://yourdomain.com"]
```

### 2. Database Migration (Optional)
```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 3. Run with Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🔗 Frontend Integration

The API is designed to work seamlessly with the React frontend:

- CORS is configured for frontend origins
- JWT tokens for secure authentication
- RESTful endpoints for all features
- Real-time ready for future WebSocket features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the API documentation at `/docs`
- Review the code comments
- Open an issue on GitHub

---

**Happy Learning! 🎓**