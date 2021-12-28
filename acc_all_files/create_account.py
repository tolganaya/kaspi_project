import sys
from decimal import Decimal
from uuid import uuid4

from account.account import Account
from database.database import AccountDatabase
from database.implementations.postgres_db import AccountDatabasePostgres
import os

from database.implementations.ram import AccountDatabaseRAM


def create_account(database: AccountDatabase, currency: str, balance: Decimal) -> None:
    account = Account(
        id_=uuid4(),
        currency=currency,
        balance=balance,
    )
    database.save(account)


if __name__ == "__main__":
    connection_str = "dbname=p_tolganay port=5432 user=postgres password=tolganay5366 host=localhost"
    database = AccountDatabasePostgres(connection=connection_str)
    print("Connected!")
    sys.exit(0)
