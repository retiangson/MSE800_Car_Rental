from passlib.hash import pbkdf2_sha256
from Business.Interfaces.IUserService import IUserService
from Domain.Interfaces.IUserRepository import IUserRepository
from Domain.Mappers.UserMapper import UserMapper
from Contracts.UserDto import UserDto
from Contracts.Enums.StatusEnums import UserStatus

class UsersService(IUserService):
    """Service layer for managing users (registration, login, updates, soft delete)."""

    def __init__(self, repo: IUserRepository):
        """Initialize with a UserRepository implementation."""
        self.repo = repo

    def register_user(self, dto: UserDto) -> UserDto:
        """Register a new user (hash password before saving)."""
        user = UserMapper.from_dto(dto)

        # Ensure password is hashed before storing
        if getattr(user, "password", None):
            user.password = pbkdf2_sha256.hash(user.password)

        saved = self.repo.add(user)
        return UserMapper.to_dto(saved)

    def login_user(self, username: str, password: str) -> UserDto | None:
        """Authenticate user by verifying username and password."""
        try:
            user = self.repo.find_by_username(username)
        except Exception:
            # Fallback if repo method fails → manually search
            users = self.repo.get_all()
            user = next((u for u in users if u.username == username), None)

        # Reject if user not found or soft-deleted
        if not user or user.status == UserStatus.DELETED:
            return None

        # Verify password hash
        if pbkdf2_sha256.verify(password, user.password):
            return UserMapper.to_dto(user)

        return None

    def list_users(self, include_deleted: bool = False, sort_by: str = "id") -> list[UserDto]:
        """Return all users as DTOs, optionally including deleted ones."""
        users = self.repo.get_all(include_deleted=include_deleted)

        # Exclude soft-deleted unless explicitly included
        if not include_deleted:
            users = [u for u in users if u.status != UserStatus.DELETED]

        dtos = [UserMapper.to_dto(u) for u in users]
        return sorted(dtos, key=lambda u: getattr(u, sort_by, u.id))

    def delete(self, user_id: int) -> bool:
        """Soft delete a user by ID."""
        return self.repo.soft_delete(user_id)
    
    def get_by_id(self, user_id: int) -> UserDto | None:
        """Fetch a user by ID (excluding deleted)."""
        user = self.repo.get_by_id(user_id, include_deleted=False)
        return UserMapper.to_dto(user)
    
    def update_user(self, dto: UserDto) -> UserDto | None:
        """Update user details (rehash password if plain)."""
        user = UserMapper.from_dto(dto)

        # Re-hash password if it's not already hashed
        if dto.password and not dto.password.startswith("$pbkdf2-sha256$"):
            user.password = pbkdf2_sha256.hash(dto.password)

        updated = self.repo.update(user)
        return UserMapper.to_dto(updated) if updated else None
