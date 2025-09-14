import pytest
from faker import Faker
from Contracts.CarDto import CarDto
from Business.Services.CarService import CarService
from Domain.Repositories.CarRepository import CarRepository

fake = Faker()

@pytest.fixture
def car_service():
    return CarService(CarRepository())

def make_fake_car_dto():
    return CarDto(
        id=None,
        make=fake.company(),          # car manufacturer
        model=fake.word().title(),    # fake model name
        year=fake.random_int(2000, 2025),
        vtype=fake.random_element(["sedan", "suv", "ev", "truck"]),
        base_rate=fake.random_int(40, 120),
        status="Available"
    )

def test_add_fake_car(car_service):
    dto = make_fake_car_dto()
    saved = car_service.add_car(dto)
    assert saved is not None
    assert saved.status == "Available"
