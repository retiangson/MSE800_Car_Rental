import pytest
from faker import Faker
from Domain.Repositories.UserRepository import UserRepository
from Domain.Models.User import User
from Domain.Repositories.DBManager import init_db
from Contracts.Enums.StatusEnums import UserStatus 

faker = Faker()

@pytest.fixture(autouse=True)
def setup_db():
    """Reinitialize the test database before each test run."""
    init_db()

@pytest.fixture
def repo():
    """Provide a fresh UserRepository instance."""
    return UserRepository()

def make_user(username=None, password="secret123", role="customer", status=UserStatus.ACTIVE):
    """Helper to generate a User object with fake data."""
    return User(
        id=None,
        username=username or faker.user_name(),
        password=password,
        role=role,
        name=faker.name(),
        contact_number=faker.phone_number(),
        email=faker.email(),
        address=faker.address(),
        status=status
    )

# --- Tests ---

def test_seed_default_users(repo):
    """Ensure seeding inserts default admin if DB is empty."""
    repo.seed_default_users()
    users = repo.get_all(include_deleted=True)
    assert any(u.username == "admin" and u.role == "admin" for u in users)

def test_add_user(repo):
    user = make_user()
    saved = repo.add(user)
    assert saved.id is not None
    assert saved.username == user.username
    assert saved.status == UserStatus.ACTIVE

def test_get_all_and_get_by_id(repo):
    u1 = repo.add(make_user())
    u2 = repo.add(make_user())

    all_users = repo.get_all()
    assert len(all_users) >= 2

    found = repo.get_by_id(u1.id)
    assert found is not None
    assert found.id == u1.id

def test_find_by_username(repo):
    fakeUserName = faker.user_name()
    user = repo.add(make_user(username=fakeUserName))
    found = repo.find_by_username(fakeUserName)
    assert found is not None
    assert found.username == fakeUserName

def test_soft_delete_and_restore(repo):
    user = repo.add(make_user())
    assert repo.soft_delete(user.id) is True

    deleted = repo.get_by_id(user.id, include_deleted=True)
    assert deleted.status == UserStatus.DELETED

    assert repo.restore(user.id) is True
    restored = repo.get_by_id(user.id)
    assert restored.status == UserStatus.ACTIVE

def test_update_user(repo):
    updated_username = faker.user_name()
    user = repo.add(make_user())
    user.username = updated_username
    user.role = "admin"
    user.email = "updated@example.com"

    updated = repo.update(user)
    assert updated is not None
    assert updated.username == updated_username
    assert updated.role == "admin"
    assert updated.email == "updated@example.com"

def test_get_by_id_excludes_deleted(repo):
    user = repo.add(make_user())
    repo.soft_delete(user.id)

    found = repo.get_by_id(user.id)  # default excludes deleted
    assert found is None

    found_including = repo.get_by_id(user.id, include_deleted=True)
    assert found_including is not None
    assert found_including.status == UserStatus.DELETED
