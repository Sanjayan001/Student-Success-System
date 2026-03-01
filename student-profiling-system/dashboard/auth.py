import os
import sqlite3
import bcrypt
from typing import Optional

DB_PATH = os.path.join("models", "auth.db")

def _get_conn():
    os.makedirs("models", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash BLOB NOT NULL
    )""")
    conn.commit()
    return conn

def create_admin_if_missing(username: str, password: str) -> None:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cur.fetchone() is None:
        pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cur.execute("INSERT INTO users(username, password_hash) VALUES(?,?)", (username, pw_hash))
        conn.commit()
    conn.close()

def add_user(username: str, password: str) -> Optional[str]:
    username = (username or "").strip()
    password = (password or "").strip()
    if not username or not password:
        return "Username and password are required."
    if len(password) < 6:
        return "Password must be at least 6 characters."
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cur.fetchone() is not None:
        conn.close()
        return "Username already exists."
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    cur.execute("INSERT INTO users(username, password_hash) VALUES(?,?)", (username, pw_hash))
    conn.commit()
    conn.close()
    return None

def verify_login(username: str, password: str) -> bool:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM users WHERE username = ?", ((username or "").strip(),))
    row = cur.fetchone()
    conn.close()
    if not row:
        return False
    return bcrypt.checkpw((password or "").encode("utf-8"), row[0])
