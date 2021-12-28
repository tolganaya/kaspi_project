import json

from django.http import HttpResponse, HttpRequest

from django.shortcuts import render

from database.implementations.postgres_db import TransactionDatabasePostgres

connection_str = "dbname=pg_tolganay port=5432 user=postgres password=tolganay5366 host=localhost"
database = TransactionDatabasePostgres(connection=connection_str)


def transactions_list(request: HttpRequest) -> HttpResponse:
    transactions = database.get_objects()
    return render(request, "index_trans.html", context={"transactions": transactions})

def button(request: HttpRequest,val) -> HttpResponse:
    button = database.button(val)
    return render(request, "index_button.html", context={"button": button})

def accounts_list(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects_ac()
    return render(request, "index_account.html", context={"accounts": accounts})


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(content="""<html>
        <body>
           <h1><center>Web-service of Accounts and Transactions!</center></h1> 
           <h2>Try to access <a href="/accounts/">Accounts</a></h2>
           <h2>Try to access <a href="/transactions/">Transactions</a></h2>
           <h2>Try to access <a href="/button/">b</a></h2>
           <h3>Try to access <a href="/api/accounts/">API Accounts</a></h3>
           <h3>Try to access <a href="/api/transactions/">API Transactions</a></h3>
        </body>
    </html>
    """)

def transactions(request: HttpRequest) -> HttpResponse:
    transactions = database.get_objects()
    json_obj = []
    for transaction in transactions:
        json_obj.append(transaction.to_json())
    return HttpResponse(content=json.dumps(json_obj))

def accounts(request: HttpRequest) -> HttpResponse:
    accounts = database.get_objects_ac()
    json_obj = []
    for account in accounts:
        json_obj.append(account.to_json())
    return HttpResponse(content=json.dumps(json_obj))
