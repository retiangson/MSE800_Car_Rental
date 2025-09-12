from Business.Services.Interfaces.IRentalService import IRentalService
from Domain.Interfaces.IRentalRepository import IRentalRepository
from datetime import datetime

class RentalService(IRentalService):
    def __init__(self, repo: IRentalRepository, car_service):
        self.repo = repo
        self.car_service = car_service  # ✅ injected dependency

    def create_rental(self, rental):
        return self.repo.add(rental)

    def list_rentals(self, include_deleted=False, sort_by="start_date"):
        rentals = self.repo.get_all(include_deleted=include_deleted)
        return sorted(rentals, key=lambda r: getattr(r, sort_by, r.id))

    def list_active_rentals(self):
        rentals = self.repo.get_all()
        # Active rentals = status == "Active"
        return list(filter(lambda r: r.status == "Active", rentals))

    def approve_and_start_rental(self, rental_id):
        """Approve and immediately start rental, set cost, and print receipt."""
        rental = self.repo.find_by_id(rental_id)
        if not rental:
            return False

        car = self.car_service.repo.find_by_id(rental.car_id)
        if not car:
            return False

        # Calculate rental days based on planned dates
        start = datetime.strptime(rental.start_date, "%Y-%m-%d")
        end = datetime.strptime(rental.end_date, "%Y-%m-%d")
        days = max((end - start).days, 1)

        total_cost = car.rate * days

        # Update rental status and total cost
        updated = self.repo.update_status(rental_id, "Active")
        if updated:
            self.repo.update_total_cost(rental_id, total_cost)
            self.car_service.rent_car(rental.car_id)
            self.print_receipt(rental, car, days, total_cost, "INITIAL RECEIPT")

        return updated

    def reject_rental(self, rental_id):
        return self.repo.update_status(rental_id, "Rejected")

    def complete_rental(self, rental_id, actual_return: datetime):
        """Complete rental, recalc cost based on actual return date, free car, and print final receipt."""
        rental = self.repo.find_by_id(rental_id)
        if not rental:
            return False

        car = self.car_service.repo.find_by_id(rental.car_id)
        if not car:
            return False

        # Calculate actual rental days
        start = datetime.strptime(rental.start_date, "%Y-%m-%d")
        days = max((actual_return - start).days, 1)

        total_cost = car.rate * days

        # Update rental
        updated = self.repo.update_status(rental_id, "Completed")
        if updated:
            self.repo.update_total_cost(rental_id, total_cost)
            self.car_service.return_car(rental.car_id)
            self.print_receipt(rental, car, days, total_cost, "FINAL RECEIPT")

        return updated

    def cancel_rental(self, rental_id):
        return self.repo.update_status(rental_id, "Cancelled")

    def delete_rental(self, rental_id):
        # Soft delete → status = Deleted
        return self.repo.update_status(rental_id, "Deleted")
    
    def print_receipt(self, rental, car, days, total_cost, title="RECEIPT"):
        print(f"\n===== {title} =====")
        print(f"Rental ID   : {rental.id}")
        print(f"Customer    : {rental.name}")
        print(f"Car         : {car.make} {car.model} ({car.year})")
        print(f"Period      : {rental.start_date} → {rental.end_date} ({days} days)")
        print(f"Rate/Day    : ${car.rate:.2f}")
        print(f"Total Cost  : ${total_cost:.2f}")
        print("==========================\n")
