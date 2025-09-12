from abc import ABC, abstractmethod

class ICarService(ABC):
    @abstractmethod
    def add_car(self, car): pass

    @abstractmethod
    def list_cars(self, include_deleted=False, sort_by="id"): pass

    @abstractmethod
    def list_available_cars(self, sort_by="rate"): pass

    @abstractmethod
    def delete_car(self, car_id): pass   # this will mark as Deleted

    @abstractmethod
    def rent_car(self, car_id): pass     # set status = Rented

    @abstractmethod
    def return_car(self, car_id): pass   # set status = Available

    @abstractmethod
    def send_to_maintenance(self, car_id): pass   # set status = Maintenance
