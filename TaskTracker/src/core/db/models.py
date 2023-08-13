from pydantic import BaseModel


class Task(BaseModel):
    task_id: int
    description: str
    status: str = 'new'
    popug_email: int = 0


class User(BaseModel):
    username: str
    role: str = 'user'
    email: str
    disabled: int = 0

