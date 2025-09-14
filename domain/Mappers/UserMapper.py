from Domain.Models.User import User
from Contracts.UserDto import UserDto

class UserMapper:
    @staticmethod
    def to_dto(user: User) -> UserDto:
        return UserDto(
            id=user.id,
            username=user.username,
            password=user.password,
            role=user.role,
            name=user.name,
            contact_number=user.contact_number,
            email=user.email,
            address=user.address,
            status=user.status
        )

    @staticmethod
    def from_dto(dto: UserDto) -> User:
        return User(
            id=dto.id,
            username=dto.username,
            password=dto.password,
            role=dto.role,
            name=dto.name,
            contact_number=dto.contact_number,
            email=dto.email,
            address=dto.address,
            status=dto.status or "Active"
        )
