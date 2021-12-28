import sys
from decimal import Decimal
from uuid import uuid4

from transaction.transaction import Transaction
from database.database import TransactionDatabase
from database.implementations.postgres_db import TransactionDatabasePostgres


def create_transaction(database: TransactionDatabase, balance_brutto: Decimal, balance_netto: Decimal, currency: str) -> None:
    transaction = Transaction(
        id_=uuid4(),
        balance_brutto=balance_brutto,
        balance_netto=balance_netto,
        currency=currency
    )
    database.save(transaction)


if __name__ == "__main__":
    connection_str = "dbname=p_tolganay port=5432 user=postgres password=tolganay5366 host=localhost"
    database = TransactionDatabasePostgres(connection=connection_str)
    print("Connected!")
    sys.exit(0)
