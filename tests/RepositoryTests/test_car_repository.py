import pytest
from faker import Faker
from Domain.Repositories.CarRepository import CarRepository
from Domain.Models.Car import Car
from Domain.Repositories.DBManager import init_db
from Contracts.Enums.StatusEnums import CarStatus

faker = Faker()

@pytest.fixture(autouse=True)
def setup_db():
    """Reinitialize the test database before each test run."""
    init_db()

@pytest.fixture
def repo():
    """Provide a fresh CarRepository instance."""
    return CarRepository()

def make_car(status=CarStatus.ACTIVE):
    """Helper to generate a Car object with fake data."""
    return Car(
        id=None,
        make=faker.company(),
        model=faker.word(),
        year=faker.random_int(min=2000, max=2024),
        vtype=faker.random_element(elements=["sedan", "suv", "ev"]),
        base_rate=round(faker.random_number(digits=2), 2),
        status=status
    )

# --- Tests ---

def test_add_car(repo):
    car = make_car()
    saved = repo.add(car)
    assert saved.id is not None
    assert saved.make == car.make
    assert saved.status == CarStatus.ACTIVE

def test_update_car(repo):
    car = repo.add(make_car())
    car.make = "UpdatedMake"
    car.model = "UpdatedModel"
    updated = repo.update(car)
    assert updated is not None
    assert updated.make == "UpdatedMake"
    assert updated.model == "UpdatedModel"

def test_soft_delete_car(repo):
    car = repo.add(make_car())
    result = repo.soft_delete(car.id)
    assert result is True
    deleted = repo.get_by_id(car.id, include_deleted=True)
    assert deleted.status == CarStatus.DELETED

def test_restore_car(repo):
    car = repo.add(make_car())
    repo.soft_delete(car.id)
    restored = repo.restore(car.id)
    assert restored is True
    restored_car = repo.get_by_id(car.id)
    assert restored_car.status == CarStatus.AVAILABLE

def test_get_by_id_excludes_deleted(repo):
    car = repo.add(make_car())
    repo.soft_delete(car.id)
    found = repo.get_by_id(car.id)  # default excludes deleted
    assert found is None
    found_including = repo.get_by_id(car.id, include_deleted=True)
    assert found_including is not None
    assert found_including.status == CarStatus.DELETED

def test_list_cars_excludes_deleted(repo):
    car1 = repo.add(make_car())
    car2 = repo.add(make_car())
    repo.soft_delete(car2.id)

    cars = repo.list()  # exclude deleted
    ids = [c.id for c in cars]
    assert car1.id in ids
    assert car2.id not in ids

    all_cars = repo.list(include_deleted=True)
    ids_all = [c.id for c in all_cars]
    assert car1.id in ids_all
    assert car2.id in ids_all

def test_get_all_is_alias_of_list(repo):
    car = repo.add(make_car())
    cars_list = repo.list()
    cars_all = repo.get_all()
    assert len(cars_list) == len(cars_all)
    assert cars_list[0].id == cars_all[0].id

def test_update_status(repo):
    car = repo.add(make_car())
    result = repo.update_status(car.id, CarStatus.MAINTENANCE)
    assert result is True
    updated = repo.get_by_id(car.id)
    assert updated.status == CarStatus.MAINTENANCE
