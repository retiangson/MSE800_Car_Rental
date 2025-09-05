from typing import Optional, List, Tuple
from datetime import date
from .db import get_connection

def create_rental(car_id, customer_id, start_date: date, planned_end_date: date, user_id) -> int:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""INSERT INTO rentals(car_id, customer_id, start_date, planned_end_date, created_by)
                   VALUES (?,?,?,?,?);""",
                (car_id, customer_id, start_date.isoformat(), planned_end_date.isoformat() if planned_end_date else None, user_id))
    conn.commit(); rid = cur.lastrowid; conn.close(); return rid

def return_rental(rental_id, returned_date: date, total_price: float, user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""UPDATE rentals SET returned_date=?, total_price=?, date_updated=CURRENT_TIMESTAMP, updated_by=?
                   WHERE id=?;""",
                (returned_date.isoformat(), total_price, user_id, rental_id))
    conn.commit(); conn.close()

def get_active_rental_by_car(car_id) -> Optional[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT id, car_id, customer_id, start_date, planned_end_date
                   FROM rentals WHERE car_id=? AND returned_date IS NULL AND isDeleted=0;""", (car_id,))
    row = cur.fetchone(); conn.close(); return row

def list_rentals(active_only=False, include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    q = """SELECT id, car_id, customer_id, start_date, planned_end_date, returned_date, total_price
           FROM rentals WHERE 1=1"""
    if not include_deleted: q += " AND isDeleted=0"
    if active_only: q += " AND returned_date IS NULL"
    q += " ORDER BY id;"
    cur.execute(q)
    rows = cur.fetchall(); conn.close(); return rows

def search_rentals(car_id=None, customer_id=None, active_only=None, include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    q = """SELECT id, car_id, customer_id, start_date, planned_end_date, returned_date, total_price
           FROM rentals WHERE 1=1"""
    params = []
    if not include_deleted: q += " AND isDeleted=0"
    if car_id: q += " AND car_id=?"; params.append(car_id)
    if customer_id: q += " AND customer_id=?"; params.append(customer_id)
    if active_only is True: q += " AND returned_date IS NULL"
    elif active_only is False: q += " AND returned_date IS NOT NULL"
    q += " ORDER BY id;"
    cur.execute(q, tuple(params))
    rows = cur.fetchall(); conn.close(); return rows

def remove_rental(rental_id, user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE rentals SET isDeleted=1, date_updated=CURRENT_TIMESTAMP, updated_by=? WHERE id=?;", (user_id, rental_id))
    conn.commit(); conn.close()

def restore_rental(rental_id, user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE rentals SET isDeleted=0, date_updated=CURRENT_TIMESTAMP, updated_by=? WHERE id=?;", (user_id, rental_id))
    conn.commit(); conn.close()

def list_deleted_rentals() -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT id, car_id, customer_id, start_date, planned_end_date, returned_date, total_price
                   FROM rentals WHERE isDeleted=1 ORDER BY id;""")
    rows = cur.fetchall(); conn.close(); return rows
