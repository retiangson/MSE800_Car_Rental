from Domain.Models.User import User
from Contracts.UserDto import UserDto

class UserMapper:
    """
    Mapper class for converting between User ORM model and UserDto.
    Keeps the domain model (DB entity) separate from the DTO (used in APIs/UI).
    """
    @staticmethod
    def to_dto(user: User) -> UserDto:
        """
        Convert a User model to a UserDto.
        Returns None if input is None.
        """
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
        """
        Convert a UserDto back into a User model.
        Returns None if input is None.
        """
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
