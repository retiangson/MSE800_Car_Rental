import ui.login_ui as login

from ui.login_ui import prompt
from services import rental_service as svc
from utils.validators import parse_int, parse_date
from utils.formatting import row_to_rental_str

def rent_car_ui():
    try:
        car_id = parse_int(prompt("Car ID: "))
        email = prompt("Customer email: ")
        start = parse_date(prompt("Start date (YYYY-MM-DD): "))
        planned = prompt("Planned end date (YYYY-MM-DD, optional): ")
        planned_date = parse_date(planned) if planned else None
        rid = svc.rent_car(car_id, email, start, planned_date, login.current_user["id"])
        print(f"Rental created with id={rid}.")
    except Exception as e:
        print(f"[Error] {e}")

def return_car_ui():
    try:
        car_id = parse_int(prompt("Car ID to return: "))
        ret = parse_date(prompt("Return date (YYYY-MM-DD): "))
        price = svc.return_car(car_id, ret, login.current_user["id"])
        print(f"Car returned. Total price: ${price:.2f}")
    except Exception as e:
        print(f"[Error] {e}")

def rental_list_ui(include_deleted=False):
    active_only = prompt("Active rentals only? (y/n): ").lower() == "y"
    rows = svc.list_rentals(active_only=active_only, include_deleted=include_deleted)
    if not rows: 
        print("No rentals found.")
        return
    print("\nRentals:")
    for r in rows: print("  " + row_to_rental_str(r))

def rental_search_ui(include_deleted=False):
    car = prompt("Car ID (blank=any): ")
    cust = prompt("Customer ID (blank=any): ")
    status = prompt("Status (active/returned/all): ").lower() or "all"
    car_id = int(car) if car else None
    cust_id = int(cust) if cust else None
    if status == "active": active_only = True
    elif status == "returned": active_only = False
    else: active_only = None
    rows = svc.search_rentals(
        car_id=car_id, customer_id=cust_id,
        active_only=active_only, include_deleted=include_deleted
    )
    if not rows: 
        print("No matching rentals.")
        return
    print("\nRentals:")
    for r in rows: print("  " + row_to_rental_str(r))

def rental_menu():
    while True:
        print("\n=== Rental Management ===")
        print("1) Rent a Car")
        print("2) Return a Car")
        print("3) List Rentals")
        print("4) Search Rentals")
        print("0) Back")
        ch = prompt("Select: ")
        if ch == "1": rent_car_ui()
        elif ch == "2": return_car_ui()
        elif ch == "3": rental_list_ui()
        elif ch == "4": rental_search_ui()
        elif ch == "0": break
        else: print("Invalid choice.")
