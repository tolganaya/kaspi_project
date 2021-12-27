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
    dbname:str = os.environ.get("pg_dbname", "")
    if dbname == "":
        database = AccountDatabaseRAM()
        print("Using RAM")
    else:
        port:int = 25060
        user:str = os.environ.get("pg_user")
        password:str = os.environ.get("pg_password")
        host:str = "db-postgresql-nyc3-99638-do-user-4060406-0.b.db.ondigitalocean.com"
        connection_str = f"dbname={dbname} port={port} user={user} password={password} host={host}"
        database = AccountDatabasePostgres(connection=connection_str)
        print("Connected!")
    currency = input("Enter Currency: ")
    balance = Decimal(input("Enter balance: "))
    create_account(database=database, balance=balance, currency=currency)
    sys.exit(0)