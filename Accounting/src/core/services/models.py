from datetime import datetime
from uuid import uuid4
from pydantic import BaseModel
from fastapi_auth_middleware import FastAPIUser


class TaskInService(BaseModel):
    description: str
    status: str = 'new'
    popug_public_id: str
    public_id: str = uuid4()


class User(FastAPIUser):
    role: str
    email: str
    public_id: str


class AccountRowInService(BaseModel):
    popug_public_id: str
    task_public_id: str
    payment: int

