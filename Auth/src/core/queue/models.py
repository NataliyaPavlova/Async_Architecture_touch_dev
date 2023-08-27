import datetime
from pydantic import BaseModel, ConfigDict
from uuid import uuid4


class EventData(BaseModel):
    public_id: str


class Event(BaseModel):
    model_config = ConfigDict(title='Event', arbitrary_types_allowed=True)
    event_id: str = str(uuid4())
    event_version: int = 1
    event_name: str
    event_time: str = datetime.datetime.now().strftime('%Y-%m-%d %H:%I:%S')
    producer: str = 'auth'
    data: EventData


class BEvent(Event):
    pass


class StreamEvent(Event):
    pass

