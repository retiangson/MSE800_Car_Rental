from abc import ABC, abstractmethod

class IRentalService(ABC):
    @abstractmethod
    def create_rental(self, rental):
        """Create a new rental"""
        pass

    @abstractmethod
    def list_rentals(self, include_deleted=False, sort_by="start_date"):
        """List all rentals, optionally including those with status=Deleted"""
        pass

    @abstractmethod
    def list_active_rentals(self):
        """List rentals with status=Active"""
        pass

    @abstractmethod
    def approve_rental(self, rental_id):
        """Mark rental as Approved"""
        pass

    @abstractmethod
    def reject_rental(self, rental_id):
        """Mark rental as Rejected"""
        pass

    @abstractmethod
    def start_rental(self, rental_id):
        """Mark rental as Active (when it begins)"""
        pass

    @abstractmethod
    def complete_rental(self, rental_id, car_service):
        """Mark rental as Completed and set car Available again"""
        pass

    @abstractmethod
    def cancel_rental(self, rental_id):
        """Mark rental as Cancelled"""
        pass

    @abstractmethod
    def delete_rental(self, rental_id):
        """Soft delete rental (set status=Deleted)"""
        pass
