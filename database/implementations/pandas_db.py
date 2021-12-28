from typing import List
from uuid import UUID, uuid4
import pandas as pd
from pandas import DataFrame
from account.account import Account
from database.database import AccountDatabase
from database.database import ObjectNotFound


class AccountDatabasePandas(AccountDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = pd.DataFrame(columns=["id", "currency", "balance"])
        try:
            self._objects = pd.read_pickle("database.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def clear_all(self) -> None:
        self._objects = pd.DataFrame(columns=["id", "currency", "balance"])
        self._objects.to_pickle("database.pk")

    def _save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        if account.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != account.id_]

        new_row = pd.DataFrame({
            "id": [account.id_],
            "currency": [account.currency],
            "balance": [account.balance],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("database.pk")

    def get_objects(self) -> List[Account]:
        result = []
        for index, row in self._objects.iterrows():
            result.append(Account(
                id_=row["id"],
                currency=row["currency"],
                balance=row["balance"],
            ))
        return result

    def get_object(self, id_: UUID) -> Account:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            account = Account(
                id_=filtered["id"],
                currency=filtered["currency"],
                balance=filtered["balance"],
            )
            return account
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")
