import random

from src.core.services.abstract_service import AbstractService
from src.core.db.models import Task, AccountRow
from src.core.services.models import TaskInService, AccountRowInService
from src.api.request_models import TaskRequest


class AccountService(AbstractService):

    def get_account_log(self, popug_public_id: str) -> list[AccountRow] | None:
        transactions = self.account_repository.get_popugs_transactions(popug_public_id)
        return transactions or None

    def create(self, account_row: AccountRow) -> None:
        row_to_create = AccountRowInService(
                    popug_public_id=account_row.public_id,
                    task_public_id=account_row.public_id,
                    payment=(-1)*account_row.assigning_cost
                )
        self.account_repository.add(row_to_create)

