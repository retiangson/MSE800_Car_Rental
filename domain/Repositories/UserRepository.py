from passlib.hash import pbkdf2_sha256
from typing import Optional, List
from Domain.Interfaces.IUserRepository import IUserRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.User import User

def _is_hashed(pwd: str) -> bool:
    return isinstance(pwd, str) and pwd.startswith("$pbkdf2-sha256$")

def _hash_if_plain(pwd: str) -> str:
    if not pwd:
        return pwd
    return pwd if _is_hashed(pwd) else pbkdf2_sha256.hash(pwd)

class UserRepository(IUserRepository):
    def __init__(self):
        pass

    def seed_default_users(self) -> None:
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
        user.password = _hash_if_plain(user.password)
        if not user.status:
            user.status = "Active"
        with DBManager() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    def get_all(self, include_deleted: bool = False) -> List[User]:
        with DBManager() as db:
            q = db.query(User)
            if not include_deleted:
                q = q.filter(User.status != "Deleted")
            return q.all()

    def get_by_id(self, user_id: int, include_deleted: bool = False) -> Optional[User]:
        with DBManager() as db:
            q = db.query(User).filter_by(id=user_id)
            if not include_deleted:
                q = q.filter(User.status != "Deleted")
            return q.first()

    def find_by_username(self, username: str, include_deleted: bool = False) -> Optional[User]:
        with DBManager() as db:
            q = db.query(User).filter_by(username=username)
            if not include_deleted:
                q = q.filter(User.status != "Deleted")
            return q.first()

    def soft_delete(self, user_id: int) -> bool:
        with DBManager() as db:
            user = db.get(User, user_id)
            if not user:
                return False
            user.status = "Deleted"
            db.commit()
            return True

    def restore(self, user_id: int) -> bool:
        with DBManager() as db:
            user = db.get(User, user_id)
            if not user:
                return False
            user.status = "Active"
            db.commit()
            return True
