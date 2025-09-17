from Business.Interfaces.IRentalService import IRentalService
from Domain.Interfaces.IRentalRepository import IRentalRepository
from Domain.Mappers.RentalMapper import RentalMapper
from Contracts.RentalDto import RentalDto
from datetime import datetime
from Business.Utils.RentalCalculator import RentalCalculator
from Business.Utils.ReceiptPrinter import ReceiptPrinter
from Contracts.Enums.StatusEnums import RentalStatus

class RentalService(IRentalService):
    """Service layer for managing rentals (create, approve, complete, cancel)."""

    def __init__(self, repo: IRentalRepository, car_service, user_service):
        """Initialize with repository and dependent services (Car, User)."""
        self.repo = repo
        self.car_service = car_service
        self.user_service = user_service

    def create_rental(self, dto: RentalDto) -> RentalDto:
        """Create a new rental (default status = Pending)."""
        rental = RentalMapper.from_dto(dto)
        saved = self.repo.add(rental)
        return RentalMapper.to_dto(saved)

    def list_rentals(self, include_deleted: bool = False, sort_by: str = "start_date") -> list[RentalDto]:
        """List all rentals, sorted by field (default start_date)."""
        rentals = self.repo.get_all(include_deleted=include_deleted)
        if not include_deleted:
            rentals = [r for r in rentals if r.status != RentalStatus.DELETED]
        dtos = [RentalMapper.to_dto(r) for r in rentals]
        return sorted(dtos, key=lambda r: getattr(r, sort_by, r.id))
    
    def list_rentals_by_customer(self, user_id: int, include_deleted: bool = False):
        """List all rentals for a specific customer."""
        rentals = self.repo.get_all(include_deleted=include_deleted)
        rentals = [r for r in rentals if r.user_id == user_id]
        return [RentalMapper.to_dto(r) for r in rentals]

    def list_active_rentals(self) -> list[RentalDto]:
        """List rentals currently marked as Active."""
        rentals = self.repo.get_all()
        active = [r for r in rentals if r.status == RentalStatus.ACTIVE]
        return [RentalMapper.to_dto(r) for r in active]
    
    def get_rentals_by_status(self, status: str, include_deleted: bool = False) -> list[RentalDto]:
        """
        Get all rentals filtered by status.
        
        Args:
            status (str): Rental status to filter by (e.g., "Pending", RentalStatus.ACTIVE, RentalStatus.COMPLETED).
            include_deleted (bool): Whether to include rentals marked as Deleted.
        
        Returns:
            list[RentalDto]: List of rentals with the given status.
        """
        rentals = self.repo.get_all(include_deleted=include_deleted)
        filtered = [r for r in rentals if r.status == status]
        return [RentalMapper.to_dto(r) for r in filtered]

    def approve_and_start_rental(self, rental_id: int) -> bool:
        rental = self.repo.get_by_id(rental_id)
        if not rental or rental.status == RentalStatus.DELETED:
            return False

        car = self.car_service.get_by_id(rental.car_id)
        if not car or car.status == RentalStatus.DELETED:
            return False

        days = RentalCalculator.calculate_days(rental.start_date, rental.end_date)
        total_cost = RentalCalculator.calculate_cost(car.base_rate, days)

        updated = self.repo.update_status(rental_id, RentalStatus.ACTIVE)
        if updated:
            self.repo.update_total_cost(rental_id, total_cost)
            self.car_service.rent_car(rental.car_id)

            customer = self.user_service.get_by_id(rental.user_id)
            ReceiptPrinter.print_receipt(rental, car, customer, days, total_cost, "INITIAL RECEIPT")

        return updated

    def reject_rental(self, rental_id: int) -> bool:
        """Reject a rental request."""
        return self.repo.update_status(rental_id, RentalStatus.REJECTED)

    def complete_rental(self, rental_id: int, actual_return: datetime) -> bool:
        rental = self.repo.get_by_id(rental_id)
        if not rental or rental.status == RentalStatus.DELETED:
            return False

        car = self.car_service.get_by_id(rental.car_id)
        if not car or car.status == RentalStatus.DELETED:
            return False

        days = RentalCalculator.calculate_days(rental.start_date, actual_return, actual_return=True)
        total_cost = RentalCalculator.calculate_cost(car.base_rate, days)

        updated = self.repo.update_status(rental_id, RentalStatus.COMPLETED)
        if updated:
            self.repo.update_total_cost(rental_id, total_cost)
            self.car_service.return_car(rental.car_id)

            customer = self.user_service.get_by_id(rental.user_id)
            ReceiptPrinter.print_receipt(rental, car, customer, days, total_cost, "FINAL RECEIPT")

        return updated

    def cancel_rental(self, rental_id: int) -> bool:
        """Cancel a rental request."""
        return self.repo.update_status(rental_id, RentalStatus.CANCELLED)

    def delete_rental(self, rental_id: int) -> bool:
        """Soft delete a rental (mark as Deleted)."""
        return self.repo.update_status(rental_id, RentalStatus.DELETED)
