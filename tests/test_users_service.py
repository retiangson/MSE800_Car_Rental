import pytest
from faker import Faker
from passlib.hash import pbkdf2_sha256
from Business.Services.UsersService import UsersService
from Domain.Repositories.UserRepository import UserRepository
from Contracts.UserDto import UserDto

fake = Faker()

@pytest.fixture
def user_service():
    repo = UserRepository()
    return UsersService(repo)

def make_fake_user_dto():
    return UserDto(
        id=None,
        username=fake.user_name(),
        password="Password123!",
        role="customer",
        name=fake.name(),
        contact_number=fake.phone_number(),
        email=fake.email(),
        address=fake.address(),
        status="Active"
    )

def test_register_fake_user(user_service):
    dto = make_fake_user_dto()
    saved = user_service.register_user(dto)
    assert saved is not None
    assert pbkdf2_sha256.verify("Password123!", saved.password)
