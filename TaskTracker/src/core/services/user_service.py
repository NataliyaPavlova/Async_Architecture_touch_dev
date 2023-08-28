from fastapi import HTTPException, status

from src.core.services.abstract_service import AbstractService
from src.core.services.models import User


class UserService(AbstractService):

    def get(self, popug_public_id: str) -> User | None:
        user = self.user_repository.get(popug_public_id)
        if user:
            return User(role=user.role, email=user.email, public_id=user.public_id)



