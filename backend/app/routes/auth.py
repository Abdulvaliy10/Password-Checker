from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import authenticate_user, create_user, create_access_token, create_refresh_token, refresh_access_token, get_current_user
from ..schemas import UserCreate, Token, LoginRequest, RefreshTokenRequest, UserResponse
from ..models import User

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **username**: Unique username for the account
    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    """
    try:
        db_user = create_user(db, user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username and password.
    
    - **username**: Your username
    - **password**: Your password
    """
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_data: RefreshTokenRequest):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Your refresh token
    """
    new_access_token = refresh_access_token(refresh_data.refresh_token)
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_data.refresh_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information.
    Requires authentication.
    """
    return current_user