from abc import ABC, abstractmethod
from typing import List
from Contracts.Enums.StatusEnums import RentalStatus

class IRentalService(ABC):
    @abstractmethod
    def create_rental(self, rental):
        """Create a new rental (status=Pending by default)."""
        pass

    @abstractmethod
    def list_rentals(self, include_deleted: bool = False, sort_by: str = "start_date"):
        """List all rentals, optionally including those with status=Deleted."""
        pass

    @abstractmethod
    def list_rentals_by_customer(self, user_id: int, include_deleted: bool = False):
        """List all rentals belonging to a specific customer."""
        pass

    @abstractmethod
    def list_active_rentals(self):
        """List rentals with status=Active."""
        pass

    @abstractmethod
    def get_rentals_by_status(self, status: RentalStatus, include_deleted: bool = False):
        """
        Get rentals filtered by status (e.g., Pending, Active, Completed).
        Optionally include deleted rentals.
        """
        pass

    @abstractmethod
    def approve_and_start_rental(self, rental_id: int):
        """
        Approve and immediately start a rental:
        - Set status = Active
        - Calculate initial cost (days * car rate)
        - Save total_cost
        - Mark car as Active
        - Print initial receipt
        """
        pass

    @abstractmethod
    def reject_rental(self, rental_id: int):
        """Mark rental as Rejected."""
        pass

    @abstractmethod
    def complete_rental(self, rental_id: int, actual_return=None):
        """
        Complete rental:
        - Set status = Completed
        - Recalculate cost using actual return date
        - Update total_cost
        - Mark car as Available
        - Print final receipt
        """
        pass

    @abstractmethod
    def cancel_rental(self, rental_id: int):
        """Mark rental as Cancelled."""
        pass

    @abstractmethod
    def delete_rental(self, rental_id: int):
        """Soft delete rental (set status=Deleted)."""
        pass
