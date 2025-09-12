from ui.MainMenu import run
from Domain.Repositories.CarRepository import CarRepository
from Domain.Repositories.UserRepository import UserRepository
from Domain.Repositories.RentalRepository import RentalRepository
from Business.Services.CarService import CarService
from Business.Services.UsersService import UsersService
from Business.Services.RentalService import RentalService

if __name__ == "__main__":
    print("🚗 Starting Car Rental System 🚗")

    # Dependency injection
    car_repo = CarRepository()
    car_service = CarService(car_repo)

    user_service = UsersService(UserRepository())

    rental_repo = RentalRepository()
    rental_service = RentalService(rental_repo, car_service)  # ✅ pass car_service too

    run(car_service, user_service, rental_service)
