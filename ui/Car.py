from Domain.Models.Car import Car

def add_car_ui(car_service):
    try:
        make = input("Enter make: ")
        model = input("Enter model: ")
        year = int(input("Enter year: "))
        rate = float(input("Enter daily rate: "))
        new_car = Car(make=make, model=model, year=year, rate=rate)
        car_service.add_car(new_car)
        print("Car added successfully (status = Available).")
    except Exception as e:
        print(f"Error adding car: {e}")


def list_cars_ui(car_service):
    print("\nAll Cars:")
    cars = car_service.list_cars(include_deleted=True)
    for car in cars:
        print(f"{car.id}: {car.make} {car.model} ({car.year}) - "
              f"${car.rate}/day - Status: {car.status}")


def list_available_cars_ui(car_service):
    print("\nAvailable Cars:")
    cars = car_service.list_available_cars()
    for car in cars:
        print(f"{car.id}: {car.make} {car.model} ({car.year}) - "
              f"${car.rate}/day - Status: {car.status}")


def delete_car_ui(car_service):
    try:
        car_id = int(input("Enter Car ID to mark as Deleted: "))
        if car_service.delete_car(car_id):
            print("🗑 Car marked as Deleted.")
        else:
            print("Car not found.")
    except Exception as e:
        print(f"Error deleting car: {e}")


def restore_car_ui(car_service):
    try:
        car_id = int(input("Enter Car ID to restore (make Available): "))
        if car_service.restore_car(car_id):
            print("Car restored and set to Available.")
        else:
            print("Car not found or not in Deleted status.")
    except Exception as e:
        print(f"Error restoring car: {e}")
