from Business.Interfaces.IRentalService import IRentalService
from Domain.Interfaces.IRentalRepository import IRentalRepository
from Domain.Mappers.RentalMapper import RentalMapper
from Contracts.RentalDto import RentalDto
from datetime import datetime

class RentalService(IRentalService):
    def __init__(self, repo: IRentalRepository, car_service, user_service):
        self.repo = repo
        self.car_service = car_service
        self.user_service = user_service

    def create_rental(self, dto: RentalDto) -> RentalDto:
        rental = RentalMapper.from_dto(dto)
        saved = self.repo.add(rental)
        return RentalMapper.to_dto(saved)

    def list_rentals(self, include_deleted: bool = False, sort_by: str = "start_date") -> list[RentalDto]:
        rentals = self.repo.get_all(include_deleted=include_deleted)
        if not include_deleted:
            rentals = [r for r in rentals if r.status != "Deleted"]
        dtos = [RentalMapper.to_dto(r) for r in rentals]
        return sorted(dtos, key=lambda r: getattr(r, sort_by, r.id))
    
    def list_rentals_by_customer(self, user_id: int, include_deleted: bool = False):
        rentals = self.repo.get_all(include_deleted=include_deleted)
        rentals = [r for r in rentals if r.user_id == user_id]
        return [RentalMapper.to_dto(r) for r in rentals]

    def list_active_rentals(self) -> list[RentalDto]:
        rentals = self.repo.get_all()
        active = [r for r in rentals if r.status == "Active"]
        return [RentalMapper.to_dto(r) for r in active]

    def approve_and_start_rental(self, rental_id: int) -> bool:
        """Approve a rental request and activate it immediately."""
        rental = self.repo.get_by_id(rental_id)
        if not rental or rental.status == "Deleted":
            return False

        car = self.car_service.get_by_id(rental.car_id)
        if not car or car.status == "Deleted":
            return False

        # Calculate rental duration
        start = datetime.strptime(rental.start_date, "%Y-%m-%d")
        end = datetime.strptime(rental.end_date, "%Y-%m-%d")
        days = max((end - start).days, 1)

        total_cost = car.base_rate * days

        # Update rental status and cost
        updated = self.repo.update_status(rental_id, "Active")
        if updated:
            self.repo.update_total_cost(rental_id, total_cost)
            self.car_service.rent_car(rental.car_id)
            self.print_receipt(rental, car, days, total_cost, "INITIAL RECEIPT")

        return updated

    def reject_rental(self, rental_id: int) -> bool:
        return self.repo.update_status(rental_id, "Rejected")

    def complete_rental(self, rental_id: int, actual_return: datetime) -> bool:
        rental = self.repo.get_by_id(rental_id)
        if not rental or rental.status == "Deleted":
            return False

        car = self.car_service.get_by_id(rental.car_id)
        if not car or car.status == "Deleted":
            return False

        start = datetime.strptime(rental.start_date, "%Y-%m-%d")
        days = max((actual_return - start).days, 1)

        total_cost = car.base_rate * days

        updated = self.repo.update_status(rental_id, "Completed")
        if updated:
            self.repo.update_total_cost(rental_id, total_cost)
            self.car_service.return_car(rental.car_id)
            self.print_receipt(rental, car, days, total_cost, "FINAL RECEIPT")

        return updated

    def cancel_rental(self, rental_id: int) -> bool:
        return self.repo.update_status(rental_id, "Cancelled")

    def delete_rental(self, rental_id: int) -> bool:
        return self.repo.update_status(rental_id, "Deleted")
    
    def print_receipt(self, rental, car, days: int, total_cost: float, title="RECEIPT"):
        # Fetch user (assuming you have user_service injected)
        customer = self.user_service.get_by_id(rental.user_id)

        print(f"\n===== {title} =====")
        print(f"Rental ID   : {rental.id}")
        print(f"Customer    : {customer.name} ({customer.email})")  # ✅ name instead of ID
        print(f"Car         : {car.make} {car.model} ({car.year})")
        print(f"Period      : {rental.start_date} → {rental.end_date} ({days} days)")
        print(f"Rate/Day    : ${car.base_rate:.2f}")
        print(f"Total Cost  : ${total_cost:.2f}")
        print("==========================\n")

