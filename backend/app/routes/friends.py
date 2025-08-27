from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..auth import get_current_active_user
from ..models import Friend, User
from ..schemas import FriendResponse, FriendRequest, UserResponse

router = APIRouter(prefix="/friends", tags=["friends"])

@router.get("/", response_model=List[FriendResponse])
def get_friends(
    status_filter: Optional[str] = Query(None, description="Filter by status: pending, accepted, blocked"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's friends.
    
    - **status_filter**: Filter by friendship status
    """
    query = db.query(Friend).filter(Friend.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(Friend.status == status_filter)
    
    friends = query.all()
    return friends

@router.post("/request", response_model=FriendResponse)
def send_friend_request(
    friend_request: FriendRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a friend request to another user.
    
    - **friend_username**: Username of the user to send request to
    """
    # Find the friend by username
    friend = db.query(User).filter(
        User.username == friend_request.friend_username,
        User.is_active == True
    ).first()
    
    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if friend.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself"
        )
    
    # Check if friendship already exists
    existing_friendship = db.query(Friend).filter(
        ((Friend.user_id == current_user.id) & (Friend.friend_id == friend.id)) |
        ((Friend.user_id == friend.id) & (Friend.friend_id == current_user.id))
    ).first()
    
    if existing_friendship:
        if existing_friendship.status == "accepted":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already friends with this user"
            )
        elif existing_friendship.status == "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Friend request already pending"
            )
        elif existing_friendship.status == "blocked":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot send friend request to blocked user"
            )
    
    # Create friend request
    friendship = Friend(
        user_id=current_user.id,
        friend_id=friend.id,
        status="pending"
    )
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    
    return friendship

@router.post("/{friend_id}/accept", response_model=FriendResponse)
def accept_friend_request(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Accept a friend request.
    
    - **friend_id**: ID of the user who sent the request
    """
    # Find the friend request
    friendship = db.query(Friend).filter(
        Friend.user_id == friend_id,
        Friend.friend_id == current_user.id,
        Friend.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    # Accept the request
    friendship.status = "accepted"
    db.commit()
    db.refresh(friendship)
    
    return friendship

@router.post("/{friend_id}/reject", status_code=status.HTTP_204_NO_CONTENT)
def reject_friend_request(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Reject a friend request.
    
    - **friend_id**: ID of the user who sent the request
    """
    # Find the friend request
    friendship = db.query(Friend).filter(
        Friend.user_id == friend_id,
        Friend.friend_id == current_user.id,
        Friend.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend request not found"
        )
    
    # Delete the request
    db.delete(friendship)
    db.commit()
    return None

@router.post("/{friend_id}/block", response_model=FriendResponse)
def block_user(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Block a user.
    
    - **friend_id**: ID of the user to block
    """
    # Check if user exists
    friend = db.query(User).filter(User.id == friend_id, User.is_active == True).first()
    if not friend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if friend.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot block yourself"
        )
    
    # Find existing friendship or create new one
    friendship = db.query(Friend).filter(
        ((Friend.user_id == current_user.id) & (Friend.friend_id == friend.id)) |
        ((Friend.user_id == friend.id) & (Friend.friend_id == current_user.id))
    ).first()
    
    if friendship:
        # Update existing friendship
        if friendship.user_id == current_user.id:
            friendship.status = "blocked"
        else:
            # Create new blocked relationship
            db.delete(friendship)
            friendship = Friend(
                user_id=current_user.id,
                friend_id=friend.id,
                status="blocked"
            )
            db.add(friendship)
    else:
        # Create new blocked relationship
        friendship = Friend(
            user_id=current_user.id,
            friend_id=friend.id,
            status="blocked"
        )
        db.add(friendship)
    
    db.commit()
    db.refresh(friendship)
    return friendship

@router.delete("/{friend_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove a friend or cancel a friend request.
    
    - **friend_id**: ID of the friend to remove
    """
    # Find the friendship
    friendship = db.query(Friend).filter(
        ((Friend.user_id == current_user.id) & (Friend.friend_id == friend_id)) |
        ((Friend.user_id == friend_id) & (Friend.friend_id == current_user.id))
    ).first()
    
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friendship not found"
        )
    
    # Delete the friendship
    db.delete(friendship)
    db.commit()
    return None

@router.get("/requests", response_model=List[FriendResponse])
def get_friend_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get pending friend requests for current user.
    """
    requests = db.query(Friend).filter(
        Friend.friend_id == current_user.id,
        Friend.status == "pending"
    ).all()
    
    return requests

@router.get("/search", response_model=List[UserResponse])
def search_users(
    q: str = Query(..., min_length=1, description="Search term"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Search for users to add as friends.
    
    - **q**: Search query (username)
    - **skip**: Number of results to skip
    - **limit**: Maximum number of results to return
    """
    search_term = f"%{q}%"
    
    users = db.query(User).filter(
        User.is_active == True,
        User.username.ilike(search_term),
        User.id != current_user.id
    ).offset(skip).limit(limit).all()
    
    return users

@router.get("/suggestions", response_model=List[UserResponse])
def get_friend_suggestions(
    limit: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get friend suggestions for current user.
    """
    # Get users who are not friends and not blocked
    subquery = db.query(Friend.friend_id).filter(
        Friend.user_id == current_user.id
    ).union(
        db.query(Friend.user_id).filter(
            Friend.friend_id == current_user.id
        )
    )
    
    suggestions = db.query(User).filter(
        User.is_active == True,
        User.id != current_user.id,
        ~User.id.in_(subquery)
    ).limit(limit).all()
    
    return suggestions