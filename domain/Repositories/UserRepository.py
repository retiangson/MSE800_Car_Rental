from Domain.Interfaces.IUserRepository import IUserRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.User import User

class UserRepository(IUserRepository):
    def __init__(self):
        self._init_table()
        self._seed_default_users()

    def _init_table(self):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    role TEXT,
                    name TEXT,
                    contact_number TEXT,
                    email TEXT,
                    address TEXT,
                    isActive INTEGER DEFAULT 1,
                    isDeleted INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def _seed_default_users(self):
        """Insert default admin if no users exist."""
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            (count,) = cursor.fetchone()
            if count == 0:
                cursor.execute(
                    "INSERT INTO users (username, password, role, name, contact_number, email, address, isActive, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    ("admin", "admin123", "admin", "System Admin", "0000000000", "admin@system.local", "Head Office", 1, 0)
                )
                conn.commit()

    def add(self, user: User):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role, name, contact_number, email, address, isActive, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user.username, user.password, user.role, user.name,
                 user.contact_number, user.email, user.address,
                 int(user.isActive), int(user.isDeleted))
            )
            conn.commit()
            user.id = cursor.lastrowid
            return user

    def get_all(self):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role, name, contact_number, email, address, isActive, isDeleted FROM users")
            rows = cursor.fetchall()
            return [User(*row) for row in rows]

    def find_by_id(self, user_id):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role, name, contact_number, email, address, isActive, isDeleted FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return User(*row) if row else None

    def find_by_username(self, username):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role, name, contact_number, email, address, isActive, isDeleted FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return User(*row) if row else None

    def delete(self, user_id):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET isDeleted = 1, isActive = 0 WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
