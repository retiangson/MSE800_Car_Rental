import pytest
from faker import Faker
from Domain.Repositories.RentalRepository import RentalRepository
from Domain.Repositories.UserRepository import UserRepository
from Domain.Repositories.CarRepository import CarRepository
from Domain.Models.Rental import Rental
from Domain.Models.User import User
from Domain.Models.Car import Car
from Domain.Repositories.DBManager import Base, engine, init_db
from Contracts.Enums.StatusEnums import RentalStatus, CarStatus

faker = Faker()

@pytest.fixture(autouse=True)
def setup_db():
    """Reinitialize the test database before each test run."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    init_db()

@pytest.fixture
def repos():
    """Provide fresh repositories for each test."""
    return {
        "rentals": RentalRepository(),
        "users": UserRepository(),
        "cars": CarRepository(),
    }

def seed_user_and_car(users_repo, cars_repo):
    """Helper to insert a user and a car before rentals."""
    user = User(username=faker.user_name(), password="pwd", role="customer", name="Tester")
    users_repo.add(user)

    car = Car(
        make="Toyota",
        model="Corolla",
        year=2021,
        vtype="sedan",
        base_rate=50.0,
        status=CarStatus.AVAILABLE,
    )
    cars_repo.add(car)
    return user, car

def make_rental(user_id, car_id, status=RentalStatus.PENDING):
    """Helper to generate a Rental object with fake data."""
    return Rental(
        id=None,
        user_id=user_id,
        car_id=car_id,
        start_date=faker.date(),
        end_date=faker.date(),
        total_cost=0.0,
        status=status,
    )

# --- Tests ---

def test_add_rental(repos):
    user, car = seed_user_and_car(repos["users"], repos["cars"])
    rental = make_rental(user.id, car.id)
    saved = repos["rentals"].add(rental)
    assert saved.id is not None
    assert saved.status == RentalStatus.PENDING

def test_get_all_and_get_by_id(repos):
    user, car = seed_user_and_car(repos["users"], repos["cars"])
    r1 = repos["rentals"].add(make_rental(user.id, car.id))
    r2 = repos["rentals"].add(make_rental(user.id, car.id))

    all_rentals = repos["rentals"].get_all()
    assert len(all_rentals) >= 2

    found = repos["rentals"].get_by_id(r1.id)
    assert found is not None
    assert found.id == r1.id

def test_soft_delete_and_restore(repos):
    user, car = seed_user_and_car(repos["users"], repos["cars"])
    rental = repos["rentals"].add(make_rental(user.id, car.id))
    assert repos["rentals"].soft_delete(rental.id) is True

    deleted = repos["rentals"].get_by_id(rental.id, include_deleted=True)
    assert deleted.status == RentalStatus.DELETED

    assert repos["rentals"].restore(rental.id) is True
    restored = repos["rentals"].get_by_id(rental.id)
    assert restored.status == RentalStatus.PENDING

def test_update_status(repos):
    user, car = seed_user_and_car(repos["users"], repos["cars"])
    rental = repos["rentals"].add(make_rental(user.id, car.id))
    updated = repos["rentals"].update_status(rental.id, RentalStatus.ACTIVE)
    assert updated is True
    found = repos["rentals"].get_by_id(rental.id)
    assert found.status == RentalStatus.ACTIVE

def test_update_total_cost(repos):
    user, car = seed_user_and_car(repos["users"], repos["cars"])
    rental = repos["rentals"].add(make_rental(user.id, car.id))
    result = repos["rentals"].update_total_cost(rental.id, 150.0)
    assert result is True
    updated = repos["rentals"].get_by_id(rental.id)
    assert updated.total_cost == 150.0

def test_get_by_id_excludes_deleted(repos):
    user, car = seed_user_and_car(repos["users"], repos["cars"])
    rental = repos["rentals"].add(make_rental(user.id, car.id))
    repos["rentals"].soft_delete(rental.id)

    found = repos["rentals"].get_by_id(rental.id)  # default excludes deleted
    assert found is None

    found_including = repos["rentals"].get_by_id(rental.id, include_deleted=True)
    assert found_including is not None
    assert found_including.status == RentalStatus.DELETED
