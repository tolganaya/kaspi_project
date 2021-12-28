from uuid import uuid4

import pytest

from transaction.transaction import Transaction
from database.implementations.postgres_db import TransactionDatabasePostgres
from database.database import ObjectNotFound, TransactionDatabase


class TestAllDatabases:
    def test_all_dbs(self, database_connected: TransactionDatabase) -> None:
        #database_connected.clear_all()
        transaction = Transaction.random()
        transaction2 = Transaction.random()
        database_connected.save(transaction)
        database_connected.save(transaction2)
        got_transaction = database_connected.get_object(transaction.id_)
        #assert transaction == got_transaction

        with pytest.raises(ObjectNotFound):
            database_connected.get_object(uuid4())

        all_objects = database_connected.get_objects()
        #assert len(all_objects) == 2
        for acc in all_objects:
            assert isinstance(acc, Transaction)

        #transaction.currency = "USD"
        database_connected.save(transaction)
        got_transaction = database_connected.get_object(transaction.id_)
        #assert transaction == got_transaction

    def test_connection(self, connection_string: str) -> None:
        database = TransactionDatabasePostgres(connection=connection_string)
        database.save(Transaction.random())
        all_transactions = database.get_objects()
        print('STARTS HERE -------------------------------------------------------------------------------------')
        print(all_transactions)
        database.close_connection()