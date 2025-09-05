from typing import Optional, List, Tuple
from .db import get_connection

def add_customer(name, email, phone) -> int:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
        INSERT INTO customers(name, email, phone, isDeleted, isActive)
        VALUES (?, ?, ?, 0, 1);
    """, (name, email, phone))
    conn.commit(); cid = cur.lastrowid; conn.close(); return cid

def list_customers(include_deleted: bool = False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    q = "SELECT id, name, email, phone, isDeleted, isActive FROM customers WHERE 1=1"
    if not include_deleted:
        q += " AND isDeleted=0"
    q += " ORDER BY id;"
    cur.execute(q)
    rows = cur.fetchall(); conn.close(); return rows

def search_customers(keyword: str, include_deleted: bool = False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    like = f"%{keyword}%"
    q = "SELECT id, name, email, phone, isDeleted, isActive FROM customers WHERE (name LIKE ? OR email LIKE ?)"
    if not include_deleted:
        q += " AND isDeleted=0"
    q += " ORDER BY id;"
    cur.execute(q, (like, like))
    rows = cur.fetchall(); conn.close(); return rows

def search_customers(keyword: str, include_deleted=False) -> List[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    like = f"%{keyword}%"
    q = "SELECT id, name, email, phone FROM customers WHERE (name LIKE ? OR email LIKE ?)"
    if not include_deleted: q += " AND isDeleted=0"
    q += " ORDER BY id;"
    cur.execute(q, (like, like))
    rows = cur.fetchall(); conn.close(); return rows

def get_customer_by_email(email: str) -> Optional[Tuple]:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT id, name, email, phone, isDeleted, isActive
                   FROM customers WHERE email=? AND isDeleted=0 AND isActive=1;""", (email,))
    row = cur.fetchone(); conn.close(); return row

def remove_customer(customer_id: int, user_id: int):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""UPDATE customers
                   SET isDeleted=1, isActive=0
                   WHERE id=?;""", (customer_id,))
    conn.commit(); conn.close()

def restore_customer(customer_id: int, user_id: int):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""UPDATE customers
                   SET isDeleted=0, isActive=1
                   WHERE id=?;""", (customer_id,))
    conn.commit(); conn.close()
