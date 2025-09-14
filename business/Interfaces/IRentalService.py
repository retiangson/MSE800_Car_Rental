from abc import ABC, abstractmethod

class IRentalService(ABC):
    @abstractmethod
    def create_rental(self, rental):
        """Create a new rental (status=Pending by default)"""
        pass

    @abstractmethod
    def list_rentals(self, include_deleted=False, sort_by="start_date"):
        """List all rentals, optionally including those with status=Deleted"""
        pass

    @abstractmethod
    def list_rentals_by_customer(self, user_id: int, include_deleted: bool = False):
        pass

    @abstractmethod
    def list_active_rentals(self):
        """List rentals with status=Active"""
        pass

    @abstractmethod
    def approve_and_start_rental(self, rental_id):
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
    def reject_rental(self, rental_id):
        """Mark rental as Rejected"""
        pass

    @abstractmethod
    def complete_rental(self, rental_id):
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
    def cancel_rental(self, rental_id):
        """Mark rental as Cancelled"""
        pass

    @abstractmethod
    def delete_rental(self, rental_id):
        """Soft delete rental (set status=Deleted)"""
        pass
