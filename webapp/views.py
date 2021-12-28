import json

from django.http import HttpResponse, HttpRequest

from django.shortcuts import render

from database.implementations.postgres_db import TransactionDatabasePostgres

connection_str = "dbname=pg_tolganay port=5432 user=postgres password=tolganay5366 host=localhost"
database = TransactionDatabasePostgres(connection=connection_str)


def transactions_list(request: HttpRequest) -> HttpResponse:
    transactions = database.get_objects()
    return render(request, "index.html", context={"transactions": transactions})


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="""<html>
        <body>
           <h1>Hello, World!</h1> 
           <h2>Try to access <a href="/transactions/">/transactions/</a></h2>
           <h3>Try to access <a href="/api/transactions/">/api/transactions/</a></h3>
        </body>
    </html>
    """)

def transactions(request: HttpRequest) -> HttpResponse:
    transactions = database.get_objects()
    json_obj = []
    for transaction in transactions:
        json_obj.append(transaction.to_json())
    return HttpResponse(content=json.dumps(json_obj))
