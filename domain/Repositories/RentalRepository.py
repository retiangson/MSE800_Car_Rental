from typing import Optional, List
from Domain.Interfaces.IRentalRepository import IRentalRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.Rental import Rental

class RentalRepository(IRentalRepository):
    def __init__(self):
        pass

    def add(self, rental: Rental) -> Rental:
        with DBManager() as db:
            if not rental.status:
                rental.status = "Pending"  # default for new rentals
            db.add(rental)
            db.flush()
            db.refresh(rental)
            return rental

    def get_all(self, include_deleted: bool = False) -> List[Rental]:
        with DBManager() as db:
            q = db.query(Rental)
            if not include_deleted:
                q = q.filter(Rental.status != "Deleted")
            return q.all()

    def get_by_id(self, rental_id: int, include_deleted: bool = False) -> Optional[Rental]:
        with DBManager() as db:
            q = db.query(Rental).filter(Rental.id == rental_id)
            if not include_deleted:
                q = q.filter(Rental.status != "Deleted")
            return q.first()

    def soft_delete(self, rental_id: int) -> bool:
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.status = "Deleted"
            db.commit()
            return True

    def restore(self, rental_id: int) -> bool:
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.status = "Pending"  # or "Active", depending on workflow
            db.commit()
            return True

    def update_status(self, rental_id: int, status: str) -> bool:
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.status = status
            db.commit()
            return True

    def update_total_cost(self, rental_id: int, total_cost: float) -> bool:
        with DBManager() as db:
            rental = db.get(Rental, rental_id)
            if not rental:
                return False
            rental.total_cost = total_cost
            db.commit()
