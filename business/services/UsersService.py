from Business.Services.Interfaces.IUserService import IUserService
from Domain.Interfaces.IUserRepository import IUserRepository

class UsersService(IUserService):
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    def register_user(self, user):
        return self.repo.add(user)

    def login_user(self, username, password):
        users = self.repo.get_all()
        return next(
            filter(lambda u: u.username == username and u.password == password and not u.isDeleted, users),
            None
        )

    def list_users(self, include_deleted=False, sort_by="id"):
        users = self.repo.get_all()
        if not include_deleted:
            users = list(filter(lambda u: not u.isDeleted, users))
        return sorted(users, key=lambda u: getattr(u, sort_by, u.id))

    def delete(self, user_id: int):
        return self.repo.delete(user_id)
