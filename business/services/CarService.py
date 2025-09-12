from Business.Services.Interfaces.ICarService import ICarService
from Domain.Interfaces.ICarRepository import ICarRepository

class CarService(ICarService):
    def __init__(self, repo: ICarRepository):
        self.repo = repo

    def add_car(self, car):
        # Default new car as Available
        car.status = "Available"
        return self.repo.add(car)

    def list_cars(self, include_deleted=False, sort_by="id"):
        cars = self.repo.get_all()
        if not include_deleted:
            # Only cars that are not marked as Deleted
            cars = list(filter(lambda c: c.status != "Deleted", cars))
        return sorted(cars, key=lambda c: getattr(c, sort_by, c.id))

    def list_available_cars(self, sort_by="rate"):
        cars = self.repo.get_all()
        cars = list(filter(lambda c: c.status == "Available", cars))
        return sorted(cars, key=lambda c: getattr(c, sort_by, c.id))
    
    def delete_car(self, car_id):
        return self.repo.update_status(car_id, "Deleted")
    
    def rent_car(self, car_id):
        return self.repo.update_status(car_id, "Rented")

    def return_car(self, car_id):
        return self.repo.update_status(car_id, "Available")

    def send_to_maintenance(self, car_id):
        return self.repo.update_status(car_id, "Maintenance")
