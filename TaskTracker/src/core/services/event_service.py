from src.core.queue.models import BEvent, StreamEvent
from src.core.services.abstract_service import AbstractService
from src.core.services.auth_service import AuthService
from src.core.services.models import User


class EventService(AbstractService):

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()

    async def process_business_event(self, event: BEvent):
        ...

    async def process_stream_event(self, event: StreamEvent):
        if event.event_name == 'UserCreated':
            popug = self.user_repository.get(event.data.public_id)
            if not popug:
                popug = self.auth_service.get_popug_info(event.data.public_id)
                self.user_repository.add(User(
                    role=popug.role, email=popug.email, public_id=event.public_id)
                )

