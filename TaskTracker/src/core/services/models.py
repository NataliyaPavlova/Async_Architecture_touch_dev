from pydantic import BaseModel
from fastapi_auth_middleware import AuthMiddleware, FastAPIUser


class TaskInService(BaseModel):
    description: str
    status: str = 'new'
    popug_email: str


class User(FastAPIUser):
    username: str
    role: str = 'user'
    email: str

