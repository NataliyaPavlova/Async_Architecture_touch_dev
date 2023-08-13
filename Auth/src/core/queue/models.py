from pydantic import BaseModel


class Event(BaseModel):
    name: str


class BEvent(Event):
    pass


class CUDEvent(Event):
    pass
