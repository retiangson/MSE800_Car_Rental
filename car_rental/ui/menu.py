from datetime import date

# Import services/utils robustly for package or script mode
try:
    from car_rental.services import rental_service as svc
    from car_rental.services import auth_service as auth
    from car_rental.utils.validators import parse_date, parse_float, parse_int
    from car_rental.utils.formatting import row_to_car_str, row_to_customer_str, row_to_rental_str
except Exception:
    from services import rental_service as svc
    from services import auth_service as auth
    from utils.validators import parse_date, parse_float, parse_int
    from utils.formatting import row_to_car_str, row_to_customer_str, row_to_rental_str

current_user = None


def prompt(msg: str) -> str:
    return input(msg).strip()


def login_ui():
    global current_user
    print("=== Car Rental System Login ===")
    while True:
        u = prompt("Username: ")
        p = prompt("Password: ")
        user = auth.login(u, p)
        if user:
            current_user = user
            print(f"Welcome, {user['username']} ({user['role'].capitalize()})")
            return
        else:
            print("Invalid credentials, try again.")


# ---------------- Car Management ----------------
def add_car_ui():
    try:
        make = prompt("Make: ")
        model = prompt("Model: ")
        year = parse_int(prompt("Year (e.g., 2022): "))
        vtype = prompt("Type (e.g., sedan/suv/ev): ")
        rate = parse_float(prompt("Base rate per day (e.g., 55.0): "))
        cid = svc.add_car(make, model, year, vtype, rate)
        print(f"Car added with id={cid}.")
    except Exception as e:
        print(f"[Error] {e}")


def edit_car_ui():
    try:
        car_id = parse_int(prompt("Car ID to edit: "))
        make = prompt("New make (blank = keep): ")
        model = prompt("New model (blank = keep): ")
        year = prompt("New year (blank = keep): ")
        vtype = prompt("New type (blank = keep): ")
        rate = prompt("New base rate (blank = keep): ")

        year_val = int(year) if year else None
        rate_val = float(rate) if rate else None

        svc.update_car(car_id, make=make or None, model=model or None, year=year_val, vtype=vtype or None, base_rate=rate_val)
        print("Car updated.")
    except Exception as e:
        print(f"[Error] {e}")


def list_cars_ui():
    include_un = prompt("Include unavailable cars? (y/n): ").lower() != "n"
    rows = svc.list_cars(include_unavailable=include_un)
    if not rows:
        print("No cars found.")
        return
    print("\nCars:")
    for r in rows:
        print("  " + row_to_car_str(r))


def search_car_ui():
    kw = prompt("Search keyword (make/model/year/type): ")
    rows = svc.search_cars(kw)
    if not rows:
        print("No matching cars.")
        return
    print("\nCars:")
    for r in rows:
        print("  " + row_to_car_str(r))


# ---------------- Customer Management ----------------
def add_customer_ui():
    try:
        name = prompt("Full name: ")
        email = prompt("Email: ")
        phone = prompt("Phone: ")
        cid = svc.add_customer(name, email, phone)
        print(f"Customer added with id={cid}.")
    except Exception as e:
        print(f"[Error] {e}")


def list_customers_ui():
    rows = svc.list_customers()
    if not rows:
        print("No customers found.")
        return
    print("\nCustomers:")
    for r in rows:
        print("  " + row_to_customer_str(r))


def search_customer_ui():
    kw = prompt("Search keyword (name/email): ")
    rows = svc.repo.search_customers(kw)
    if not rows:
        print("No matching customers.")
        return
    print("\nCustomers:")
    for r in rows:
        print("  " + row_to_customer_str(r))


# ---------------- Employee Management ----------------
def add_employee_ui():
    try:
        u = prompt("New username: ")
        p = prompt("Password: ")
        role = prompt("Role (manager/employee, default employee): ") or "employee"
        uid = auth.add_employee(u, p, role)
        print(f"User created with id={uid}.")
    except Exception as e:
        print(f"[Error] {e}")


def list_employees_ui():
    rows = auth.list_users()
    if not rows:
        print("No employees/users found.")
        return
    print("\nEmployees/Users:")
    for r in rows:
        print(f"#{r[0]:<3} | {r[1]:<15} | {r[2]}")


