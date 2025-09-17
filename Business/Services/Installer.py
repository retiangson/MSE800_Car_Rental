from Domain.Repositories.CarRepository import CarRepository
from Domain.Repositories.UserRepository import UserRepository
from Domain.Repositories.RentalRepository import RentalRepository

from Business.Services.CarService import CarService
from Business.Services.UsersService import UsersService
from Business.Services.RentalService import RentalService

from ui.Car import CarUI
from ui.Customer import CustomerUI
from ui.User import UserUI
from ui.Login import LoginUI
from ui.Rental import RentalUI

from Domain.Repositories.DBManager import init_db

class ServiceInstaller:
    """Central installer that wires repositories, services, and UI components."""

    def __init__(self):
        init_db()  # Ensure DB tables are created before anything else

        # --- Repositories (Data Layer) ---
        car_repo = CarRepository()
        user_repo = UserRepository()
        user_repo.seed_default_users()  # Create default admin if no users exist
        rental_repo = RentalRepository()

        # --- Services (Business Logic Layer) ---
        self.car_service = CarService(car_repo)
        self.user_service = UsersService(user_repo)
        self.rental_service = RentalService(rental_repo, self.car_service, self.user_service)

        # --- UI Components (Presentation Layer) ---
        self.car_ui = CarUI(self.car_service)
        self.customer_ui = CustomerUI(self.user_service)
        self.user_ui = UserUI(self.user_service)
        self.login_ui = LoginUI(self.user_service)
        self.rental_ui = RentalUI(self.rental_service)
