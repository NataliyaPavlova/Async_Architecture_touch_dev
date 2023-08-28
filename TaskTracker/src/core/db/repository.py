from src.core.db.db import con
from src.core.db.models import Task, User
from src.core.services.models import TaskInService

cur = con.cursor()


def create_tables():
    cur.execute("CREATE TABLE IF NOT EXISTS popug_tasks ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "description NVARCHAR, "
                "status NVARCHAR, "
                "popug_public_id NVARCHAR, "
                "public_id NVARCHAR"
                ")")
    cur.execute("CREATE TABLE IF NOT EXISTS popugs ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "role NVARCHAR,"
                "email NVARCHAR, "
                "disabled INTEGER, "
                "public_id NVARCHAR "
                ")")

    con.commit()


def close_connection():
    cur.close()
    con.close()


class TaskRepository:
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

    def add(self, task: TaskInService):
        cur.execute(f"INSERT INTO popug_tasks (description, status, popug_public_id, public_id) VALUES ('{task.description}', '{task.status}', '{task.popug_public_id}, {task.public_id}')")
        con.commit()
        return cur.lastrowid

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

    def get_task(self, public_id: str):
        res = cur.execute(f"SELECT description, status, popug_public_id, public_id FROM popug_tasks WHERE public_id='{public_id}'")
        row = res.fetchone()
        if not row:
            return None
        return Task(
            description=row[0],
            status=row[1],
            popug_public_id=row[2],
            public_id=row[3],
        )

    def get_undone_tasks(self):
        res = cur.execute(f"SELECT description, status,id,popug_public_id,public_id FROM popug_tasks WHERE status!='done'")
        rows = res.fetchall()
        if not rows:
            return None
        return [Task(
            description=row[0],
            status=row[1],
            popug_public_id=row[3],
            task_id=row[2],
            public_id=row[3],
        ) for row in rows]

    def update_status(self, task_id: int):
        cur.execute(f"UPDATE popug_tasks SET status='done' WHERE id='{task_id}'")
        con.commit()
        return cur.lastrowid

    def update_assignee(self, task_id: int, popug_public_id: str):
        cur.execute(f"UPDATE popug_tasks SET popug_public_id='{popug_public_id}' WHERE id='{task_id}'")
        con.commit()
        return cur.lastrowid


class UserRepository:
    def get(self, public_id: str) -> User | None:
        res = cur.execute(
            f"SELECT role, email,public_id FROM popugs WHERE public_id='{public_id}'")
        row = res.fetchone()
        if not row:
            return None
        return User(
            role=row[0],
            email=row[1],
            public_id=row[2],
        )

    def get_list_of_workers(self) -> list[User]:
        res = cur.execute("SELECT role, email, public_id FROM popugs WHERE role='worker'")
        rows = res.fetchall()
        users = [User(
            role=row[0],
            email=row[1],
            public_id=row[2],
        ) for row in rows]
        return users

    def add(self, user: User) -> None:
        cur.execute(
            f"INSERT INTO popugs (role,email,public_id) VALUES ('{user.role}', '{user.email}', '{user.public_id}')")
        con.commit()

