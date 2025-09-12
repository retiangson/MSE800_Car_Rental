from Business.Services.Interfaces.IRentalService import IRentalService
from Domain.Interfaces.IRentalRepository import IRentalRepository

class RentalService(IRentalService):
    def __init__(self, repo: IRentalRepository):
        self.repo = repo

    def create_rental(self, rental):
        return self.repo.add(rental)

    def list_rentals(self, include_deleted=False, sort_by="start_date"):
        rentals = self.repo.get_all(include_deleted=include_deleted)
        return sorted(rentals, key=lambda r: getattr(r, sort_by, r.id))

    def list_active_rentals(self):
        rentals = self.repo.get_all()
        # Active rentals = status == "Active"
        return list(filter(lambda r: r.status == "Active", rentals))

    def approve_rental(self, rental_id):
        return self.repo.update_status(rental_id, "Approved")

    def reject_rental(self, rental_id):
        return self.repo.update_status(rental_id, "Rejected")

    def start_rental(self, rental_id):
        return self.repo.update_status(rental_id, "Active")

    def complete_rental(self, rental_id, car_service):
        # mark rental completed
        updated = self.repo.update_status(rental_id, "Completed")
        if updated:
            # mark car available again
            rental = self.repo.find_by_id(rental_id)
            if rental:
                car_service.return_car(rental.car_id)  # reuse CarService method
        return updated

    def cancel_rental(self, rental_id):
        return self.repo.update_status(rental_id, "Cancelled")

    def delete_rental(self, rental_id):
        # Soft delete → status = Deleted
        return self.repo.update_status(rental_id, "Deleted")
