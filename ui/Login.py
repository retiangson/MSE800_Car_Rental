def login_ui(user_service):
    username = input("Username: ")
    password = input("Password: ")

    user = user_service.login_user(username, password)
    if user:
        print(f"✅ Welcome, {user.username}! Role: {user.role}")
        return user   # return the User object
    else:
        print("❌ Invalid login.")
        return None
