from typing import List, Optional
from Domain.Repositories.DBManager import DBManager
from Domain.Models.Car import Car

class CarRepository:
    """
    Repository class for managing Car entities in the database.
    Encapsulates all CRUD operations and soft-delete functionality.
    """
    def add(self, car: Car) -> Car:
        """
        Add a new car to the database.
        If no status is provided, default to 'Available'.
        """
        with DBManager() as db:
            if not car.status:
                car.status = "Available"  # default new car status
            db.add(car)
            db.flush()
            db.refresh(car)
            return car

    def update(self, car: Car) -> Car:
        """
        Update an existing car with new values.
        Only works if the car already exists in DB.
        Returns the updated car, or None if not found.
        """
        with DBManager() as db:
            db.add(car)
            db.commit()
            db.refresh(car)
            return car

    def soft_delete(self, car_id: int) -> bool:
        """
        Perform a soft delete on a car.
        Instead of removing it, mark status as 'Deleted'.
        Returns True if successful, False if car not found.
        """
        with DBManager() as db:
            car = db.get(Car, car_id)
            if not car:
                return False
            car.status = "Deleted"
            db.commit()
            return True

    def restore(self, car_id: int) -> bool:
        """
        Restore a car previously marked as 'Deleted'.
        Sets status back to 'Available'.
        Returns True if successful, False if car not found.
        """
        with DBManager() as db:
            car = db.get(Car, car_id)
            if not car:
                return False
            if not car.status or car.status == "Deleted":
                car.status = "Available"
            db.commit()
            return True

    def get_by_id(self, car_id: int, include_deleted: bool = False) -> Optional[Car]:
        """
        Retrieve a car by its ID.
        By default, excludes soft-deleted cars unless include_deleted=True.
        """
        with DBManager() as db:
            q = db.query(Car).filter(Car.id == car_id)
            if not include_deleted:
                q = q.filter(Car.status != "Deleted")
            return q.first()

    def list(self, include_deleted: bool = False) -> List[Car]:
        """
        List all cars in the system.
        By default, excludes soft-deleted cars.
        Ordered by make, model, year.
        """
        with DBManager() as db:
            q = db.query(Car)
            if not include_deleted:
                q = q.filter(Car.status != "Deleted")
            return q.order_by(Car.make, Car.model, Car.year).all()
        
    def get_all(self, include_deleted: bool = False) -> List[Car]:
        """
        Alias for list(), included for compatibility.
        Returns all cars (active and optionally deleted).
        """
        with DBManager() as db:
            q = db.query(Car)
            if not include_deleted:
                q = q.filter(Car.status != "Deleted")
            return q.order_by(Car.make, Car.model, Car.year).all()
        
    def update_status(self, car_id: int, status: str) -> bool:
        """
        Update only the status of a car (e.g., Available, Inactive, Deleted).
        Returns True if update successful, False if car not found.
        """
        with DBManager() as db:
            car = db.get(Car, car_id)
            if not car:
                return False
            car.status = status
            db.commit()
            return True
        
    def update(self, car: Car) -> Car:
        """
        Update an existing car record with new values.

        Args:
            car (Car): Car object with updated values.
                    The `id` must correspond to an existing record.

        Returns:
            Car | None:
                - Updated Car object if found and updated.
                - None if no car with the given ID exists.
        """
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
