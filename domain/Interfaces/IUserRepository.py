from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Models.User import User

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        pass

    @abstractmethod
    def find_by_username(self, username: str, include_deleted: bool = False) -> Optional[User]:
        pass

    @abstractmethod
    def soft_delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def restore(self, user_id: int) -> bool:
        pass
