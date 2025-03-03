from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Any, List

from ....core.database import get_session
from ....core.security import get_current_user
from ....models.user import User
from ....schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
def get_users(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve users.
    """
    # Check if current user has admin privileges
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    *,
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get a specific user by id.
    """
    # Users can access their own data, admins can access any user's data
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    user_in: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new user.
    """
    # Only admins can create new users
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if user with given email already exists
    user = session.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )
    
    # Create new user
    user = User.from_schema(user_in)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    user_id: int,
    user_in: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update a user.
    """
    # Users can update their own data, admins can update any user's data
    if not current_user.is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user attributes
    user_data = user_in.dict(exclude_unset=True)
    for key, value in user_data.items():
        if key == "password" and value:
            # Handle password update separately
            user.set_password(value)
        else:
            setattr(user, key, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    *,
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete a user.
    """
    # Only admins can delete users
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    session.delete(user)
    session.commit() 