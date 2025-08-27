# English Learning API - FastAPI Backend

A comprehensive FastAPI backend for the English Learning platform with authentication, quizzes, badges, gamification, and social features.

## 🚀 Features

### 🔐 Authentication & Security
- **JWT Authentication** with access and refresh tokens
- **Password Hashing** using bcrypt
- **CORS Support** for frontend integration
- **User Registration & Login** with validation

### 📚 Learning Management
- **Quiz System** with multiple categories and difficulty levels
- **Score Tracking** with detailed analytics
- **Progress Monitoring** for individual users
- **Word of the Day** feature for daily vocabulary

### 🏆 Gamification
- **Badge System** with different rarity levels (Common, Rare, Epic, Legendary)
- **Achievement Tracking** with automatic badge awarding
- **Points System** with experience and level progression
- **Streak Tracking** for daily learning motivation

### 📊 Social Features
- **Leaderboards** with multiple ranking criteria
- **User Statistics** and progress analytics
- **Friend System** (ready for implementation)
- **Global Rankings** by points, lessons, and streaks

### 🛠️ Technical Features
- **RESTful API** with comprehensive endpoints
- **Database Models** with SQLAlchemy ORM
- **Input Validation** with Pydantic schemas
- **Error Handling** with proper HTTP status codes
- **API Documentation** with Swagger/OpenAPI

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 with SQLite/PostgreSQL
- **Authentication**: JWT with python-jose
- **Password Hashing**: passlib with bcrypt
- **Validation**: Pydantic 2.5.0
- **Documentation**: Swagger/OpenAPI
- **Testing**: pytest

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
│       ├── badges.py        # Badge system
│       ├── word_of_day.py   # Word of the day
│       └── leaderboard.py   # Leaderboards
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── seed_data.py            # Database seeding script
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Database Setup

The application uses SQLite by default for development. For production, configure PostgreSQL in your `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/english_learning
```

### Seed Data

Populate the database with sample data:

```bash
python seed_data.py
```

This creates:
- Sample users (admin, student1, student2, student3)
- Sample quizzes with questions
- Badges with different rarity levels
- Words of the day
- User streaks

## 📚 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/logout` - Logout user

### Quizzes
- `GET /api/v1/quizzes/` - List all quizzes
- `GET /api/v1/quizzes/{id}` - Get quiz details
- `POST /api/v1/quizzes/{id}/submit` - Submit quiz score
- `GET /api/v1/quizzes/categories/stats` - Quiz category statistics

### Badges
- `GET /api/v1/badges/` - List all badges
- `GET /api/v1/badges/my-badges` - Get user's badges
- `POST /api/v1/badges/check-achievements` - Check and award achievements
- `GET /api/v1/badges/progress/summary` - Badge progress summary

### Word of the Day
- `GET /api/v1/word-of-day/today` - Get today's word
- `GET /api/v1/word-of-day/` - List words of the day
- `GET /api/v1/word-of-day/random` - Get random word

### Leaderboard
- `GET /api/v1/leaderboard/` - Global leaderboard
- `GET /api/v1/leaderboard/my-position` - User's position
- `GET /api/v1/leaderboard/stats` - User statistics
- `GET /api/v1/leaderboard/weekly` - Weekly leaderboard
- `GET /api/v1/leaderboard/monthly` - Monthly leaderboard

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=sqlite:///./english_learning.db

# JWT
SECRET_KEY=your-secret-key-here-make-it-long-and-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# App
DEBUG=True
ENVIRONMENT=development
```

### Database Models

The application includes the following models:

- **User**: Authentication and profile data
- **Quiz**: Quiz questions and metadata
- **Score**: User quiz performance
- **Badge**: Achievement badges
- **UserBadge**: User-badge relationships
- **WordOfDay**: Daily vocabulary words
- **Friendship**: Social connections
- **UserStreak**: Learning streaks
- **Lesson**: Structured learning content
- **UserLesson**: User lesson progress

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

## 🚀 Deployment

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔌 Frontend Integration

The API is designed to work seamlessly with the React frontend. Key integration points:

1. **CORS Configuration**: Already configured for `http://localhost:3000`
2. **JWT Tokens**: Use access tokens for authenticated requests
3. **Error Handling**: Consistent error responses
4. **Pagination**: Standard pagination for list endpoints

### Example Frontend Integration

```javascript
// Login
const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});

const { access_token } = await response.json();

// Authenticated request
const quizResponse = await fetch('/api/v1/quizzes/', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

## 🔮 Future Enhancements

### Planned Features
- **Real-time Features**: WebSocket support for live quizzes
- **Voice Recognition**: Speech-to-text for pronunciation practice
- **AI Integration**: Chatbot for conversation practice
- **Email Notifications**: Progress reminders and achievements
- **Mobile API**: Optimized endpoints for mobile apps

### Scalability Improvements
- **Redis Caching**: For frequently accessed data
- **Database Optimization**: Indexing and query optimization
- **Load Balancing**: Multiple server instances
- **CDN Integration**: For static assets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **SQLAlchemy** for the powerful ORM
- **Pydantic** for data validation
- **JWT** for secure authentication

---

**Built with ❤️ for English learners worldwide!**