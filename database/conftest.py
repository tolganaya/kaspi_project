from typing import Type, Any

import pytest

from cmkcls.database import AccountDatabase
from cmkcls.pandas_db import AccountDatabasePandas
from cmkcls.postgres_db import AccountDatabasePostgres
from cmkcls.ram import AccountDatabaseRAM


@pytest.fixture()
def connection_string(request: Any) -> str:
    return "dbname=pg_tolganay port=5432 user=postgres password=tolganay5366 host=127.0.0.1"


@pytest.fixture(params=[AccountDatabasePandas, AccountDatabaseRAM, AccountDatabasePostgres])
def database_implementation(request: Any) -> Type[AccountDatabase]:
    implementation = request.param
    return implementation


@pytest.fixture()
def database_connected(
        request: Any,
        database_implementation: Type[AccountDatabase],
        connection_string: str,
) -> AccountDatabase:
    if database_implementation == AccountDatabasePostgres:
        return AccountDatabasePostgres(connection=connection_string)
    return database_implementation()