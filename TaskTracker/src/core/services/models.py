from pydantic import BaseModel


class TaskInService(BaseModel):
    description: str
    status: str = 'new'
    popug_id: int = 0
