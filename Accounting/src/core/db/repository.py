import random

from src.core.db.db import con
from src.core.db.models import Task, User, AccountRow
from src.core.services.models import TaskInService

cur = con.cursor()


def create_tables():
    cur.execute("CREATE TABLE IF NOT EXISTS popug_tasks ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "status NVARCHAR, "
                "popug_public_id NVARCHAR, "
                "public_id NVARCHAR, "
                "description NVARCHAR, "
                "assigning_cost INTEGER, "
                "price INTEGER, "
                ")")
    cur.execute("CREATE TABLE IF NOT EXISTS popugs ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "role NVARCHAR,"
                "email NVARCHAR, "
                "disabled INTEGER DEFAULT 0, "
                "public_id NVARCHAR, "
                "current_account INTEGER DEFAULT 0"
                ")")
    cur.execute("CREATE TABLE IF NOT EXISTS account_log ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "popug_public_id NVARCHAR, "
                "task_public_id NVARCHAR, "
                "payment INTEGER DEFAULT 0, "
                "created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
                ")")
    con.commit()


def close_connection():
    cur.close()
    con.close()


class TaskRepository:
    def add(self, task: TaskInService):
        price = random.randrange(20, 41)
        assigning_cost = random.randrange(-20, -9)
        cur.execute(f"INSERT INTO popug_tasks (description, status, popug_public_id, public_id, assigning_cost, price) "
                    f"VALUES ('{task.description}', '{task.status}', '{task.popug_public_id}, {task.public_id}', '{assigning_cost}', '{price}')")
        con.commit()
        return cur.lastrowid

    def get_popug_tasks(self, popug_public_id: int):
        res = cur.execute(f"SELECT description, status,id, public_id FROM popug_tasks WHERE popug_public_id='{popug_public_id}'")
        rows = res.fetchall()
        if not rows:
            return None
        return [Task(
            description=row[0],
            status=row[1],
            popug_public_id=popug_public_id,
            task_id=row[2],
            public_id=row[3],
        ) for row in rows]

    def get(self, id: int):
        res = cur.execute(f"SELECT description, status, popug_public_id, id, public_id FROM popug_tasks WHERE id='{id}'")
        row = res.fetchone()
        if not row:
            return None
        return Task(
            description=row[0],
            status=row[1],
            popug_public_id=row[2],
            task_id=row[3],
            public_id=row[4],
        )

    def get_task(self, public_id: int):
        res = cur.execute(
            f"SELECT description, status, popug_public_id, public_id FROM popug_tasks WHERE public_id='{public_id}'")
        row = res.fetchone()
        if not row:
            return None
        return Task(
            description=row[0],
            status=row[1],
            popug_public_id=row[2],
            public_id=row[3],
        )

    def update(self, task: TaskInService):
        cur.execute(f"UPDATE popug_tasks SET status='f{task.status}',popug_public_id='f{task.popug_public_id}',description='f{task.description}' WHERE public_id='{task.public_id}'")
        con.commit()


class UserRepository:
    def get(self, public_id: str) -> User | None:
        res = cur.execute(
            f"SELECT role, email,public_id,current_account FROM popugs WHERE public_id='{public_id}'")
        row = res.fetchone()
        if not row:
            return None
        return User(
            role=row[0],
            email=row[1],
            public_id=row[2],
            current_account=row[3],
        )

    def add(self, user: User) -> None:
        cur.execute(
            f"INSERT INTO popugs (role,email,public_id) VALUES ('{user.role}', '{user.email}', '{user.public_id}')")
        con.commit()

    def update_account(self, popug_public_id: str, current_account: int) -> None:
        cur.execute(
            f"UPDATE popugs SET current_account=f'{current_account}' WHERE public_id = 'f{popug_public_id}'")
        con.commit()


class AccountRepository:
    def get(self, id: int) -> AccountRow | None:
        res = cur.execute(
            f"SELECT popug_public_id, task_public_id, payment, created_at FROM account_log WHERE id='{id}'")
        row = res.fetchone()
        if not row:
            return None
        return AccountRow(
            popug_public_id=row[0],
            task_public_id=row[1],
            payment=row[2],
            created_at=row[3],
        )

    def get_popugs_transactions(self, popug_public_id: str) -> list[AccountRow] | None:
        res = cur.execute(
            f"SELECT task_public_id, payment, created_at FROM account_log WHERE popug_public_id='{popug_public_id}'")
        rows = res.fetchall()
        if not rows:
            return None
        return [AccountRow(
            task_public_id=row[0],
            payment=row[1],
            created_at=row[2],
        ) for row in rows]

    def add(self, account_row: AccountRow) -> None:
        cur.execute(
            f"INSERT INTO account_log (popug_public_id,task_public_id, payment) VALUES ('{account_row.popug_public_id}', '{account_row.task_public_id}')")
        con.commit()

