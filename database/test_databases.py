from typing import Type
from uuid import uuid4

import pytest

from account.account import Account
from database.implementations.pandas_db import AccountDatabasePandas
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM
from database.database import ObjectNotFound, AccountDatabase


class TestAllDatabases:
    def test_all_dbs(self, database_connected: AccountDatabase) -> None:
        database_connected.clear_all()
        account = Account.random()
        account2 = Account.random()
        database_connected.save(account)
        database_connected.save(account2)
        got_account = database_connected.get_object(account.id_)
        assert account == got_account

        with pytest.raises(ObjectNotFound):
            database_connected.get_object(uuid4())

        all_objects = database_connected.get_objects()
        assert len(all_objects) == 2
        for acc in all_objects:
            assert isinstance(acc, Account)

        account.currency = "USD"
        database_connected.save(account)
        got_account = database_connected.get_object(account.id_)
        assert account == got_account

    def test_connection(self, connection_string: str) -> None:
        database = AccountDatabasePostgres(connection=connection_string)
        database.save(Account.random())
        all_accounts = database.get_objects()
        print(all_accounts)
        database.close_connection()
