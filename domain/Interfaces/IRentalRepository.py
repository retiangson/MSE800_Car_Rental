from abc import ABC, abstractmethod

class IRentalRepository(ABC):
    @abstractmethod
    def add(self, rental): 
        """Insert a new rental record"""
        pass

    @abstractmethod
    def get_all(self, include_deleted: bool = False): 
        """Retrieve all rentals (optionally including Deleted ones)"""
        pass

    @abstractmethod
    def find_by_id(self, rental_id, include_deleted: bool = False): 
        """Find rental by ID (optionally including Deleted)"""
        pass

    @abstractmethod
    def delete(self, rental_id): 
        """Soft delete rental (set status = 'Deleted')"""
        pass

    @abstractmethod
    def update_status(self, rental_id, status: str): 
        """Update rental workflow status (Pending, Approved, Active, Completed, Cancelled, Deleted)"""
        pass
