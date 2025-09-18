import pytest
from faker import Faker
from Domain.Repositories import DBManager
from Domain.Repositories.DBManager import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Initialize the database schema for tests (in-memory auto by DBManager)."""
    # thanks to DBManager auto-detect, this will always use sqlite:///:memory: in pytest
    DBManager.engine.dispose()  # reset engine if already initialized
    DBManager.init_db()

@pytest.fixture
def faker():
    """Provide a Faker instance for generating test data."""
    return Faker()

@pytest.fixture(autouse=True)
def clean_db():
    """Ensure fresh DB schema for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # optional cleanup after each test
    Base.metadata.drop_all(bind=engine)