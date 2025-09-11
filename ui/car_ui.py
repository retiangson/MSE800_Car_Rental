import ui.login_ui as login

from ui.login_ui import prompt
from services import car_service as svc
from utils.validators import parse_int, parse_float
from utils.formatting import row_to_car_str

def car_add_ui():
    try:
        if not login.current_user:
            raise ValueError("You must be logged in to add a car.")
        
        make = prompt("Make: ")
        model = prompt("Model: ")
        year = parse_int(prompt("Year (e.g., 2022): "))
        vtype = prompt("Type (e.g., sedan/suv/ev): ")
        rate = parse_float(prompt("Base rate per day: "))
        cid = svc.add_car(make, model, year, vtype, rate, login.current_user["id"])
        print(f"Car added with id={cid}.")
    except Exception as e:
        print(f"[Error] {e}")

def car_list_ui(include_deleted=False):
    rows = svc.list_cars(include_unavailable=True, include_deleted=include_deleted)
    if not rows: print("No cars found."); return
    print("\nCars:")
    for r in rows: print("  " + row_to_car_str(r))

def car_search_ui(include_deleted=False):
    kw = prompt("Search keyword: ")
    rows = svc.search_cars(kw, include_deleted=include_deleted)
    if not rows: print("No matching cars."); return
    print("\nCars:")
    for r in rows: print("  " + row_to_car_str(r))

def car_edit_ui():
    try:
        car_id = parse_int(prompt("Car ID to edit: "))
        make = prompt("New make (blank=keep): ")
        model = prompt("New model (blank=keep): ")
        year = prompt("New year (blank=keep): ")
        vtype = prompt("New type (blank=keep): ")
        rate = prompt("New base rate (blank=keep): ")
        svc.update_car(
            car_id,
            make=make or None, model=model or None,
            year=int(year) if year else None,
            vtype=vtype or None,
            base_rate=float(rate) if rate else None,
            user_id=login.current_user["id"]
        )
        print("Car updated.")
    except Exception as e:
        print(f"[Error] {e}")

def car_remove_ui():
    try:
        car_id = parse_int(prompt("Car ID to remove (soft delete): "))
        svc.remove_car(car_id, login.current_user["id"])
        print("Car removed (soft delete).")
    except Exception as e:
        print(f"[Error] {e}")

def car_view_deleted_ui():
    rows = svc.list_deleted_cars()
    if not rows: print("No deleted cars."); return
    print("\nDeleted Cars:")
    for r in rows: print("  " + row_to_car_str(r))

def car_restore_ui():
    try:
        car_id = parse_int(prompt("Car ID to restore: "))
        svc.restore_car(car_id, login.current_user["id"])
        print("Car restored.")
    except Exception as e:
        print(f"[Error] {e}")

def car_menu():
    while True:
        print("\n=== Car Management ===")
        print("1) Add Car")
        print("2) List Cars")
        print("3) Search Car")
        print("4) Edit Car")
        print("5) Remove Car (soft delete)")
        print("6) View Deleted Cars")
        print("7) Restore Car")
        print("0) Back")
        ch = prompt("Select: ")
        if ch == "1": car_add_ui()
        elif ch == "2": car_list_ui()
        elif ch == "3": car_search_ui()
        elif ch == "4": car_edit_ui()
        elif ch == "5": car_remove_ui()
        elif ch == "6": car_view_deleted_ui()
        elif ch == "7": car_restore_ui()
        elif ch == "0": break
        else: print("Invalid choice.")
