from Business.Interfaces.ICarService import ICarService
from Domain.Interfaces.ICarRepository import ICarRepository
from Domain.Mappers.CarMapper import CarMapper
from Contracts.CarDto import CarDto

class CarService(ICarService):
    def __init__(self, repo: ICarRepository):
        self.repo = repo

    def add_car(self, dto: CarDto) -> CarDto:
        car = CarMapper.from_dto(dto)
        if not car.status:                 # ✅ avoid redundant overwrite
            car.status = "Available"       # enforce default only if None
        saved = self.repo.add(car)
        return CarMapper.to_dto(saved)

    def list_cars(self, include_deleted: bool = False, sort_by: str = "id") -> list[CarDto]:
        cars = self.repo.get_all(include_deleted=include_deleted)
        dtos = [CarMapper.to_dto(c) for c in cars]
        return sorted(dtos, key=lambda c: getattr(c, sort_by, c.id))

    def list_available_cars(self, sort_by: str = "base_rate") -> list[CarDto]:  # ✅ fixed
        cars = self.repo.get_all()
        available = [c for c in cars if c.status == "Available"]
        dtos = [CarMapper.to_dto(c) for c in available]
        return sorted(dtos, key=lambda c: getattr(c, sort_by, c.id))
    
    def delete_car(self, car_id: int) -> bool:
        """Soft delete: mark car as Deleted"""
        return self.repo.update_status(car_id, "Deleted")
    
    def restore_car(self, car_id: int) -> bool:
        """Restore a previously deleted car"""
        return self.repo.update_status(car_id, "Available")
    
    def rent_car(self, car_id: int) -> bool:
        """Mark car as Active when a rental begins"""
        return self.repo.update_status(car_id, "Active")

    def get_by_id(self, car_id: int) -> bool:
        return self.repo.get_by_id(car_id)
    
    def return_car(self, car_id: int) -> bool:
        """Mark car as Available when rental ends"""
        return self.repo.update_status(car_id, "Available")

    def send_to_maintenance(self, car_id: int) -> bool:
        """Mark car as under Maintenance"""
        return self.repo.update_status(car_id, "Maintenance")

    def update_car(self, dto: CarDto) -> CarDto | None:
        car = CarMapper.from_dto(dto)
        updated = self.repo.update(car)
        return CarMapper.to_dto(updated) if updated else None
