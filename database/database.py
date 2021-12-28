from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from uuid import UUID

from transaction.transaction import Transaction


class ObjectNotFound(ValueError):
    ...


@dataclass
class TransactionDatabase(ABC):  # <---- INTERFACE
    def save(self, transaction: Transaction) -> None:
        print("I am going to save this:", transaction)
        return self._save(transaction=transaction)

    @abstractmethod
    def _save(self, transaction: Transaction) -> None:
        ...

    @abstractmethod
    def clear_all(self) -> None:
        ...

    @abstractmethod
    def get_objects(self) -> List[Transaction]:
        ...

    @abstractmethod
    def get_object(self, id_: UUID) -> Transaction:
        ...