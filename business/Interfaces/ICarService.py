from abc import ABC, abstractmethod
from Contracts.CarDto import CarDto
from typing import List, Optional

class ICarService(ABC):
    @abstractmethod
    def add_car(self, car):
        """Add a new car (default status = Available)"""
        pass

    @abstractmethod
    def list_cars(self, include_deleted=False, sort_by="id"):
        """List all cars, optionally including those with status=Deleted"""
        pass

    @abstractmethod
    def list_available_cars(self, sort_by="rate"):
        """List only cars with status=Available"""
        pass

    @abstractmethod
    def update_car(self, dto: CarDto) -> Optional[CarDto]:
        """Update car details (make, model, year, vtype, base_rate, status)."""

    @abstractmethod
    def delete_car(self, car_id):
        """Soft delete a car (set status=Deleted)"""
        pass

    @abstractmethod
    def restore_car(self, car_id):
        """Restore a deleted car (set status=Available)"""
        pass

    @abstractmethod
    def rent_car(self, car_id):
        """Mark car as Active (when a rental starts)"""
        pass
    
    def get_by_id(self, car_id: int) -> bool:
        pass

    @abstractmethod
    def return_car(self, car_id):
        """Mark car as Available (when rental ends)"""
        pass

    @abstractmethod
    def send_to_maintenance(self, car_id):
        """Mark car as Maintenance"""
        pass