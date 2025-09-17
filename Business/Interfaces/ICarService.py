from abc import ABC, abstractmethod
from Contracts.CarDto import CarDto
from typing import List, Optional

class ICarService(ABC):
    """Interface defining business logic operations for Car service."""

    @abstractmethod
    def add_car(self, car: CarDto) -> CarDto:
        """Add a new car (default status = Available)."""
        pass

    @abstractmethod
    def list_cars(self, include_deleted: bool = False, sort_by: str = "id") -> List[CarDto]:
        """List all cars, optionally including those with status=Deleted."""
        pass

    @abstractmethod
    def list_available_cars(self, sort_by: str = "rate") -> List[CarDto]:
        """List only cars with status=Available."""
        pass

    @abstractmethod
    def update_car(self, dto: CarDto) -> Optional[CarDto]:
        """Update car details (make, model, year, vtype, base_rate, status)."""
        pass

    @abstractmethod
    def delete_car(self, car_id: int) -> bool:
        """Soft delete a car (set status=Deleted)."""
        pass

    @abstractmethod
    def restore_car(self, car_id: int) -> bool:
        """Restore a deleted car (set status=Available)."""
        pass

    @abstractmethod
    def rent_car(self, car_id: int) -> bool:
        """Mark car as Active (when a rental starts)."""
        pass
    
    @abstractmethod
    def get_by_id(self, car_id: int) -> Optional[CarDto]:
        """Fetch a car by its ID (excluding deleted ones)."""
        pass

    @abstractmethod
    def return_car(self, car_id: int) -> bool:
        """Mark car as Available (when rental ends)."""
        pass

    @abstractmethod
    def send_to_maintenance(self, car_id: int) -> bool:
        """Mark car as under Maintenance (not rentable)."""
        pass
