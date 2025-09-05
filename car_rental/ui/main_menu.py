from ui.login_ui import login_ui, current_user, prompt
from ui.car_ui import car_menu
from ui.customer_ui import customer_menu
from ui.employee_ui import employee_menu
from ui.rental_ui import rental_menu

def manager_menu():
    while True:
        print("\n=== Main Menu (Manager) ===")
        print("1) Car Management")
        print("2) Customer Management")
        print("3) Employee Management")
        print("4) Rental Management")
        print("0) Exit")
        ch = prompt("Select: ")
        if ch == "1": car_menu()
        elif ch == "2": customer_menu()
        elif ch == "3": employee_menu()
        elif ch == "4": rental_menu()
        elif ch == "0": print("Goodbye!"); break

def employee_main_menu():
    while True:
        print("\n=== Main Menu (Employee) ===")
        print("1) Car Management")
        print("2) Customer Management")
        print("3) Rental Management")
        print("0) Exit")
        ch = prompt("Select: ")
        if ch == "1": car_menu()
        elif ch == "2": customer_menu()
        elif ch == "3": rental_menu()
        elif ch == "0": print("Goodbye!"); break

def run():
    user = login_ui()
    if user["role"] == "manager":
        manager_menu()
    else:
        employee_main_menu()
