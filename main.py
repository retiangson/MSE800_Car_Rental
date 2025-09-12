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
    car_service = CarService(CarRepository())
    user_service = UsersService(UserRepository())
    rental_service = RentalService(RentalRepository())

    run(car_service, user_service, rental_service)
