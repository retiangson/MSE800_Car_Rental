from abc import ABC, abstractmethod

class ICarRepository(ABC):
    @abstractmethod
    def add(self, car):
        """Insert a new car"""
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False):
        """Retrieve all cars (optionally including those with status=Deleted)"""
        pass

    @abstractmethod
    def find_by_id(self, car_id):
        """Find a car by its ID"""
        pass

    @abstractmethod
    def update_status(self, car_id, status: str):
        """Update the car's status (Available, Active, Maintenance, Deleted)"""
        pass
