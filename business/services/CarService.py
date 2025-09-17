from Business.Interfaces.ICarService import ICarService
from Domain.Interfaces.ICarRepository import ICarRepository
from Domain.Mappers.CarMapper import CarMapper
from Contracts.CarDto import CarDto
from Contracts.Enums.StatusEnums import CarStatus

class CarService(ICarService):
    """Service layer for managing cars (CRUD, availability, status changes)."""

    def __init__(self, repo: ICarRepository):
        """Initialize with a CarRepository implementation."""
        self.repo = repo

    def add_car(self, dto: CarDto) -> CarDto:
        """Add a new car (default status = Available if none provided)."""
        car = CarMapper.from_dto(dto)
        if not car.status:                 # Avoid redundant overwrite
            car.status = CarStatus.AVAILABLE      # Enforce default only if None
        saved = self.repo.add(car)
        return CarMapper.to_dto(saved)

    def list_cars(self, include_deleted: bool = False, sort_by: str = "id") -> list[CarDto]:
        """List all cars, optionally including deleted ones."""
        cars = self.repo.get_all(include_deleted=include_deleted)
        dtos = [CarMapper.to_dto(c) for c in cars]
        return sorted(dtos, key=lambda c: getattr(c, sort_by, c.id))

    def list_available_cars(self, sort_by: str = "base_rate") -> list[CarDto]:
        """List cars available for rental, sorted by base_rate (default)."""
        cars = self.repo.get_all()
        available = [c for c in cars if c.status == CarStatus.AVAILABLE]
        dtos = [CarMapper.to_dto(c) for c in available]
        return sorted(dtos, key=lambda c: getattr(c, sort_by, c.id))
    
    def delete_car(self, car_id: int) -> bool:
        """Soft delete a car (mark status as Deleted)."""
        return self.repo.update_status(car_id, CarStatus.DELETED)
    
    def restore_car(self, car_id: int) -> bool:
        """Restore a previously deleted car (set status back to Available)."""
        return self.repo.update_status(car_id, CarStatus.AVAILABLE)
    
    def rent_car(self, car_id: int) -> bool:
        """Mark car as Active when a rental begins."""
        return self.repo.update_status(car_id, CarStatus.ACTIVE)

    def get_by_id(self, car_id: int, include_deleted: bool = False)-> CarDto | None:
        """Fetch a car by its ID (excludes Deleted)."""
        car = self.repo.get_by_id(car_id, include_deleted=include_deleted)
        return CarMapper.to_dto(car) if car else None
    
    def return_car(self, car_id: int) -> bool:
        """Mark car as Available when a rental ends."""
        return self.repo.update_status(car_id, CarStatus.AVAILABLE)

    def send_to_maintenance(self, car_id: int) -> bool:
        """Mark car as under Maintenance (not rentable)."""
        return self.repo.update_status(car_id, CarStatus.MAINTENANCE)

    def update_car(self, dto: CarDto) -> CarDto | None:
        """Update car details and return updated DTO (None if not found)."""
        car = CarMapper.from_dto(dto)
        updated = self.repo.update(car)
        return CarMapper.to_dto(updated) if updated else None
