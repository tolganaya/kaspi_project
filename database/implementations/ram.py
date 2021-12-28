from typing import List
from uuid import UUID, uuid4

from transaction.transaction import Transaction
from database.database import TransactionDatabase
from database.database import ObjectNotFound


class TransactionDatabaseRAM(TransactionDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects = dict()

    def _save(self, transaction: Transaction) -> None:
        if transaction.id_ is None:
            transaction.id_ = uuid4()

        self._objects[transaction.id_] = transaction.to_json_str()

    def clear_all(self) -> None:
        self._objects = dict()

    def get_objects(self) -> List[Transaction]:
        return [Transaction.from_json_str(v) for k, v in self._objects.items()]

    def get_object(self, id_: UUID) -> Transaction:
        if id_ not in self._objects:
            raise ObjectNotFound("RAM error: object not found")
        return Transaction.from_json_str(self._objects[id_])