from pydantic import BaseModel


class TaskResponse(BaseModel):
    task_id: int
    description: str
    status: str
    popug_id: int | None


class HealthResponse(BaseModel):
    api_ok: bool
    db_ok: bool

