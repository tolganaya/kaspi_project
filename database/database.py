from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from uuid import UUID

from account.account import Account


class ObjectNotFound(ValueError):
    ...


@dataclass
class AccountDatabase(ABC):  # <---- INTERFACE
    def save(self, account: Account) -> None:
        print("I am going to save this:", account)
        return self._save(account=account)

    @abstractmethod
    def _save(self, account: Account) -> None:
        ...

    @abstractmethod
    def clear_all(self) -> None:
        ...

    @abstractmethod
    def get_objects(self) -> List[Account]:
        ...

    @abstractmethod
    def get_object(self, id_: UUID) -> Account:
        ...
