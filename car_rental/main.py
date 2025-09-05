try:
    from car_rental.repository.db import init_db, init_users
    from car_rental.ui.main_menu import run
except Exception:
    from repository.db import init_db, init_users
    from ui.main_menu import run


def main():
    init_db()
    init_users()
    run()


if __name__ == "__main__":
    main()