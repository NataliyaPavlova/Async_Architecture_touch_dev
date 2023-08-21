from datetime import datetime
from pydantic import BaseModel


class AccountRowResponse(BaseModel):
    popug_public_id: str
    task_public_id: str
    payment: int
    created_at: datetime


class AccountingInfoResponse(BaseModel):
    current_account: int
    account_log: list[AccountRowResponse]


class HealthResponse(BaseModel):
    api_ok: bool
    db_ok: bool

