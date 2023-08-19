from pydantic import BaseModel
from uuid import uuid4


class Task(BaseModel):
    task_id: int
    description: str
    status: str = 'new'
    popug_public_id: str = ''
    public_id: str = uuid4()


class User(BaseModel):
    role: str = 'user'
    email: str
    public_id: str

