import pytest
from faker import Faker
from datetime import datetime, timedelta
from Business.Services.RentalService import RentalService
from Business.Services.CarService import CarService
from Business.Services.UsersService import UsersService
from Domain.Repositories.RentalRepository import RentalRepository
from Domain.Repositories.CarRepository import CarRepository
from Domain.Repositories.UserRepository import UserRepository
from Contracts.RentalDto import RentalDto
from Contracts.CarDto import CarDto
from Contracts.UserDto import UserDto
from Contracts.Enums.StatusEnums import CarStatus, RentalStatus, UserStatus

faker = Faker()

@pytest.fixture
def services():
    """Provide RentalService with CarService and UserService dependencies."""
    car_service = CarService(CarRepository())
    user_service = UsersService(UserRepository())
    rental_service = RentalService(RentalRepository(), car_service, user_service)

    # Seed a car
    car = CarDto(
        id=None,
        make="Toyota",
        model="Corolla",
        year=2020,
        vtype="sedan",
        base_rate=50.0,
        status=CarStatus.AVAILABLE
    )
    saved_car = car_service.add_car(car)

    # Seed a user
    user = UserDto(
        id=None,
        username=faker.unique.user_name(),
        password="password123",
        role="customer",
        name=faker.name(),
        contact_number=faker.phone_number(),
        email=faker.email(),
        address=faker.address(),
        status=UserStatus.ACTIVE
    )
    saved_user = user_service.register_user(user)

    return rental_service, car_service, user_service, saved_car, saved_user

def make_rental_dto(car_id, user_id, days=3):
    """Helper to create a RentalDto."""
    start_date = datetime.today().strftime("%Y-%m-%d")
    end_date = (datetime.today() + timedelta(days=days)).strftime("%Y-%m-%d")
    return RentalDto(
        id=None,
        car_id=car_id,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        total_cost=None,
        status=None
    )

# --- Tests ---

def test_create_rental(services):
    rental_service, _, _, car, user = services
    dto = make_rental_dto(car.id, user.id)
    rental = rental_service.create_rental(dto)
    assert rental.id is not None
    assert rental.status == RentalStatus.PENDING

def test_approve_and_start_rental(services):
    rental_service, car_service, _, car, user = services
    dto = make_rental_dto(car.id, user.id)
    rental = rental_service.create_rental(dto)

    approved = rental_service.approve_and_start_rental(rental.id)
    assert approved is True

    updated = rental_service.repo.get_by_id(rental.id)
    assert updated.status == RentalStatus.ACTIVE

    updated_car = car_service.get_by_id(car.id)
    assert updated_car.status == CarStatus.ACTIVE

def test_complete_rental(services):
    rental_service, car_service, _, car, user = services
    dto = make_rental_dto(car.id, user.id, days=2)
    rental = rental_service.create_rental(dto)
    rental_service.approve_and_start_rental(rental.id)

    return_date = datetime.today() + timedelta(days=2)
    completed = rental_service.complete_rental(rental.id, return_date)
    assert completed is True

    updated = rental_service.repo.get_by_id(rental.id)
    assert updated.status == RentalStatus.COMPLETED
    assert updated.total_cost == car.base_rate * 2

    returned_car = car_service.get_by_id(car.id)
    assert returned_car.status == CarStatus.AVAILABLE

def test_reject_rental(services):
    rental_service, _, _, car, user = services
    dto = make_rental_dto(car.id, user.id)
    rental = rental_service.create_rental(dto)

    rejected = rental_service.reject_rental(rental.id)
    assert rejected is True

    updated = rental_service.repo.get_by_id(rental.id)
    assert updated.status == RentalStatus.REJECTED

def test_cancel_rental(services):
    rental_service, _, _, car, user = services
    dto = make_rental_dto(car.id, user.id)
    rental = rental_service.create_rental(dto)

    cancelled = rental_service.cancel_rental(rental.id)
    assert cancelled is True

    updated = rental_service.repo.get_by_id(rental.id)
    assert updated.status == RentalStatus.CANCELLED

def test_delete_rental(services):
    rental_service, _, _, car, user = services
    dto = make_rental_dto(car.id, user.id)
    rental = rental_service.create_rental(dto)

    deleted = rental_service.delete_rental(rental.id)
    assert deleted is True

    updated = rental_service.repo.get_by_id(rental.id, include_deleted=True)
    assert updated.status == RentalStatus.DELETED

def test_list_rentals_and_active(services):
    rental_service, _, _, car, user = services
    dto1 = make_rental_dto(car.id, user.id)
    dto2 = make_rental_dto(car.id, user.id)

    r1 = rental_service.create_rental(dto1)
    r2 = rental_service.create_rental(dto2)

    rental_service.approve_and_start_rental(r1.id)

    rentals = rental_service.list_rentals()
    assert len(rentals) >= 2

    active = rental_service.list_active_rentals()
    assert any(r.status == RentalStatus.ACTIVE for r in active)
