from typing import List
from uuid import UUID, uuid4

from account.account import Account
from database.database import AccountDatabase
from database.database import ObjectNotFound


class AccountDatabaseRAM(AccountDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects = dict()

    def _save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        self._objects[account.id_] = account.to_json_str()

    def clear_all(self) -> None:
        self._objects = dict()

    def get_objects(self) -> List[Account]:
        return [Account.from_json_str(v) for k, v in self._objects.items()]

    def get_object(self, id_: UUID) -> Account:
        if id_ not in self._objects:
            raise ObjectNotFound("RAM error: object not found")
        return Account.from_json_str(self._objects[id_])
