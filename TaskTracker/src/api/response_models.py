from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_id: int
    description: str
    status: str
    popug_public_id: str | None
    public_id: str


class HealthResponse(BaseModel):
    api_ok: bool
    db_ok: bool


class UserResponse(BaseModel):
    username: str
    role: str = 'user'
    email: str
    disabled: int = 0
    public_id: str
