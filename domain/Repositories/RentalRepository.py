from typing import Optional, List
from Domain.Interfaces.IRentalRepository import IRentalRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.Rental import Rental

class RentalRepository(IRentalRepository):
    """
    Repository for managing Rental entities in the database.
    Provides CRUD, soft delete, restore, and utility methods for rentals.
    """
    def __init__(self):
        pass

    def add(self, rental: Rental) -> Rental:
        """
        Add a new rental record to the database.
        Default status is 'Pending' if not specified.
        """
        with DBManager() as db:
            if not rental.status:
                rental.status = "Pending"  # default for new rentals
            db.add(rental)
            db.flush()
            db.refresh(rental)
            return rental

    def get_all(self, include_deleted: bool = False) -> List[Rental]:
        """
        Retrieve all rentals.
        By default excludes rentals marked as 'Deleted'.
        """
        with DBManager() as db:
            q = db.query(Rental)
            if not include_deleted:
                q = q.filter(Rental.status != "Deleted")
            return q.all()

    def get_by_id(self, rental_id: int, include_deleted: bool = False) -> Optional[Rental]:
        """
        Retrieve a rental by its ID.
        Excludes deleted rentals unless include_deleted=True.
        """
        with DBManager() as db:
            q = db.query(Rental).filter(Rental.id == rental_id)
            if not include_deleted:
                q = q.filter(Rental.status != "Deleted")
            return q.first()

    def soft_delete(self, rental_id: int) -> bool:
        """
        Soft delete a rental (mark as 'Deleted' instead of removing).
        Returns:
            True if successful, False if rental not found.
        """
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.status = "Deleted"
            db.commit()
            return True

    def restore(self, rental_id: int) -> bool:
        """
        Restore a previously soft-deleted rental.
        Sets status back to 'Pending' (or another initial status).
        Returns:
            True if successful, False if rental not found.
        """
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.status = "Pending"  # or "Active", depending on workflow
            db.commit()
            return True

    def update_status(self, rental_id: int, status: str) -> bool:
        """
        Update only the status of a rental.
        Example: Pending → Approved → Active → Completed.
        Returns True if updated, False if not found.
        """
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.status = status
            db.commit()
            return True

    def update_total_cost(self, rental_id: int, total_cost: float) -> bool:
        """
        Update the total rental cost for a given rental.
        Returns True if updated, False if rental not found.
        """
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.total_cost = total_cost
            db.commit()
