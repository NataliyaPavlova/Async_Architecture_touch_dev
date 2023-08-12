from pydantic import BaseModel


class User(BaseModel):
    username: str
    role: str = 'user'
    disabled: int = 0


class UserInDB(User):
    hashed_password: str
