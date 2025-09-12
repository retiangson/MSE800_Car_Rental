import sqlite3
import os

class Config:
    """Configuration for database."""
    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")  # sqlite | postgres | mysql
    DB_NAME = os.getenv("DB_NAME", "car_rental.db")


class DBManager:
    """Reusable Database Manager for connection handling."""

    def __init__(self):
        self.conn = None

    def connect(self):
        """Establish a database connection."""
        if Config.DB_ENGINE == "sqlite":
            self.conn = sqlite3.connect(Config.DB_NAME)
        else:
            raise NotImplementedError(f"{Config.DB_ENGINE} not supported yet.")
        return self.conn

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
