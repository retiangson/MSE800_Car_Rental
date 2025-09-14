from Domain.Models.Car import Car
from Contracts.CarDto import CarDto

class CarMapper:
    @staticmethod
    def to_dto(car: Car) -> CarDto:
        return CarDto(
            id=car.id,
            make=car.make,
            model=car.model,
            year=car.year,
            vtype=car.vtype,
            base_rate=car.base_rate,
            status=car.status
        )

    @staticmethod
    def from_dto(dto: CarDto) -> Car:
        return Car(
            id=dto.id,
            make=dto.make,
            model=dto.model,
            year=dto.year,
            vtype=dto.vtype,
            base_rate=dto.base_rate,
            status=dto.status or "Available"
        )
