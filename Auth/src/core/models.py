from pydantic import BaseModel
from uuid import uuid4

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    public_id: str | None = None


class User(BaseModel):
    username: str
    role: str = 'user'
    disabled: int = 0
    email: str = 'p@p'
    public_id: str = uuid4()


class UserInDB(User):
    hashed_password: str
