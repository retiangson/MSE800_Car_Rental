from typing import List, Optional
from Domain.Repositories.DBManager import DBManager
from Domain.Models.Car import Car

class CarRepository:
    def add(self, car: Car) -> Car:
        with DBManager() as db:
            if not car.status:
                car.status = "Available"  # default new car status
            db.add(car)
            db.flush()
            db.refresh(car)
            return car

    def update(self, car: Car) -> Car:
        with DBManager() as db:
            db.add(car)
            db.commit()
            db.refresh(car)
            return car

    def soft_delete(self, car_id: int) -> bool:
        """Mark car as deleted (soft delete)."""
        with DBManager() as db:
            car = db.get(Car, car_id)
            if not car:
                return False
            car.status = "Deleted"
            db.commit()
            return True

    def restore(self, car_id: int) -> bool:
        """Restore a previously soft-deleted car."""
        with DBManager() as db:
            car = db.get(Car, car_id)
            if not car:
                return False
            if not car.status or car.status == "Deleted":
                car.status = "Available"
            db.commit()
            return True

    def get_by_id(self, car_id: int, include_deleted: bool = False) -> Optional[Car]:
        with DBManager() as db:
            q = db.query(Car).filter(Car.id == car_id)
            if not include_deleted:
                q = q.filter(Car.status != "Deleted")
            return q.first()

    def list(self, include_deleted: bool = False) -> List[Car]:
        with DBManager() as db:
            q = db.query(Car)
            if not include_deleted:
                q = q.filter(Car.status != "Deleted")
            return q.order_by(Car.make, Car.model, Car.year).all()
        
    def get_all(self, include_deleted: bool = False) -> List[Car]:
        with DBManager() as db:
            q = db.query(Car)
            if not include_deleted:
                q = q.filter(Car.status != "Deleted")
            return q.order_by(Car.make, Car.model, Car.year).all()
        
    def update_status(self, car_id: int, status: str) -> bool:
        """Update only the car's status."""
        with DBManager() as db:
            car = db.get(Car, car_id)
            if not car:
                return False
            car.status = status
            db.commit()
            return True
        
    def update(self, car: Car) -> Car:
        with DBManager() as db:
            existing = db.get(Car, car.id)
            if not existing:
                return None
            # overwrite fields
            existing.make = car.make
            existing.model = car.model
            existing.year = car.year
            existing.vtype = car.vtype
            existing.base_rate = car.base_rate
            existing.status = car.status
            db.commit()
            db.refresh(existing)
            return existing
