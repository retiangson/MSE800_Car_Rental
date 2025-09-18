import os
import sys
from contextlib import contextmanager
from typing import Optional

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session, Session


# ---------- Shared Base (import this in your ORM models) ----------
class Base(DeclarativeBase):
    pass


class Config:
    """Configuration for database."""
    DB_URL = os.getenv("DB_URL")  # e.g. "sqlite:///car_rental.db"
    DB_NAME = os.getenv("DB_NAME", "car_rental.db")


def _resolve_db_url() -> str:
    """Resolve DB URL with fallback to project-root SQLite file.
       Auto-switch to in-memory SQLite when running under pytest.
    """
    if "pytest" in sys.modules:
        # Use shared in-memory DB so FastAPI + SQLAlchemy share schema
        return "sqlite+pysqlite:///file::memory:?cache=shared&uri=true"

    if Config.DB_URL:
        return Config.DB_URL

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    db_path = os.path.join(project_root, Config.DB_NAME)
    return f"sqlite:///{db_path}"

# Global engine & session factory
DB_URL = _resolve_db_url()
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {},
)

# Apply helpful SQLite PRAGMAs on each new DB-API connection
@event.listens_for(engine, "connect")
def _sqlite_on_connect(dbapi_conn, _):
    try:
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA journal_mode=WAL;")
        cur.execute("PRAGMA synchronous=NORMAL;")
        cur.execute("PRAGMA foreign_keys=ON;")
        cur.close()
    except Exception:
        pass


# Thread-local session registry
_SessionFactory = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)
ScopedSession = scoped_session(_SessionFactory)


def init_db() -> None:
    """
    Call once at startup *after* importing ORM models.
    Example:
        from Domain.Models.user import User
        from Domain.Models.car import Car
        from Domain.Models.rental import Rental
        from Domain.Repositories.DBManager import init_db
        init_db()
    """
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Session:
    """Context manager that commits or rolls back automatically."""
    session: Session = ScopedSession()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        ScopedSession.remove()


class DBManager:
    """Backward-compatible context manager for older code."""
    def __init__(self):
        self._session: Optional[Session] = None

    def __enter__(self) -> Session:
        self._session = ScopedSession()
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                self._session.rollback()
            else:
                self._session.commit()
        finally:
            ScopedSession.remove()
            self._session = None


def get_session() -> Session:
    """Return the current thread’s Session (creates one if needed)."""
    return ScopedSession()

import Domain.Models.User
import Domain.Models.Car
import Domain.Models.Rental