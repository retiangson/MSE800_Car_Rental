from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from typing import Optional, List
from Domain.Interfaces.IUserRepository import IUserRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.User import User
from Contracts.Enums.StatusEnums import UserStatus
def _is_hashed(pwd: str) -> bool:
    """
    Check if a string looks like a pbkdf2_sha256 hash.
    Prevents double hashing of already-hashed passwords.
    """
    return isinstance(pwd, str) and pwd.startswith("$pbkdf2-sha256$")

def _hash_if_plain(pwd: str) -> str:
    """
    Hash a password if it is not already hashed.
    Returns the original hash if it's already hashed.
    """
    if not pwd:
        return pwd
    return pwd if _is_hashed(pwd) else pbkdf2_sha256.hash(pwd)

class UserRepository(IUserRepository):
    """
    Repository for managing User entities in the database.
    Handles user creation, update, soft delete, restore, and lookup.
    """
    def __init__(self):
        pass

    def seed_default_users(self) -> None:
        """
        Ensure at least one admin user exists in the system.
        If no users exist, create a default admin account with username='admin' and password='admin'.
        """
        with DBManager() as db:
            if db.query(User).count() == 0:
                admin = User(
                    username="admin",
                    password=_hash_if_plain("admin"),
                    role="admin",
                    name="System Administrator",
                    status="Active",
                )
                db.add(admin)
                db.commit()

    def add(self, user: User) -> User:
        """
        Add a new user to the database.
        - Password will be hashed before saving.
        - Default status is 'Active'.
        - Prevent duplicate usernames.
        """
        user.password = _hash_if_plain(user.password)
        if not user.status:
            user.status = UserStatus.ACTIVE

        with DBManager() as db:
            # check for duplicates first
            existing = db.query(User).filter(User.username == user.username).first()
            if existing:
                raise ValueError(f"Username '{user.username}' already exists")

            try:
                db.add(user)
                db.commit()
                db.refresh(user)
                return user
            except IntegrityError as e:
                db.rollback()
                raise ValueError(f"Failed to add user '{user.username}': {str(e)}")

    def get_all(self, include_deleted: bool = False) -> List[User]:
        """
        Retrieve all users.
        By default excludes users with status='Deleted'.
        """
        with DBManager() as db:
            q = db.query(User)
            if not include_deleted:
                q = q.filter(User.status != UserStatus.DELETED)
            return q.all()

    def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        """
        Find a user by ID.
        Excludes deleted users unless include_deleted=True.
        """
        with DBManager() as db:
            q = db.query(User).filter_by(id=user_id)
            if not include_deleted:
                q = q.filter(User.status != UserStatus.DELETED)
            return q.first()

    def find_by_username(self, username: str, include_deleted: bool = False) -> Optional[User]:
        """
        Find a user by their username (for login, uniqueness checks).
        Excludes deleted users unless include_deleted=True.
        """
        with DBManager() as db:
            q = db.query(User).filter_by(username=username)
            if not include_deleted:
                q = q.filter(User.status != UserStatus.DELETED)
            return q.first()

    def soft_delete(self, user_id: int) -> bool:
        """
        Soft delete a user by setting status='Deleted'.
        Returns True if successful, False if user not found.
        """
        with DBManager() as db:
            user = db.get(User, user_id)
            if not user:
                return False
            user.status = UserStatus.DELETED
            db.commit()
            return True

    def restore(self, user_id: int) -> bool:
        """
        Restore a soft-deleted user by setting status back to 'Active'.
        Returns True if successful, False if user not found.
        """
        with DBManager() as db:
            user = db.get(User, user_id)
            if not user or user.status != UserStatus.DELETED:
                return False
            user.status = UserStatus.ACTIVE
            db.commit()
            return True

    def update(self, user: User) -> User:
        """
        Update an existing user's details.
        Replaces all fields with the new values provided.
        Returns the updated user, or None if user not found.
        """
        with DBManager() as db:
            existing = db.get(User, user.id)
            if not existing:
                return None
            existing.username = user.username
            existing.password = user.password
            existing.role = user.role
            existing.name = user.name
            existing.contact_number = user.contact_number
            existing.email = user.email
            existing.address = user.address
            existing.status = user.status
            db.commit()
            db.refresh(existing)
            return existing