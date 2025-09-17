from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Models.Car import Car
from Contracts.Enums.StatusEnums import CarStatus

class ICarRepository(ABC):
    """Interface defining CRUD and soft-delete operations for Car."""

    @abstractmethod
    def add(self, car: Car) -> Car:
        """Add a new car to the database."""
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Car]:
        """Retrieve all cars (optionally include deleted ones)."""
        pass

    @abstractmethod
    def get_by_id(self, car_id: int, include_deleted: bool = False) -> Optional[Car]:
        """Get a car by its ID (exclude deleted by default)."""
        pass

    @abstractmethod
    def update_status(self, car_id: int, status: CarStatus) -> bool:
        """Update only the car's status (Available, Inactive, Deleted)."""
        pass

    @abstractmethod
    def soft_delete(self, car_id: int) -> bool:
        """Mark a car as Deleted instead of removing it."""
        pass

    @abstractmethod
    def restore(self, car_id: int) -> bool:
        """Restore a previously soft-deleted car."""
        pass

    @abstractmethod
    def update(self, car: Car) -> Optional[Car]:
        """Update full car details (make, model, year, type, base_rate, status)."""
        pass
