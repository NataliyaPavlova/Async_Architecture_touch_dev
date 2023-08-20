from datetime import datetime
from pydantic import BaseModel
from uuid import uuid4


class Task(BaseModel):
    task_id: int
    description: str
    status: str = 'new'
    popug_public_id: str = ''
    public_id: str


class User(BaseModel):
    role: str = 'user'
    email: str
    public_id: str
    current_account: int


class AccountRow(BaseModel):
    popug_public_id: str
    task_public_id: str
    payment: int
    created_at: datetime | None = None


