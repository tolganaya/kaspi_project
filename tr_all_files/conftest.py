from typing import Type, Any

import pytest

from database.database import TransactionDatabase
from database.implementations.pandas_db import TransactionDatabasePandas
from database.implementations.postgres_db import TransactionDatabasePostgres
from database.implementations.ram import TransactionDatabaseRAM


@pytest.fixture()
def connection_string(request: Any) -> str:
    return "dbname=pg_tolganay port=5432 user=postgres password=tolganay5366 host=127.0.0.1"


@pytest.fixture(params=[TransactionDatabasePostgres])
def database_implementation(request: Any) -> Type[TransactionDatabase]:
    implementation = request.param
    return implementation


@pytest.fixture()
def database_connected(
        request: Any,
        database_implementation: Type[TransactionDatabase],
        connection_string: str,
) -> TransactionDatabase:
    if database_implementation == TransactionDatabasePostgres:
        return TransactionDatabasePostgres(connection=connection_string)
    return database_implementation()