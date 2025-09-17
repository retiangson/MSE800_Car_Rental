import pytest
from faker import Faker
from Business.Services.UsersService import UsersService
from Domain.Repositories.UserRepository import UserRepository
from Contracts.UserDto import UserDto
from Contracts.Enums.StatusEnums import UserStatus 

faker = Faker()

@pytest.fixture
def service():
    """Provide a UsersService instance with fresh UserRepository."""
    return UsersService(UserRepository())

def make_user_dto(password="secret123", role="customer"):
    """Helper to create a fake UserDto."""
    return UserDto(
        id=None,
        username=faker.user_name(),
        password=password,
        role=role,
        name=faker.name(),
        contact_number=faker.phone_number(),
        email=faker.email(),
        address=faker.address(),
        status=UserStatus.ACTIVE   # ✅ enum instead of string
    )

# --- Tests ---

def test_register_user_and_login(service):
    dto = make_user_dto(password="mypassword")
    registered = service.register_user(dto)
    assert registered.id is not None
    assert registered.username == dto.username
    assert registered.role == "customer"

    # Login success
    logged_in = service.login_user(dto.username, "mypassword")
    assert logged_in is not None
    assert logged_in.username == dto.username

    # Login fail
    wrong_login = service.login_user(dto.username, "wrongpass")
    assert wrong_login is None

def test_list_users(service):
    u1 = service.register_user(make_user_dto())
    u2 = service.register_user(make_user_dto())

    users = service.list_users()
    usernames = [u.username for u in users]
    assert u1.username in usernames
    assert u2.username in usernames

def test_delete_and_restore_user(service):
    dto = make_user_dto()
    registered = service.register_user(dto)

    # Delete
    deleted = service.delete(registered.id)
    assert deleted is True

    # User should not appear in list_users (exclude deleted)
    users = service.list_users()
    assert all(u.id != registered.id for u in users)

    # User still exists in DB (if include_deleted=True)
    users_with_deleted = service.list_users(include_deleted=True)
    assert any(u.id == registered.id for u in users_with_deleted)

def test_get_by_id(service):
    dto = make_user_dto()
    registered = service.register_user(dto)

    found = service.get_by_id(registered.id)
    assert found is not None
    assert found.username == dto.username

def test_update_user(service):
    dto = make_user_dto(password="oldpassword")
    registered = service.register_user(dto)

    updated_dto = UserDto(
        id=registered.id,
        username=registered.username,
        password="newpassword",
        role="admin",
        name="Updated Name",
        contact_number="1234567890",
        email="updated@example.com",
        address="Updated Address",
        status=UserStatus.ACTIVE   # ✅ enum instead of string
    )

    updated = service.update_user(updated_dto)
    assert updated is not None
    assert updated.role == "admin"
    assert updated.name == "Updated Name"
    assert updated.email == "updated@example.com"

    # Verify login still works with new password
    logged_in = service.login_user(updated.username, "newpassword")
    assert logged_in is not None
    assert logged_in.username == updated.username
