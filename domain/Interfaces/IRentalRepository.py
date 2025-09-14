from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Models.Rental import Rental

class IRentalRepository(ABC):
    @abstractmethod
    def add(self, rental: Rental) -> Rental:
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Rental]:
        pass

    @abstractmethod
    def get_by_id(self, rental_id: int, include_deleted: bool = False) -> Optional[Rental]:
        pass

    @abstractmethod
    def soft_delete(self, rental_id: int) -> bool:
        pass

    @abstractmethod
    def restore(self, rental_id: int) -> bool:
        pass

    @abstractmethod
    def update_status(self, rental_id: int, status: str) -> bool:
        pass

    @abstractmethod
    def update_total_cost(self, rental_id: int, total_cost: float) -> bool:
        pass
