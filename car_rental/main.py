
try:
    from car_rental.storage.db import init_db, init_users
    from car_rental.ui.menu import run
except Exception:
    from storage.db import init_db, init_users
    from ui.menu import run

def main():
    init_db()
    init_users()
    run()

if __name__=="__main__":
    main()
