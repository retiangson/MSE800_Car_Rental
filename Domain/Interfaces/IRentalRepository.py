from abc import ABC, abstractmethod
from typing import List, Optional
from Domain.Models.Rental import Rental
from Contracts.Enums.StatusEnums import RentalStatus

class IRentalRepository(ABC):
    """Interface defining CRUD and soft-delete operations for Rental."""

    @abstractmethod
    def add(self, rental: Rental) -> Rental:
        """Add a new rental record."""
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False) -> List[Rental]:
        """Retrieve all rentals (optionally include deleted ones)."""
        pass

    @abstractmethod
    def get_by_id(self, rental_id: int, include_deleted: bool = False) -> Optional[Rental]:
        """Get a rental by its ID (exclude deleted by default)."""
        pass

    @abstractmethod
    def soft_delete(self, rental_id: int) -> bool:
        """Mark a rental as Deleted instead of removing it."""
        pass

    @abstractmethod
    def restore(self, rental_id: int) -> bool:
        """Restore a previously soft-deleted rental."""
        pass

    @abstractmethod
    def update_status(self, rental_id: int, status: RentalStatus) -> bool:
        """Update only the rental's status (Pending, Approved, Active, Completed, etc.)."""
        pass

    @abstractmethod
    def update_total_cost(self, rental_id: int, total_cost: float) -> bool:
        """Update the total cost for a rental."""
        pass
