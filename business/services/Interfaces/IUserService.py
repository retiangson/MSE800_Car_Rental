from abc import ABC, abstractmethod

class IUserService(ABC):
    @abstractmethod
    def register_user(self, user):
        pass

    @abstractmethod
    def login_user(self, username, password):
        pass

    @abstractmethod
    def list_users(self, include_deleted=False, sort_by="id"):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass
