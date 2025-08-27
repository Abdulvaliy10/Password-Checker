from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import (
    authenticate_user, create_access_token, create_refresh_token,
    create_user, check_username_availability, check_email_availability,
    refresh_access_token, get_current_active_user
)
from app.schemas import (
    UserCreate, UserResponse, Token, LoginRequest, 
    RefreshTokenRequest, MessageResponse
)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    - **first_name**: Optional first name
    - **last_name**: Optional last name
    """
    # Check if username is available
    if not check_username_availability(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email is available
    if not check_email_availability(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    
    return user


@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with username and password.
    
    - **username**: Username
    - **password**: Password
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
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes in seconds
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest):
    """
    Refresh access token using refresh token.
    
    - **refresh_token**: Valid refresh token
    """
    access_token = refresh_access_token(refresh_data.refresh_token)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_data.refresh_token,
        "token_type": "bearer",
        "expires_in": 1800  # 30 minutes in seconds
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_active_user)):
    """
    Get current user information.
    
    Requires authentication.
    """
    return current_user


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """
    Logout user (client should discard tokens).
    
    Note: This endpoint is for client-side token management.
    The actual token invalidation would require a blacklist mechanism.
    """
    return {"message": "Successfully logged out"}


@router.get("/check-username/{username}", response_model=dict)
async def check_username(username: str, db: Session = Depends(get_db)):
    """
    Check if a username is available.
    
    - **username**: Username to check
    """
    is_available = check_username_availability(db, username)
    return {"username": username, "available": is_available}


@router.get("/check-email/{email}", response_model=dict)
async def check_email(email: str, db: Session = Depends(get_db)):
    """
    Check if an email is available.
    
    - **email**: Email to check
    """
    is_available = check_email_availability(db, email)
    return {"email": email, "available": is_available}