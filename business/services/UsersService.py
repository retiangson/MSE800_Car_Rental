from passlib.hash import pbkdf2_sha256
from Business.Interfaces.IUserService import IUserService
from Domain.Interfaces.IUserRepository import IUserRepository
from Domain.Mappers.UserMapper import UserMapper
from Contracts.UserDto import UserDto

class UsersService(IUserService):
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def register_user(self, dto: UserDto) -> UserDto:
        """Register a new user (hash password + save)."""
        user = UserMapper.from_dto(dto)

        # Hash plain password
        if getattr(user, "password", None):
            user.password = pbkdf2_sha256.hash(user.password)

        saved = self.repo.add(user)
        return UserMapper.to_dto(saved)

    def login_user(self, username: str, password: str) -> UserDto | None:
        try:
            user = self.repo.find_by_username(username)
        except Exception:
            users = self.repo.get_all()
            user = next((u for u in users if u.username == username), None)

        if not user or user.status == "Deleted":
            return None

        if pbkdf2_sha256.verify(password, user.password):
            return UserMapper.to_dto(user)

        return None

    def list_users(self, include_deleted: bool = False, sort_by: str = "id") -> list[UserDto]:
        users = self.repo.get_all(include_deleted=include_deleted)

        if not include_deleted:
            users = [u for u in users if u.status != "Deleted"]

        dtos = [UserMapper.to_dto(u) for u in users]
        return sorted(dtos, key=lambda u: getattr(u, sort_by, u.id))

    def delete(self, user_id: int) -> bool:
        return self.repo.soft_delete(user_id)
    
    def get_by_id(self, user_id):
        return self.repo.get_by_id(user_id, include_deleted=False)