from Domain.Models.User import User

def customer_register_ui(user_service):
    try:
        print("\n=== Customer Registration ===")
        username = input("Choose username: ")
        password = input("Choose password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            print("❌ Passwords do not match!")
            return

        name = input("Full name: ")
        contact_number = input("Contact number: ")
        email = input("Email: ")
        address = input("Address: ")

        new_user = User(username=username, password=password, role="customer",
                        name=name, contact_number=contact_number,
                        email=email, address=address)

        user_service.register_user(new_user)
        print("✅ Customer registered successfully.")
    except Exception as e:
        print(f"❌ Error registering customer: {e}")
