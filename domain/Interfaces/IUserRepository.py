from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Models.User import User

class IUserRepository(ABC):
    """Interface defining CRUD and soft-delete operations for User."""

    @abstractmethod
    def add(self, user: User) -> User:
        """Add a new user to the database."""
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[User]:
        """Retrieve all users (optionally include deleted ones)."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        """Get a user by their ID (exclude deleted by default)."""
        pass

    @abstractmethod
    def find_by_username(self, username: str, include_deleted: bool = False) -> Optional[User]:
        """Find a user by username (used for login and uniqueness checks)."""
        pass

    @abstractmethod
    def soft_delete(self, user_id: int) -> bool:
        """Mark a user as Deleted instead of removing them."""
        pass

    @abstractmethod
    def restore(self, user_id: int) -> bool:
        """Restore a previously soft-deleted user."""
        pass

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        """Update user details (name, contact, email, address, role, status)."""
        pass
