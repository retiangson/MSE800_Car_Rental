import pytest
from faker import Faker
from Domain.Repositories.RentalRepository import RentalRepository
from Domain.Models.Rental import Rental
from Domain.Repositories.DBManager import init_db
from Contracts.Enums.StatusEnums import RentalStatus 

faker = Faker()

@pytest.fixture(autouse=True)
def setup_db():
    """Reinitialize the test database before each test run."""
    init_db()

@pytest.fixture
def repo():
    """Provide a fresh RentalRepository instance."""
    return RentalRepository()

def make_rental(user_id=1, car_id=1, status=RentalStatus.PENDING):
    """Helper to generate a Rental object with fake data."""
    return Rental(
        id=None,
        user_id=user_id,
        car_id=car_id,
        start_date=faker.date(),
        end_date=faker.date(),
        total_cost=0.0,
        status=status
    )

# --- Tests ---

def test_add_rental(repo):
    rental = make_rental()
    saved = repo.add(rental)
    assert saved.id is not None
    assert saved.status == RentalStatus.PENDING

def test_get_all_and_get_by_id(repo):
    r1 = repo.add(make_rental())
    r2 = repo.add(make_rental())

    all_rentals = repo.get_all()
    assert len(all_rentals) >= 2

    found = repo.get_by_id(r1.id)
    assert found is not None
    assert found.id == r1.id

def test_soft_delete_and_restore(repo):
    rental = repo.add(make_rental())
    assert repo.soft_delete(rental.id) is True

    deleted = repo.get_by_id(rental.id, include_deleted=True)
    assert deleted.status == RentalStatus.DELETED

    assert repo.restore(rental.id) is True
    restored = repo.get_by_id(rental.id)
    assert restored.status == RentalStatus.PENDING

def test_update_status(repo):
    rental = repo.add(make_rental())
    updated = repo.update_status(rental.id, RentalStatus.ACTIVE)
    assert updated is True
    found = repo.get_by_id(rental.id)
    assert found.status == RentalStatus.ACTIVE

def test_update_total_cost(repo):
    rental = repo.add(make_rental())
    result = repo.update_total_cost(rental.id, 150.0)
    assert result is True
    updated = repo.get_by_id(rental.id)
    assert updated.total_cost == 150.0

def test_get_by_id_excludes_deleted(repo):
    rental = repo.add(make_rental())
    repo.soft_delete(rental.id)

    found = repo.get_by_id(rental.id)  # default excludes deleted
    assert found is None

    found_including = repo.get_by_id(rental.id, include_deleted=True)
    assert found_including is not None
    assert found_including.status == RentalStatus.DELETED
