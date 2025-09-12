from Domain.Models.User import User

def register_user_ui(user_service):
    try:
        print("\n=== Register New User ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            print("Passwords do not match!")
            return

        role = input("Enter role (admin/customer): ")
        name = input("Full name: ")
        contact_number = input("Contact number: ")
        email = input("Email: ")
        address = input("Address: ")

        new_user = User(username=username, password=password, role=role,
                        name=name, contact_number=contact_number,
                        email=email, address=address)

        user_service.register_user(new_user)
        print("User registered successfully.")
    except Exception as e:
        print(f"Error registering user: {e}")

def list_users_ui(user_service):
    print("\nAll Users:")
    users = user_service.list_users()
    for u in users:
        print(f"ID {u.id}: {u.username} ({u.role}) - {u.name}, {u.email}")

def delete_user_ui(user_service):
    try:
        user_id = int(input("Enter User ID to delete: "))
        if user_service.delete(user_id):
            print("🗑 User soft deleted.")
        else:
            print("User not found.")
    except Exception as e:
        print(f"Error deleting user: {e}")
