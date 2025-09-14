from Contracts.CarDto import CarDto

class CarUI:
    def __init__(self, car_service):
        self._car_service = car_service  

    def add_car_ui(self):
        try:
            make = input("Enter make: ")
            model = input("Enter model: ")
            year = int(input("Enter year: "))
            vtype = input("Enter type (e.g., sedan/suv/ev): ")
            base_rate = float(input("Enter daily base rate: "))
            
            new_car_dto = CarDto(
                id=None,
                make=make,
                model=model,
                year=year,
                vtype=vtype,
                base_rate=base_rate,
                status=None
            )

            saved_car = self._car_service.add_car(new_car_dto)
            print(f"Car added successfully: {saved_car.make} {saved_car.model} "
                  f"({saved_car.year}) - ${saved_car.base_rate}/day, status={saved_car.status}.")
        except Exception as e:
            print(f"Error adding car: {e}")

    def update_car_ui(self):
        try:
            car_id = int(input("Enter Car ID to update: "))
            existing = self._car_service.get_by_id(car_id)
            if not existing:
                print("Car not found.")
                return

            print(f"Leave blank to keep current value.")

            make = input(f"Enter new make [{existing.make}]: ") or existing.make
            model = input(f"Enter new model [{existing.model}]: ") or existing.model
            year_input = input(f"Enter new year [{existing.year}]: ")
            year = int(year_input) if year_input.strip() else existing.year
            vtype = input(f"Enter new type [{existing.vtype}]: ") or existing.vtype
            base_rate_input = input(f"Enter new base rate [{existing.base_rate}]: ")
            base_rate = float(base_rate_input) if base_rate_input.strip() else existing.base_rate
            status = input(f"Enter new status [{existing.status}]: ") or existing.status

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
        print("\nAll Cars:")
        cars = self._car_service.list_cars(include_deleted=True)
        for car in cars:
            print(f"{car.id}: {car.make} {car.model} ({car.year}) - "
                  f"${car.base_rate}/day - Status: {car.status}")

    def list_available_cars_ui(self):
        print("\nAvailable Cars:")
        cars = self._car_service.list_available_cars()
        for car in cars:
            print(f"{car.id}: {car.make} {car.model} ({car.year}) - "
                  f"${car.base_rate}/day - Status: {car.status}")

    def delete_car_ui(self):
        try:
            car_id = int(input("Enter Car ID to mark as Deleted: "))
            if self._car_service.delete_car(car_id):
                print("🗑 Car marked as Deleted.")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error deleting car: {e}")

    def restore_car_ui(self):
        try:
            car_id = int(input("Enter Car ID to restore (make Available): "))
            if self._car_service.restore_car(car_id):
                print("Car restored and set to Available.")
            else:
                print("Car not found or not in Deleted status.")
        except Exception as e:
            print(f"Error restoring car: {e}")

    def rent_car_ui(self):
        try:
            car_id = int(input("Enter Car ID to mark as Active (rented): "))
            if self._car_service.rent_car(car_id):
                print("Car marked as Active (rented).")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error renting car: {e}")

    def return_car_ui(self):
        try:
            car_id = int(input("Enter Car ID to mark as Available (returned): "))
            if self._car_service.return_car(car_id):
                print("Car returned and marked as Available.")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error returning car: {e}")

    def send_to_maintenance_ui(self):
        try:
            car_id = int(input("Enter Car ID to mark as under Maintenance: "))
            if self._car_service.send_to_maintenance(car_id):
                print("🛠 Car marked as under Maintenance.")
            else:
                print("Car not found.")
        except Exception as e:
            print(f"Error sending car to maintenance: {e}")