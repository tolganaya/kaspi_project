from typing import Type, Any

import pytest

from database.database import TransactionDatabase
from database.implementations.postgres_db import TransactionDatabasePostgres


@pytest.fixture()
def connection_string(request: Any) -> str:
    return "dbname=pg_tolganay port=5432 user=postgres password=tolganay5366 host=localhost"


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