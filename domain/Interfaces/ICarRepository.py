from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Models.Car import Car

class ICarRepository(ABC):
    @abstractmethod
    def add(self, car: Car) -> Car:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Car]:
        pass

    @abstractmethod
    def get_by_id(self, car_id: int) -> Optional[Car]:
        pass

    @abstractmethod
    def update_status(self, car_id: int, status: str) -> bool:
        pass

    @abstractmethod
    def soft_delete(self, car_id: int) -> bool:
        pass

    @abstractmethod
    def restore(self, car_id: int) -> bool:
        pass
    
    @abstractmethod
    def get_by_id(self, car_id: int, include_deleted: bool = False) -> Optional[Car]:
        pass