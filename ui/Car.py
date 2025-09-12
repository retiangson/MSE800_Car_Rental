from Domain.Models.Car import Car

def add_car_ui(car_service):
    try:
        make = input("Enter make: ")
        model = input("Enter model: ")
        year = int(input("Enter year: "))
        rate = float(input("Enter daily rate: "))
        new_car = Car(make=make, model=model, year=year, rate=rate)
        car_service.add_car(new_car)
        print("✅ Car added successfully.")
    except Exception as e:
        print(f"❌ Error adding car: {e}")

def list_cars_ui(car_service):
    print("\nAll Cars:")
    cars = car_service.list_cars()
    for car in cars:
        print(f"{car.id}: {car.make} {car.model} ({car.year}) - ${car.rate}/day")

def list_available_cars_ui(car_service):
    print("\nAvailable Cars:")
    cars = car_service.list_available_cars()
    for car in cars:
        print(f"{car.id}: {car.make} {car.model} - ${car.rate}/day")

def delete_car_ui(car_service):
    try:
        car_id = int(input("Enter Car ID to delete: "))
        if car_service.delete_car(car_id):
            print("🗑 Car soft deleted.")
        else:
            print("❌ Car not found.")
    except Exception as e:
        print(f"❌ Error deleting car: {e}")