from pydantic import BaseModel


class Event(BaseModel):
    name: str
    public_id: str


class BEvent(Event):
    pass


class StreamEvent(Event):
    pass
