from src.core.db.db import con
from src.core.db.models import Task
from src.core.services.models import TaskInService

cur = con.cursor()


def create_tables():
    cur.execute("CREATE TABLE IF NOT EXISTS popug_tasks ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "description NVARCHAR, "
                "status NVARCHAR, "
                "popug_email NVARCHAR "
                ")")
    con.commit()


def close_connection():
    # cur.execute("TRUNCATE popug_tasks")
    # con.commit()
    cur.close()
    con.close()


class TaskRepository:
    def get_popug_tasks(self, popug_email: int):
        res = cur.execute(f"SELECT description, status,id FROM popug_tasks WHERE popug_email='{popug_email}'")
        rows = res.fetchall()
        if not rows:
            return None
        return [Task(
            description=row[0],
            status=row[1],
            popug_email=popug_email,
            task_id=row[2],
        ) for row in rows]

    def add(self, task: TaskInService):
        cur.execute(f"INSERT INTO popug_tasks (description, status, popug_email) VALUES ('{task.description}', '{task.status}', '{task.popug_email}')")
        con.commit()
        return cur.lastrowid

    def get(self, id: int):
        res = cur.execute(f"SELECT description, status, popug_email, id FROM popug_tasks WHERE id='{id}'")
        row = res.fetchone()
        if not row:
            return None
        return Task(
            description=row[0],
            status=row[1],
            popug_email=row[2],
            task_id=row[3],
        )

    def get_undone_tasks(self):
        res = cur.execute(f"SELECT description, status,id,popug_email FROM popug_tasks WHERE status!='done'")
        rows = res.fetchall()
        if not rows:
            return None
        return [Task(
            description=row[0],
            status=row[1],
            popug_email=row[3],
            task_id=row[2],
        ) for row in rows]

    def update_status(self, task_id: int):
        cur.execute(f"UPDATE popug_tasks SET status='done' WHERE id='{task_id}'")
        con.commit()
        return cur.lastrowid

    def update_assignee(self, task_id: int, popug_email: str):
        cur.execute(f"UPDATE popug_tasks SET popug_email='{popug_email}' WHERE id='{task_id}'")
        con.commit()
        return cur.lastrowid

