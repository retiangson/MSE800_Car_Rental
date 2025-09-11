from typing import Optional, List, Tuple
from datetime import date
from .db import get_connection

def add_car(make, model, year, vtype, base_rate, user_id) -> int:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO cars(make, model, year, "type", base_rate, status, isDeleted, isActive, created_by)
        VALUES (?, ?, ?, ?, ?, 'available', 0, 1, ?);
    """, (make, model, year, vtype, base_rate, user_id))
    conn.commit(); cid = cur.lastrowid; conn.close(); return cid

def update_car(car_id, make=None, model=None, year=None, vtype=None, base_rate=None, user_id=None):
    fields, vals = [], []
    if make is not None: fields.append("make=?"); vals.append(make)
    if model is not None: fields.append("model=?"); vals.append(model)
    if year is not None: fields.append("year=?"); vals.append(year)
    if vtype is not None: fields.append("type=?"); vals.append(vtype)
    if base_rate is not None: fields.append("base_rate=?"); vals.append(base_rate)
    if user_id is not None:
        fields.append("date_updated=CURRENT_TIMESTAMP")
        fields.append("updated_by=?"); vals.append(user_id)
    if not fields: return
    vals.append(car_id)
    conn = get_connection(); cur = conn.cursor()
    cur.execute(f"UPDATE cars SET {', '.join(fields)} WHERE id=?;", vals)
    conn.commit(); conn.close()

def list_cars(include_unavailable=True, include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    q = "SELECT id, make, model, year, type, base_rate, status FROM cars WHERE 1=1"
    if not include_deleted: q += " AND isDeleted=0"
    if not include_unavailable: q += " AND status='available'"
    q += " ORDER BY id;"
    cur.execute(q)
    rows = cur.fetchall(); conn.close(); return rows

def list_deleted_cars() -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, make, model, year, type, base_rate, status FROM cars WHERE isDeleted=1 ORDER BY id;")
    rows = cur.fetchall(); conn.close(); return rows

def search_cars(keyword: str, include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    like = f"%{keyword}%"
    q = """SELECT id, make, model, year, type, base_rate, status
           FROM cars
           WHERE (make LIKE ? OR model LIKE ? OR type LIKE ? OR CAST(year AS TEXT) LIKE ?)"""
    if not include_deleted: q += " AND isDeleted=0"
    q += " ORDER BY id;"
    cur.execute(q, (like, like, like, like))
    rows = cur.fetchall(); conn.close(); return rows

def get_car(car_id) -> Optional[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, make, model, year, type, base_rate, status, isDeleted, isActive FROM cars WHERE id=?;", (car_id,))
    row = cur.fetchone(); conn.close(); return row

def set_car_status(car_id, status):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE cars SET status=?, date_updated=CURRENT_TIMESTAMP WHERE id=?;", (status, car_id))
    conn.commit(); conn.close()

def remove_car(car_id, user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE cars SET isDeleted=1, date_updated=CURRENT_TIMESTAMP, updated_by=? WHERE id=?;", (user_id, car_id))
    conn.commit(); conn.close()

def restore_car(car_id, user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE cars SET isDeleted=0, date_updated=CURRENT_TIMESTAMP, updated_by=? WHERE id=?;", (user_id, car_id))
    conn.commit(); conn.close()