def search_employee_ui():
    kw = prompt("Search keyword (username/role): ")
    rows = auth.search_users(kw)
    if not rows:
        print("No matching employees/users.")
        return
    print("\nEmployees/Users:")
    for r in rows:
        print(f"#{r[0]:<3} | {r[1]:<15} | {r[2]}")


# ---------------- Rentals ----------------
def rent_car_ui():
    try:
        car_id = parse_int(prompt("Car ID: "))
        email = prompt("Customer email: ")
        start = parse_date(prompt("Start date (YYYY-MM-DD): "))
        planned = prompt("Planned end date (YYYY-MM-DD, optional): ")
        planned_date = parse_date(planned) if planned else None
        rid = svc.rent_car(car_id, email, start, planned_date)
        print(f"Rental created with id={rid}.")
    except Exception as e:
        print(f"[Error] {e}")


def return_car_ui():
    try:
        car_id = parse_int(prompt("Car ID to return: "))
        ret = parse_date(prompt("Return date (YYYY-MM-DD): "))
        price = svc.return_car(car_id, ret)
        print(f"Car returned. Total price: ${price:.2f}")
    except Exception as e:
        print(f"[Error] {e}")


def list_rentals_ui():
    active_only = prompt("Active rentals only? (y/n): ").lower() == "y"
    rows = svc.list_rentals(active_only=active_only)
    if not rows:
        print("No rentals found.")
        return
    print("\nRentals:")
    for r in rows:
        print("  " + row_to_rental_str(r))


def search_rentals_ui():
    car = prompt("Car ID (blank=any): ")
    cust = prompt("Customer ID (blank=any): ")
    status = prompt("Status (active/returned/all): ").lower() or "all"
    car_id = int(car) if car else None
    cust_id = int(cust) if cust else None
    if status == "active":
        active_only = True
    elif status == "returned":
        active_only = False
    else:
        active_only = None
    rows = svc.repo.search_rentals(car_id=car_id, customer_id=cust_id, active_only=active_only)
    if not rows:
        print("No matching rentals.")
        return
    print("\nRentals:")
    for r in rows:
        print("  " + row_to_rental_str(r))


# ---------------- Menu ----------------
def show_menu():
    print("\n=== Main Menu ===")
    if current_user["role"] == "manager":
        print("1) Add car")
        print("2) List cars")
        print("3) Search car")
        print("4) Edit car")
        print("5) Add customer")
        print("6) List customers")
        print("7) Search customer")
        print("8) Add employee")
        print("9) List employees")
        print("10) Search employee")
        print("11) Rent a car")
        print("12) Return a car")
        print("13) List rentals")
        print("14) Search rentals")
        print("0) Exit")
    else:
        print("1) List cars")
        print("2) Search car")
        print("3) Add customer")
        print("4) List customers")
        print("5) Search customer")
        print("6) Rent a car")
        print("7) Return a car")
        print("8) List rentals")
        print("9) Search rentals")
        print("0) Exit")


def run():
    login_ui()
    while True:
        show_menu()
        choice = input("Select: ").strip()
        if current_user["role"] == "manager":
            if choice == "1":
                add_car_ui()
            elif choice == "2":
                list_cars_ui()
            elif choice == "3":
                search_car_ui()
            elif choice == "4":
                edit_car_ui()
            elif choice == "5":
                add_customer_ui()
            elif choice == "6":
                list_customers_ui()
            elif choice == "7":
                search_customer_ui()
            elif choice == "8":
                add_employee_ui()
            elif choice == "9":
                list_employees_ui()
            elif choice == "10":
                search_employee_ui()
            elif choice == "11":
                rent_car_ui()
            elif choice == "12":
                return_car_ui()
            elif choice == "13":
                list_rentals_ui()
            elif choice == "14":
                search_rentals_ui()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        else:  # employee
            if choice == "1":
                list_cars_ui()
            elif choice == "2":
                search_car_ui()
            elif choice == "3":
                add_customer_ui()
            elif choice == "4":
                list_customers_ui()
            elif choice == "5":
                search_customer_ui()
            elif choice == "6":
                rent_car_ui()
            elif choice == "7":
                return_car_ui()
            elif choice == "8":
                list_rentals_ui()
            elif choice == "9":
                search_rentals_ui()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
