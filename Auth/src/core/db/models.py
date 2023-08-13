from pydantic import BaseModel


class User(BaseModel):
    username: str
    role: str = 'user'
    disabled: int = 0
    email: str = 'p@p'


class UserInDB(User):
    hashed_password: str
