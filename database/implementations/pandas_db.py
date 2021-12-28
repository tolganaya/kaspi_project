from typing import List
from uuid import UUID, uuid4
import pandas as pd
from pandas import DataFrame
from transaction.transaction import Transaction
from database.database import TransactionDatabase
from database.database import ObjectNotFound


class TransactionDatabasePandas(TransactionDatabase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._objects: DataFrame = pd.DataFrame(columns=["id", "source_account", "target_account", "balance_brutto", "balance_netto", "currency"])
        try:
            self._objects = pd.read_pickle("database.pk")
            print("Got database from disk:", self._objects)
        except:
            pass

    def clear_all(self) -> None:
        self._objects = pd.DataFrame(columns=["id", "source_account", "target_account", "balance_brutto", "balance_netto", "currency"])
        self._objects.to_pickle("database.pk")

    def _save(self, transaction: Transaction) -> None:
        if transaction.id_ is None:
            transaction.id_ = uuid4()

        if transaction.id_ in list(self._objects["id"]):
            self._objects = self._objects[self._objects["id"] != transaction.id_]

        new_row = pd.DataFrame({
            "id": [transaction.id_],
            "source_account": [transaction.source_account], 
            "target_account": [transaction.target_account], 
            "balance_brutto": [transaction.balance_brutto], 
            "balance_netto": [transaction.balance_netto],
            "currency": [transaction.currency],
        })
        self._objects = self._objects.append(new_row)
        self._objects.to_pickle("database.pk")

    def get_objects(self) -> List[Transaction]:
        result = []
        for index, row in self._objects.iterrows():
            result.append(Transaction(
                id_=row["id"],
                source_account=row["source_account"],
                target_account=row["target_account"],
                balance_brutto=row["balance_brutto"],
                balance_netto=row["balance_netto"],
                currency=row["currency"],
            ))
        return result

    def get_object(self, id_: UUID) -> Transaction:
        if id_ in list(self._objects["id"]):
            filtered = self._objects[self._objects["id"] == id_].iloc[0]
            transaction = Transaction(
                id_=filtered["id"],
                source_account=filtered["source_account"],
                target_account=filtered["target_account"],
                balance_brutto=filtered["balance_brutto"],
                balance_netto=filtered["balance_netto"],
                currency=filtered["currency"],
            )
            return transaction
        print("--------this object is not found:", id_)
        print(self._objects.info())
        raise ObjectNotFound("Pandas error: object not found")