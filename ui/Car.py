from Contracts.CarDto import CarDto
from Contracts.Enums.StatusEnums import CarStatus

def safe_int_input(prompt: str) -> int:
    """Ensure user enters a valid integer."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")

def safe_float_input(prompt: str) -> float:
    """Ensure user enters a valid float."""
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid decimal number.")

class CarUI:
    """UI layer for managing car operations (add, update, list, delete, restore, etc.)."""

    def __init__(self, car_service):
        """Initialize with CarService dependency."""
        self._car_service = car_service  

    def add_car_ui(self):
        """Prompt user for car details and add a new car."""
        try:
            make = input("Enter make: ").strip()
            model = input("Enter model: ").strip()
            year = safe_int_input("Enter year: ")
            vtype = input("Enter type (e.g., sedan/suv/ev): ").strip()
            base_rate = safe_float_input("Enter daily base rate: ")

            if not make or not model or not vtype:
                print("Make, model, and type cannot be empty.")
                return

            new_car_dto = CarDto(
                id=None,
                make=make,
                model=model,
                year=year,
                vtype=vtype,
                base_rate=base_rate,
                status=CarStatus.AVAILABLE
            )

            saved_car = self._car_service.add_car(new_car_dto)
            print(f"Car added successfully: {saved_car.make} {saved_car.model} "
                  f"({saved_car.year}) - ${saved_car.base_rate}/day, status={saved_car.status}.")
        except Exception as e:
            print(f"Error adding car: {e}")

    def update_car_ui(self):
        """Prompt user for updates to an existing car."""
        try:
            car_id = safe_int_input("Enter Car ID to update: ")
            existing = self._car_service.get_by_id(car_id)
            if not existing:
                print("Car not found.")
                return

            print("Leave blank to keep current value.")

            make = input(f"Enter new make [{existing.make}]: ").strip() or existing.make
            model = input(f"Enter new model [{existing.model}]: ").strip() or existing.model
            year_input = input(f"Enter new year [{existing.year}]: ").strip()
            year = int(year_input) if year_input else existing.year
            vtype = input(f"Enter new type [{existing.vtype}]: ").strip() or existing.vtype
            base_rate_input = input(f"Enter new base rate [{existing.base_rate}]: ").strip()
            base_rate = float(base_rate_input) if base_rate_input else existing.base_rate
            status = input(f"Enter new status [{existing.status}]: ").strip() or existing.status

            updated_dto = CarDto(
                id=car_id,
                make=make,
                model=model,
                year=year,
                vtype=vtype,
                base_rate=base_rate,
                status=status
            )

            updated_car = self._car_service.update_car(updated_dto)
            if updated_car:
                print(f"Car updated: {updated_car.make} {updated_car.model} ({updated_car.year}), "
                      f"${updated_car.base_rate}/day, status={updated_car.status}")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error updating car: {e}")

    def list_cars_ui(self):
        """List all cars (including deleted ones)."""
        print("\n📋 All Cars:")
        try:
            cars = self._car_service.list_cars(include_deleted=True)
            if not cars:
                print("No cars found.")
                return
            for car in cars:
                print(f"{car.id}: {car.make} {car.model} ({car.year}) - "
                      f"${car.base_rate}/day - Status: {car.status}")
        except Exception as e:
            print(f"Error listing cars: {e}")

    def list_available_cars_ui(self):
        """List only cars available for rental."""
        print("\n🚗 Available Cars:")
        try:
            cars = self._car_service.list_available_cars()
            if not cars:
                print("No available cars.")
                return
            for car in cars:
                print(f"{car.id}: {car.make} {car.model} ({car.year}) - "
                      f"${car.base_rate}/day - Status: {car.status}")
        except Exception as e:
            print(f"Error listing available cars: {e}")

    def delete_car_ui(self):
        """Soft delete a car (mark status as Deleted)."""
        try:
            car_id = safe_int_input("Enter Car ID to mark as Deleted: ")
            if self._car_service.delete_car(car_id):
                print("🗑 Car marked as Deleted.")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error deleting car: {e}")

    def restore_car_ui(self):
        """Restore a previously deleted car (set status to Available)."""
        try:
            car_id = safe_int_input("Enter Car ID to restore (make Available): ")
            if self._car_service.restore_car(car_id):
                print("Car restored and set to Available.")
            else:
                print("Car not found or not in Deleted status.")
        except Exception as e:
            print(f"Error restoring car: {e}")

    def rent_car_ui(self):
        """Mark a car as Active (rented)."""
        try:
            car_id = safe_int_input("Enter Car ID to mark as Active (rented): ")
            if self._car_service.rent_car(car_id):
                print("Car marked as Active (rented).")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error renting car: {e}")

    def return_car_ui(self):
        """Mark a car as Available (returned)."""
        try:
            car_id = safe_int_input("Enter Car ID to mark as Available (returned): ")
            if self._car_service.return_car(car_id):
                print("Car returned and marked as Available.")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error returning car: {e}")

    def send_to_maintenance_ui(self):
        """Mark a car as under Maintenance."""
        try:
            car_id = safe_int_input("Enter Car ID to mark as under Maintenance: ")
            if self._car_service.send_to_maintenance(car_id):
                print("Car marked as under Maintenance.")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error sending car to maintenance: {e}")
