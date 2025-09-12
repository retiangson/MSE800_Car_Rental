from Domain.Interfaces.ICarRepository import ICarRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.Car import Car

class CarRepository(ICarRepository):
    def __init__(self):
        self._init_table()

    def _init_table(self):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    make TEXT,
                    model TEXT,
                    year INTEGER,
                    rate REAL,
                    status TEXT DEFAULT 'Available'
                )
            """)
            conn.commit()

    def add(self, car: Car):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cars (make, model, year, rate, status) VALUES (?, ?, ?, ?, ?)",
                (car.make, car.model, car.year, car.rate, car.status)
            )
            conn.commit()
            car.id = cursor.lastrowid
            return car

    def get_all(self, include_deleted=False):
        with DBManager() as conn:
            cursor = conn.cursor()
            if include_deleted:
                cursor.execute("SELECT id, make, model, year, rate, status FROM cars")
            else:
                cursor.execute("SELECT id, make, model, year, rate, status FROM cars WHERE status != 'Deleted'")
            rows = cursor.fetchall()
            return [Car(*row) for row in rows]

    def find_by_id(self, car_id):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, make, model, year, rate, status FROM cars WHERE id = ?", (car_id,))
            row = cursor.fetchone()
            return Car(*row) if row else None

    def update_status(self, car_id, status):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE cars SET status = ? WHERE id = ?", (status, car_id))
            conn.commit()
            return cursor.rowcount > 0