from src.core.db.db import con
from src.core.db.models import UserInDB

cur = con.cursor()


def create_tables():
    cur.execute("CREATE TABLE IF NOT EXISTS popugs ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "username NVARCHAR, "
                "password NVARCHAR, "
                "role NVARCHAR, "
                "disabled INTEGER"
                ")")
    con.commit()


def close_connection():
    cur.close()
    con.close()


def get(username: str):
    res = cur.execute(f"SELECT username, password, role, disabled FROM popugs WHERE username='{username}'")
    row = res.fetchone()
    if not row:
        return None
    return UserInDB(
        username=row[0],
        hashed_password=row[1],
        role=row[2],
        disabled=row[3],
    )


def get_list():
    res = cur.execute("SELECT username, password, role, disabled FROM popugs")
    rows = res.fetchall()
    users = [UserInDB(
        username=row[0],
        hashed_password=row[1],
        role=row[2],
        disabled=row[3],
    ) for row in rows]
    return users


def add(user: UserInDB):
    cur.execute(f"INSERT INTO popugs (username, password, role,disabled) VALUES ('{user.username}', '{user.hashed_password}', '{user.role}', '{user.disabled}')")
    con.commit()

