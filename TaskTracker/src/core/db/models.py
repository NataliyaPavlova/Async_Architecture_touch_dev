from pydantic import BaseModel


class Task(BaseModel):
    task_id: int
    description: str
    status: str = 'new'
    popug_id: int = 0


class User(BaseModel):
    username: str
    role: str = 'user'
    disabled: int = 0


class UserInDB(User):
    hashed_password: str
