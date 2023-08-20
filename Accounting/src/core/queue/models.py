from pydantic import BaseModel


class Event(BaseModel):
    name: str
    public_id: str | None = None


class BEvent(Event):
    pass


class StreamEvent(Event):
    pass
