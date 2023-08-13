from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    role: str = 'user'
    disabled: int = 0
    email: str = 'p@p'


class UserInDB(User):
    hashed_password: str
