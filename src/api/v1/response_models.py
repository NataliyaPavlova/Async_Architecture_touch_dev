from pydantic import BaseModel


class HealthResponse(BaseModel):
    api_ok: bool
    ps_ok: bool
    rabbit_ok: bool


