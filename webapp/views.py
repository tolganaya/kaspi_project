import json
from uuid import uuid4

from django.http import HttpResponse, HttpRequest
import os

from django.shortcuts import render

from account.account import Account
from database.database import ObjectNotFound
from database.implementations.postgres_db import AccountDatabasePostgres
from database.implementations.ram import AccountDatabaseRAM


connection_str = "dbname=pg_tolganay port=5432 user=postgres password=tolganay5366 host=127.0.0.1"
database = AccountDatabasePostgres(connection=connection_str)
print(database.get_objects())


def accounts_list(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()
    return render(request, "index.html", context={"accounts": accounts})


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="""
    <html>
        <body>
           <h1>Hello, why are you dont working!</h1> 
           <h2>Try to access <a href="/accounts/">/accounts/</a></h2>
           <h3>Try to access <a href="/api/accounts/">/api/accounts/</a></h3>
        </body>
    </html>
    """)


def accounts(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects()

    json_obj =[]
    for account in accounts:
        json_obj.append(account.to_json())
    return HttpResponse(content=json.dumps(json_obj))