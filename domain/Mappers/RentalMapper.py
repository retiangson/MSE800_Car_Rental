from Domain.Models.Rental import Rental
from Contracts.RentalDto import RentalDto

class RentalMapper:
    """
    Mapper for converting between Rental ORM model and RentalDto.
    Handles safe transfer of rental data between layers.
    """
    @staticmethod
    def to_dto(rental: Rental) -> RentalDto:
        """Convert Rental model to RentalDto."""
        return RentalDto(
            id=rental.id,
            car_id=rental.car_id,
            user_id=rental.user_id,
            start_date=rental.start_date,
            end_date=rental.end_date,
            total_cost=rental.total_cost,
            status=rental.status
        )

    @staticmethod
    def from_dto(dto: RentalDto) -> Rental:
        """Convert RentalDto to Rental model."""
        return Rental(
            id=dto.id,
            car_id=dto.car_id,
            user_id=dto.user_id,
            start_date=dto.start_date,
            end_date=dto.end_date,
            total_cost=dto.total_cost,
            status=dto.status or "Pending"
        )
