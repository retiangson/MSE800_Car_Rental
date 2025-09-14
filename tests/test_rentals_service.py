import pytest
from faker import Faker
from Contracts.RentalDto import RentalDto
from Business.Services.RentalService import RentalService
from Domain.Repositories.RentalRepository import RentalRepository
from Business.Services.CarService import CarService
from Domain.Repositories.CarRepository import CarRepository
from Business.Services.UsersService import UsersService
from Domain.Repositories.UserRepository import UserRepository
fake = Faker()

@pytest.fixture
def rental_service():
    rental_repo = RentalRepository()
    car_service = CarService(CarRepository())
    user_service = UsersService(UserRepository())
    return RentalService(rental_repo, car_service, user_service) 

def make_fake_rental_dto():
    start = fake.date_between(start_date="-1y", end_date="today")
    end = fake.date_between(start_date="today", end_date="+30d")
    return RentalDto(
        id=None,
        car_id=fake.random_int(1, 5),
        user_id=fake.random_int(1, 10),
        start_date=start.strftime("%Y-%m-%d"),
        end_date=end.strftime("%Y-%m-%d"),
        total_cost=None,
        status="Pending"
    )

def test_create_fake_rental(rental_service):
    dto = make_fake_rental_dto()
    saved = rental_service.create_rental(dto)
    assert saved is not None
    assert saved.status == "Pending"
