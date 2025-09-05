
from typing import Optional

try:
    from car_rental.storage.db import get_connection
except Exception:
    from storage.db import get_connection

def login(username: str, password: str) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users WHERE username=? AND password=?;", (username, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "role": row[2]}
    return None

def add_employee(username: str, password: str, role: str="employee") -> int:
    if role not in ("manager","employee"):
        raise ValueError("Role must be manager or employee")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username,password,role) VALUES (?,?,?);", (username,password,role))
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid


try:
    from car_rental.storage import repository as repo
except Exception:
    from storage import repository as repo

def list_users():
    return repo.list_users()

def search_users(keyword: str):
    return repo.search_users(keyword)
