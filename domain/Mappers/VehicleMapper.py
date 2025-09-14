# Domain/Mappers/VehicleMapper.py
from Domain.Models.Vehicle import Vehicle
from Contracts.VehicleDto import VehicleDto

class VehicleMapper:
    @staticmethod
    def to_dto(vehicle: Vehicle) -> VehicleDto:
        return VehicleDto(
            id=vehicle.id,
            make=vehicle.make,
            model=vehicle.model,
            year=vehicle.year,
            vtype=vehicle.vtype,
            base_rate=vehicle.base_rate,
            status=vehicle.status
        )

    @staticmethod
    def from_dto(dto: VehicleDto) -> Vehicle:
        return Vehicle(
            id=dto.id,
            make=dto.make,
            model=dto.model,
            year=dto.year,
            vtype=dto.vtype,
            base_rate=dto.base_rate,
            status=dto.status
        )
