from typing import Optional, List, Tuple
from .db import get_connection

def list_users(include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    q = "SELECT id, username, role FROM users WHERE 1=1"
    if not include_deleted:
        q += " AND isDeleted=0"
    else:
        q += " AND isDeleted=1"
    q += " ORDER BY id;"
    cur.execute(q)
    rows = cur.fetchall(); conn.close(); return rows

def search_users(keyword: str, include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    like = f"%{keyword}%"
    q = "SELECT id, username, role FROM users WHERE (username LIKE ? OR role LIKE ?)"
    if not include_deleted: q += " AND isDeleted=0"
    q += " ORDER BY id;"
    cur.execute(q, (like, like))
    rows = cur.fetchall(); conn.close(); return rows

def remove_user(user_id, acting_user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE users SET isDeleted=1 WHERE id=?;", (user_id,))
    conn.commit(); conn.close()

def restore_user(user_id, acting_user_id):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE users SET isDeleted=0 WHERE id=?;", (user_id,))
    conn.commit(); conn.close()

# -------------------- Authentication --------------------
def login(username: str, password: str) -> Optional[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, role FROM users WHERE username=? AND password=?;", (username, password))
    row = cur.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "username": row[1], "role": row[2]}
    return None

def add_employee(username: str, password: str, role: str = "employee") -> int:
    if role not in ("manager", "employee"):
        raise ValueError("Role must be manager or employee")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users(username,password,role) VALUES (?,?,?);", (username, password, role))
    conn.commit()
    uid = cur.lastrowid
    conn.close()
    return uid