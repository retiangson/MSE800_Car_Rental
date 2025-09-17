import uvicorn

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

import uvicorn   # make sure this import is at the top of MainMenu.py

def run_api_server():
    print("\n🚀 Starting API server at http://127.0.0.1:8000 ...")
    uvicorn.run(
        "api.main_api:app",   # path to your FastAPI app instance
        host="127.0.0.1",
        port=8000,
        reload=False          # disable reload in packaged exe
    )

def car_menu(car_ui):
    while True:
        print("\n--- Car Management ---")
        print("1. Add Car")
        print("2. List All Cars")
        print("3. List Available Cars")
        print("4. Update Car")
        print("5. Delete Car")
        print("6. Restore Car")
        print("7. Rent Car")
        print("8. Return Car")
        print("9. Send Car to Maintenance")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            car_ui.add_car_ui()
        elif choice == "2":
            car_ui.list_cars_ui()
        elif choice == "3":
            car_ui.list_available_cars_ui()
        elif choice == "4":
            car_ui.update_car_ui()
        elif choice == "5":
            car_ui.delete_car_ui()
        elif choice == "6":
            car_ui.restore_car_ui()
        elif choice == "7":
            car_ui.rent_car_ui()
        elif choice == "8":
            car_ui.return_car_ui()
        elif choice == "9":
            car_ui.send_to_maintenance_ui()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def rental_menu(rental_ui):
    while True:
        print("\n--- Rental Management ---")
        print("1. Create Rental")
        print("2. List All Rentals")
        print("3. List Active Rentals")
        print("4. Approve & Start Rental")
        print("5. Reject Rental")
        print("6. Complete Rental")
        print("7. Cancel Rental")
        print("8. Delete Rental (soft)")
        print("0. Back to Main Menu")

        choice = input("Choose an option: ")

        if choice == "1":
            rental_ui.create_rental_ui()
        elif choice == "2":
            rental_ui.list_rentals_ui(include_deleted=True)
        elif choice == "3":
            rental_ui.list_active_rentals_ui()
        elif choice == "4":
            rental_ui.approve_rental_ui()
        elif choice == "5":
            rental_ui.reject_rental_ui()
        elif choice == "6":
            rental_ui.complete_rental_ui()
        elif choice == "7":
            rental_ui.cancel_rental_ui()
        elif choice == "8":
            rental_ui.delete_rental_ui()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def user_menu(user_ui):
    while True:
        print("\n-- User Management --")
        print("1. Register User")
        print("2. List Users")
        print("3. Update User")
        print("4. Delete User")
        print("0. Back to Admin Menu")

        sub_choice = input("Enter choice: ")
        if sub_choice == "1":
            user_ui.register_user_ui()
        elif sub_choice == "2":
            user_ui.list_users_ui()
        elif sub_choice == "3":
            user_ui.update_user_ui()
        elif sub_choice == "4":
            user_ui.delete_user_ui()
        elif sub_choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def admin_menu(car_ui, rental_ui, user_ui):
    while True:
        print("\n=== Admin Menu ===")
        print("1. Manage Cars")
        print("2. Manage Rentals")
        print("3. Manage Users")
        print("4. Start API Server")
        print("0. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            car_menu(car_ui)
        elif choice == "2":
            rental_menu(rental_ui)
        elif choice == "3":
            user_menu(user_ui)
        elif choice == "4":
            run_api_server()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def customer_menu(car_ui, rental_ui, current_user):
    while True:
        print("\n=== Customer Menu ===")
        print("1. List Available Cars")
        print("2. Create Rental Request")
        print("3. View Active Rentals")
        print("4. View Rental History")
        print("0. Logout")

        choice = input("Enter choice: ")
        if choice == "1":
            car_ui.list_available_cars_ui()
        elif choice == "2":
            rental_ui.create_rental_ui(current_user=current_user) 
        elif choice == "3":
            rental_ui.list_active_rentals_ui()
        elif choice == "4":
            rental_ui.list_customer_rentals_ui(current_user, include_deleted=False)
        elif choice == "0":
            break
        else:
            print("Invalid choice.")


def run(installer):
    car_ui = installer.car_ui
    user_ui = installer.user_ui
    customer_ui = installer.customer_ui
    rental_ui = installer.rental_ui
    login_ui = installer.login_ui

    print_header()
    while True:
        print("\n=== Main Menu ===")
        print("1. Login")
        print("2. Register (Customer)")
        print("0. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            user = login_ui.login_ui()
            if user:
                if user.role == "admin":
                    admin_menu(car_ui, rental_ui, user_ui)
                elif user.role == "customer":
                    customer_menu(car_ui, rental_ui, user) 
        elif choice == "2":
            customer_ui.customer_register_ui()
        elif choice == "0":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice.")
