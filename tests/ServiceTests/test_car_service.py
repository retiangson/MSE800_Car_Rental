import pytest
from faker import Faker
from Business.Services.CarService import CarService
from Domain.Repositories.CarRepository import CarRepository
from Contracts.CarDto import CarDto
from Contracts.Enums.StatusEnums import CarStatus

faker = Faker()

@pytest.fixture
def service():
    """Provide a CarService instance with a fresh CarRepository."""
    return CarService(CarRepository())

def make_car_dto(status: CarStatus = CarStatus.AVAILABLE):
    """Helper to generate a CarDto with fake data."""
    return CarDto(
        id=None,
        make=faker.company(),
        model=faker.word(),
        year=faker.random_int(min=2000, max=2024),
        vtype=faker.random_element(elements=["sedan", "suv", "ev"]),
        base_rate=round(faker.random_number(digits=2), 2),
        status=status
    )

# --- Tests ---

def test_add_car_defaults_available(service):
    dto = make_car_dto(status=None)  # no status provided
    saved = service.add_car(dto)
    assert saved.id is not None
    assert saved.status == CarStatus.AVAILABLE

def test_list_cars_and_available(service):
    c1 = service.add_car(make_car_dto(status=CarStatus.AVAILABLE))
    c2 = service.add_car(make_car_dto(status=CarStatus.DELETED))
    c3 = service.add_car(make_car_dto(status=CarStatus.AVAILABLE))

    all_cars = service.list_cars(include_deleted=True)
    assert any(car.id == c2.id for car in all_cars)

    available_cars = service.list_available_cars()
    assert all(car.status == CarStatus.AVAILABLE for car in available_cars)
    assert c2.id not in [car.id for car in available_cars]

def test_delete_and_restore_car(service):
    car = service.add_car(make_car_dto())
    deleted = service.delete_car(car.id)
    assert deleted is True

    restored = service.restore_car(car.id)
    assert restored is True

    restored_car = service.get_by_id(car.id)
    assert restored_car.status == CarStatus.AVAILABLE

def test_rent_and_return_car(service):
    car = service.add_car(make_car_dto())

    rented = service.rent_car(car.id)
    assert rented is True
    rented_car = service.get_by_id(car.id)
    assert rented_car.status == CarStatus.ACTIVE

    returned = service.return_car(car.id)
    assert returned is True
    returned_car = service.get_by_id(car.id)
    assert returned_car.status == CarStatus.AVAILABLE

def test_send_to_maintenance(service):
    car = service.add_car(make_car_dto())
    result = service.send_to_maintenance(car.id)
    assert result is True
    updated = service.get_by_id(car.id)
    assert updated.status == CarStatus.MAINTENANCE

def test_update_car(service):
    car = service.add_car(make_car_dto())
    dto = CarDto(
        id=car.id,
        make="UpdatedMake",
        model="UpdatedModel",
        year=2025,
        vtype="suv",
        base_rate=99.99,
        status=CarStatus.AVAILABLE
    )

    updated = service.update_car(dto)
    assert updated is not None
    assert updated.make == "UpdatedMake"
    assert updated.model == "UpdatedModel"
    assert updated.year == 2025
    assert updated.base_rate == 99.99

def test_get_by_id(service):
    car = service.add_car(make_car_dto())
    found = service.get_by_id(car.id)
    assert found is not None
    assert found.id == car.id
