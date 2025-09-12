from abc import ABC, abstractmethod

class ICarRepository(ABC):
    @abstractmethod
    def add(self, car): pass

    @abstractmethod
    def get_all(self): pass

    @abstractmethod
    def find_by_id(self, car_id): pass

    @abstractmethod
    def update_status(self, car_id, status): pass