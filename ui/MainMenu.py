from ui.Login import login_ui
from ui.Customer import customer_register_ui
from ui.Employee import register_user_ui, list_users_ui, delete_user_ui
from ui.Car import (
    add_car_ui, list_cars_ui, list_available_cars_ui,
    delete_car_ui, restore_car_ui
)
from ui.Rental import (
    create_rental_ui, list_rentals_ui, list_active_rentals_ui,
    approve_and_start_rental_ui, reject_rental_ui,
    cancel_rental_ui, return_rental_ui
)

def print_header():
    header = r"""
 ____             _       _   _       _    __        ___               _     
|  _ \ ___  _ __ ( )___  | | | | ___ | |_  \ \      / / |__   ___  ___| |___ 
| |_) / _ \| '_ \|// __| | |_| |/ _ \| __|  \ \ /\ / /| '_ \ / _ \/ _ \ / __|
|  _ < (_) | | | | \__ \ |  _  | (_) | |_    \ V  V / | | | |  __/  __/ \__ \
|_| \_\___/|_| |_| |___/ |_| |_|\___/ \__|    \_/\_/  |_| |_|\___|\___|_|___/
                                                    
                             CAR RENTAL SYSTEM
    """
    print(header)

def car_menu(car_service):
    """Dedicated Car Management Sub-Menu"""
    while True:
        print("\n-- Car Management --")
        print("1. Add Car")
        print("2. List All Cars")
        print("3. List Available Cars")
        print("4. Delete Car (mark as Deleted)")
        print("5. Restore Car (set Available)")
        print("0. Back to Admin Menu")

        sub_choice = input("Enter choice: ")
        if sub_choice == "1":
            add_car_ui(car_service)
        elif sub_choice == "2":
            list_cars_ui(car_service)
        elif sub_choice == "3":
            list_available_cars_ui(car_service)
        elif sub_choice == "4":
            delete_car_ui(car_service)
        elif sub_choice == "5":
            restore_car_ui(car_service)
        elif sub_choice == "0":
            print("Returning to Admin Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def rental_menu(rental_service):
    """Dedicated Rental Management Sub-Menu"""
    while True:
        print("\n-- Rental Management --")
        print("1. List Rentals")
        print("2. List Active Rentals")
        print("3. Approve & Start Rental")
        print("4. Reject Rental")
        print("5. Return Rental (enter actual return date, recalc cost, print receipt)")
        print("6. Cancel Rental")
        print("0. Back to Admin Menu")

        sub_choice = input("Enter choice: ")
        if sub_choice == "1":
            list_rentals_ui(rental_service)
        elif sub_choice == "2":
            list_active_rentals_ui(rental_service)
        elif sub_choice == "3":
            approve_and_start_rental_ui(rental_service)
        elif sub_choice == "4":
            reject_rental_ui(rental_service)
        elif sub_choice == "5":
            return_rental_ui(rental_service)
        elif sub_choice == "6":
            cancel_rental_ui(rental_service)
        elif sub_choice == "0":
            print("Returning to Admin Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def user_menu(user_service):
    """Dedicated User Management Sub-Menu"""
    while True:
        print("\n-- User Management --")
        print("1. Register User")
        print("2. List Users")
        print("3. Delete User (mark as Deleted)")
        print("0. Back to Admin Menu")

        sub_choice = input("Enter choice: ")
        if sub_choice == "1":
            register_user_ui(user_service)
        elif sub_choice == "2":
            list_users_ui(user_service)
        elif sub_choice == "3":
            delete_user_ui(user_service)
        elif sub_choice == "0":
            print("Returning to Admin Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def admin_menu(car_service, rental_service, user_service):
    while True:
        print("\n=== Admin Menu ===")
        print("1. Manage Cars")
        print("2. Manage Rentals")
        print("3. Manage Users")
        print("0. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            car_menu(car_service)
        elif choice == "2":
            rental_menu(rental_service)
        elif choice == "3":
            user_menu(user_service)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def customer_menu(car_service, rental_service, user_service, user):
    while True:
        print("\n=== Customer Menu ===")
        print("1. List Available Cars")
        print("2. Create Rental Request")
        # Optional: add rental history and return feature
        # print("3. View My Rentals")
        # print("4. Return My Rental")
        print("0. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            list_available_cars_ui(car_service)
        elif choice == "2":
            create_rental_ui(rental_service, user)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def run(car_service, user_service, rental_service):
    print_header()
    while True:
        print("\n=== Main Menu ===")
        print("1. Login")
        print("2. Register (Customer)")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            user = login_ui(user_service)
            if user:
                if user.role == "admin":
                    admin_menu(car_service, rental_service, user_service)
                elif user.role == "customer":
                    customer_menu(car_service, rental_service, user_service, user)
        elif choice == "2":
            customer_register_ui(user_service)
        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice.")
