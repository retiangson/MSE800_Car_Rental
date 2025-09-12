from abc import ABC, abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user): pass

    @abstractmethod
    def get_all(self, include_deleted=False): pass

    @abstractmethod
    def find_by_id(self, user_id): pass

    @abstractmethod
    def find_by_username(self, username): pass

    @abstractmethod
    def delete(self, user_id): pass
