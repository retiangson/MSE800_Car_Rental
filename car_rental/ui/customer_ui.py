import ui.login_ui as login

from ui.login_ui import prompt
from services import customer_service as svc
from utils.validators import parse_int
from utils.formatting import row_to_customer_str

def customer_add_ui():
    try:
        name = prompt("Full name: ")
        email = prompt("Email: ")
        phone = prompt("Phone: ")
        cid = svc.add_customer(name, email, phone)
        print(f"Customer added with id={cid}.")
    except Exception as e:
        print(f"[Error] {e}")

def customer_list_ui(include_deleted=False):
    try:
        rows = svc.list_customers(include_deleted=include_deleted)
        if not rows:
            print("No customers found.")
            return
        print("\nCustomers:")
        for r in rows:
            print("  " + row_to_customer_str(r))
    except Exception as e:
        print(f"[Error] {e}")

def customer_search_ui(include_deleted=False):
    try:
        kw = prompt("Search keyword (name/email): ")
        rows = svc.search_customers(kw, include_deleted=include_deleted)
        if not rows:
            print("No matching customers.")
            return
        print("\nCustomers:")
        for r in rows:
            print("  " + row_to_customer_str(r))
    except Exception as e:
        print(f"[Error] {e}")

def customer_remove_ui():
    try:
        if not login.current_user:
            raise ValueError("You must be logged in to remove a customer.")

        cid = parse_int(login.prompt("Customer ID to remove (soft delete): "))
        svc.remove_customer(cid, login.current_user["id"])
        print("Customer removed (soft delete).")
    except Exception as e:
        print(f"[Error] {e}")

def customer_view_deleted_ui():
    rows = svc.list_customers(include_deleted=True)
    if not rows: 
        print("No customers (including deleted).")
        return
    print("\nCustomers (incl. deleted):")
    for r in rows: print("  " + row_to_customer_str(r))

def customer_restore_ui():
    try:
        if not login.current_user:
            raise ValueError("You must be logged in to restore a customer.")

        cid = parse_int(login.prompt("Customer ID to restore: "))
        svc.restore_customer(cid, login.current_user["id"])
        print("Customer restored.")
    except Exception as e:
        print(f"[Error] {e}")

def customer_menu():
    while True:
        print("\n=== Customer Management ===")
        print("1) Add Customer")
        print("2) List Customers")
        print("3) Search Customer")
        print("4) Remove Customer (soft delete)")
        print("5) View Deleted Customers")
        print("6) Restore Customer")
        print("0) Back")
        ch = prompt("Select: ")
        if ch == "1": customer_add_ui()
        elif ch == "2": customer_list_ui()
        elif ch == "3": customer_search_ui()
        elif ch == "4": customer_remove_ui()
        elif ch == "5": customer_view_deleted_ui()
        elif ch == "6": customer_restore_ui()
        elif ch == "0": break
        else: print("Invalid choice.")
