from Domain.Interfaces.IRentalRepository import IRentalRepository
from Domain.Repositories.DBManager import DBManager
from Domain.Models.Rental import Rental

class RentalRepository(IRentalRepository):
    def __init__(self):
        self._init_table()

    def _init_table(self):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    car_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    status TEXT DEFAULT 'Pending'
                )
            """)
            conn.commit()

    def add(self, rental: Rental):
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO rentals (customer_id, car_id, start_date, end_date, status)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    rental.customer_id,
                    rental.car_id,
                    rental.start_date,
                    rental.end_date,
                    rental.status or "Pending"
                )
            )
            conn.commit()
            rental.id = cursor.lastrowid
            return rental

    def get_all(self, include_deleted=False):
        with DBManager() as conn:
            cursor = conn.cursor()
            if include_deleted:
                cursor.execute("SELECT id, customer_id, car_id, start_date, end_date, status FROM rentals")
            else:
                cursor.execute("SELECT id, customer_id, car_id, start_date, end_date, status FROM rentals WHERE status != 'Deleted'")
            rows = cursor.fetchall()
            return [Rental(*row) for row in rows]

    def find_by_id(self, rental_id, include_deleted=False):
        with DBManager() as conn:
            cursor = conn.cursor()
            if include_deleted:
                cursor.execute("SELECT id, customer_id, car_id, start_date, end_date, status FROM rentals WHERE id = ?", (rental_id,))
            else:
                cursor.execute("SELECT id, customer_id, car_id, start_date, end_date, status FROM rentals WHERE id = ? AND status != 'Deleted'", (rental_id,))
            row = cursor.fetchone()
            return Rental(*row) if row else None

    def delete(self, rental_id):
        """Soft delete rental by setting status to Deleted"""
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE rentals SET status = 'Deleted' WHERE id = ?", (rental_id,))
            conn.commit()
            return cursor.rowcount > 0
        
    def update_status(self, rental_id, status):
        """Update rental workflow status (Pending, Approved, Active, Completed, Cancelled, Deleted)"""
        with DBManager() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE rentals SET status = ? WHERE id = ?", (status, rental_id))
            conn.commit()
            return cursor.rowcount > 0
