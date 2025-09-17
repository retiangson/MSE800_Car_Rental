from abc import ABC, abstractmethod
from Contracts.UserDto import UserDto
from typing import List, Optional

class IUserService(ABC):
    """Interface defining business logic operations for User service."""

    @abstractmethod
    def register_user(self, user: UserDto) -> UserDto:
        """Register a new user (hash password before saving)."""
        pass

    @abstractmethod
    def login_user(self, username: str, password: str) -> Optional[UserDto]:
        """Authenticate a user by verifying username and password."""
        pass

    @abstractmethod
    def list_users(self, include_deleted: bool = False, sort_by: str = "id") -> List[UserDto]:
        """Retrieve all users, optionally including deleted ones."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Soft delete a user by ID (mark status=Deleted)."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[UserDto]:
        """Fetch a user by ID (excluding deleted ones)."""
        pass
