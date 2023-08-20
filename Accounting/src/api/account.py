from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends, HTTPException, status


from src.api.response_models import AccountingInfoResponse, AccountRowResponse

from src.core.services.user_service import UserService
from src.core.services.account_service import AccountService
from src.core.queue.models import BEvent, StreamEvent


router = APIRouter(prefix="", tags=["account"])


@router.get('/{popug_public_id}',
            response_model=AccountingInfoResponse,
            response_model_exclude_none=True,
            status_code=status.HTTP_200_OK,
            summary='Get accounting info for popug',
            response_description='Accounting Log and current account for the popug'
            )
async def get_popug_accounting_info(
        popug_public_id: str,
        user_service: UserService = Depends(),
        account_service: AccountService = Depends(),
) -> AccountingInfoResponse:
    current_account = user_service.get_current_account(popug_public_id)
    account_log = account_service.get_account_log(popug_public_id)
    if not current_account or account_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Something bad happened",
        )
    return AccountingInfoResponse(
            current_account=current_account,
            account_log=[AccountRowResponse(
                popug_public_id=popug_public_id,
                task_public_id=row.task_public_id,
                payment=row.payment,
                created_at=row.created_at
            ) for row in account_log])



