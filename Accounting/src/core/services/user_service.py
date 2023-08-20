from fastapi import HTTPException, status

from src.core.services.abstract_service import AbstractService


class UserService(AbstractService):

    def get_current_account(self, popug_public_id: str) -> int:
        user = self.user_repository.get(popug_public_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Popug not found",
            )
        return user.current_account



