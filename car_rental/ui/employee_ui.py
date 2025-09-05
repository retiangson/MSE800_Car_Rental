import ui.login_ui as login

from ui.login_ui import prompt
from services import users_service as auth
from utils.validators import parse_int

def employee_add_ui():
    try:
        u = prompt("New username: ")
        p = prompt("Password: ")
        role = prompt("Role (manager/employee, default employee): ") or "employee"
        uid = auth.add_employee(u, p, role)
        print(f"User created with id={uid}.")
    except Exception as e:
        print(f"[Error] {e}")

def employee_list_ui(include_deleted=False):
    rows = auth.list_users(include_deleted=include_deleted)
    if not rows: 
        print("No employees/users found.")
        return
    print("\nEmployees/Users:")
    for r in rows: print(f"#{r[0]:<3} | {r[1]:<15} | {r[2]}")

def employee_search_ui(include_deleted=False):
    kw = prompt("Search keyword (username/role): ")
    rows = auth.search_users(kw, include_deleted=include_deleted)
    if not rows: 
        print("No matching employees/users.")
        return
    print("\nEmployees/Users:")
    for r in rows: print(f"#{r[0]:<3} | {r[1]:<15} | {r[2]}")

def employee_remove_ui():
    try:
        uid = parse_int(prompt("User ID to remove (soft delete): "))
        auth.remove_user(uid, login.current_user["id"])
        print("User removed (soft delete).")
    except Exception as e:
        print(f"[Error] {e}")

def employee_restore_ui():
    try:
        uid = parse_int(prompt("User ID to restore: "))
        auth.restore_user(uid, login.current_user["id"])
        print("User restored.")
    except Exception as e:
        print(f"[Error] {e}")

def employee_menu():
    while True:
        print("\n=== Employee Management ===")
        print("1) Add Employee")
        print("2) List Employees")
        print("3) Search Employee")
        print("4) Remove Employee (soft delete)")
        print("5) View Deleted Employees")
        print("6) Restore Employee")
        print("0) Back")
        ch = prompt("Select: ")
        if ch == "1": employee_add_ui()
        elif ch == "2": employee_list_ui()
        elif ch == "3": employee_search_ui()
        elif ch == "4": employee_remove_ui()
        elif ch == "5": employee_list_ui(include_deleted=True)
        elif ch == "6": employee_restore_ui()
        elif ch == "0": break
        else: print("Invalid choice.")
