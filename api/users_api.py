from fastapi import APIRouter, HTTPException
from typing import List
from Contracts.UserDto import UserDto
from Business.Services.UsersService import UsersService

router = APIRouter(prefix="/users", tags=["Users"])
user_service: UsersService = None  # Injected later in main_api

@router.get("/", response_model=List[UserDto])
def list_users(include_deleted: bool = False):
    """Get all users (optionally include deleted)."""
    return user_service.list_users(include_deleted=include_deleted)

@router.get("/{user_id}", response_model=UserDto)
def get_user(user_id: int):
    """Get a single user by ID."""
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserDto)
def register_user(user: UserDto):
    """Register a new user (admin or customer)."""
    saved = user_service.register_user(user)
    if not saved:
        raise HTTPException(status_code=400, detail="Failed to register user")
    return saved

@router.put("/{user_id}", response_model=UserDto)
def update_user(user_id: int, dto: UserDto):
    """Update user details by ID."""
    dto.id = user_id
    updated = user_service.update_user(dto)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}")
def delete_user(user_id: int):
    """Soft delete a user (mark as Deleted)."""
    if not user_service.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
