import random
from typing import List, Optional
from uuid import UUID, uuid4
import psycopg2
import pandas as pd
from pandas import Series
from transaction.transaction import Transaction
from account.account import Account
from database.database import TransactionDatabase
from database.database import ObjectNotFound


class TransactionDatabasePostgres(TransactionDatabase):
    def __init__(self, connection: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = psycopg2.connect(connection)
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id varchar primary key ,
            source_account varchar,
            target_account varchar,
            balance_brutto decimal, 
            balance_netto decimal,
            currency varchar
        );
        """)
        self.conn.commit()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS max_balance_account (
                max_balance varchar,
                currency varchar);
                    """)
        self.conn.commit()
        cur.execute("""insert into max_balance_account 
            (SELECT max(balance) as max_balance, currency FROM accounts group by currency);
                """)
        self.conn.commit()


    def close_connection(self):
        self.conn.close()

    def _save(self, transaction: Transaction) -> None:
        cur = self.conn.cursor()
        cur.execute("""
                select id from accounts
            """)
        acc_id = cur.fetchall()
        acc_id1 = random.sample(acc_id,k=1)[0][0]
        acc_id2 = random.sample(acc_id,k=1)[0][0]
        while True:
            if acc_id1 == acc_id2:
                acc_id2 = random.sample(acc_id,k=1)[0][0]
            else: break
        cur.execute("""
                    insert into transactions (id, source_account, target_account,
                    balance_brutto, balance_netto, currency) VALUES (%s, %s, %s, %s, %s, %s);
        """, (str(transaction.id_), str(acc_id1), str(acc_id2), transaction.balance_brutto,
              round(transaction.balance_netto,2), transaction.currency))
        self.conn.commit()

    def clear_all(self) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM transactions;")
        self.conn.commit()

    def pandas_row_to_transaction(self, row: Series) -> Transaction:
        return Transaction(
            id_=UUID(row["id"]),
            source_account=row["source_account"],
            target_account=row["target_account"],
            balance_brutto=row["balance_brutto"],
            balance_netto=row["balance_netto"],
            currency=row["currency"],
        )

    def pandas_row_to_account(self, row: Series) -> Account:
        return Account(
            id_=UUID(row["id"]),
            currency=row["currency"],
            balance=row["balance"],
        )

    def max_obj(self) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT id ,max(balance) ,currency FROM accounts group by currency ,id;")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_account(row) for index, row in df.iterrows()]

    def button(self, val) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("Insert into accounts (id, currency, balance) values (%s, 'KZT', 0);",str(val))
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_account(row) for index, row in df.iterrows()]

    def get_objects(self) -> List[Transaction]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM transactions;")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_transaction(row) for index, row in df.iterrows()]

    def get_objects_ac(self) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts;")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_account(row) for index, row in df.iterrows()]

    def get_object(self, id_: UUID) -> Optional[Transaction]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM transactions WHERE id = %s;", (str(id_),))
        print("Trying to find", str(id_))
        data = cur.fetchall()
        if len(data) == 0:
            raise ObjectNotFound("Postgres: Object not found")
        cols = [x[0] for x in cur.description]
        # This is the implementation without Pandas
        # for i in range(len(cols)):
        #     if str(cols[i]) == "id":
        #         transaction_id = data[0][i]
        #     if str(cols[i]) == "balance":
        #         transaction_balance = data[0][i]
        #     if str(cols[i]) == "currency":
        #         transaction_currency = data[0][i]
        # return Transaction(
        #     id_=UUID(transaction_id),
        #     balance=transaction_balance,
        #     currency=transaction_currency,
        # )

        df = pd.DataFrame(data, columns=cols)
        return self.pandas_row_to_transaction(row=df.iloc[0])
