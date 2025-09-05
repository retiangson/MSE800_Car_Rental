
from services import users_service as auth
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
            return current_user
        else:
            print("Invalid credentials, try again.")