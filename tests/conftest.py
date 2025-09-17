import pytest
from faker import Faker
from Domain.Repositories.DBManager import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Initialize test database before running tests."""
    init_db()

@pytest.fixture
def faker():
    """Provide a Faker instance for generating test data."""
    return Faker()
