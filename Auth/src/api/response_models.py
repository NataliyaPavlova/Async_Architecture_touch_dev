from pydantic import BaseModel


class HealthResponse(BaseModel):
    api_ok: bool
    ps_ok: bool
    redis_ok: bool


class UserResponse(BaseModel):
    username: str
    role: str
    email: str
    public_id: str


