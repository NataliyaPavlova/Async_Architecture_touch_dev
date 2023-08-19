import sqlite3

from src.core.db.models import UserInDB

con = sqlite3.connect("tutorial.db", check_same_thread=False)
cur = con.cursor()


def create_tables():

    cur.execute("CREATE TABLE IF NOT EXISTS popugs ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "public_id NVARCHAR, "
                "username NVARCHAR, "
                "password NVARCHAR, "
                "role NVARCHAR,"
                "email NVARCHAR, "
                "disabled INTEGER"
                ")")
    con.commit()


def close_connection():
    cur.close()
    con.close()


def get(username: str):
    res = cur.execute(f"SELECT username, password, role, disabled, email,public_id FROM popugs WHERE username='{username}'")
    row = res.fetchone()
    if not row:
        return None
    return UserInDB(
        username=row[0],
        hashed_password=row[1],
        role=row[2],
        disabled=row[3],
        email=row[4],
        public_id=row[5],
    )


def get_list():
    res = cur.execute("SELECT username, password, role, disabled, email FROM popugs")
    rows = res.fetchall()
    users = [UserInDB(
        username=row[0],
        hashed_password=row[1],
        role=row[2],
        disabled=row[3],
        email=row[4],
    ) for row in rows]
    return users


def add(user: UserInDB):
    cur.execute(f"INSERT INTO popugs (username, password, role,disabled,email,public_id) VALUES ('{user.username}', '{user.hashed_password}', '{user.role}', '{user.disabled}','{user.email}', '{user.public_id}')")
    con.commit()


def get_workers_db():
    res = cur.execute("SELECT id FROM popugs WHERE role NOT IN ('manager','admin')")
    rows = res.fetchall()
    users = [row[0] for row in rows]
    return users


