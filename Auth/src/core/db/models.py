from pydantic import BaseModel
from uuid import uuid4


class User(BaseModel):
    username: str
    role: str = 'user'
    disabled: int = 0
    email: str = 'p@p'
    public_id: str = str(uuid4())


class UserInDB(User):
    hashed_password: str
