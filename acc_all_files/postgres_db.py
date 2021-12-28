from typing import List, Optional
from uuid import UUID, uuid4
import psycopg2
import pandas as pd
from pandas import DataFrame, Series
from account.account import Account
from database.database import AccountDatabase
from database.database import ObjectNotFound


class AccountDatabasePostgres(AccountDatabase):
    def __init__(self, connection: str,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = psycopg2.connect(connection)
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id varchar primary key ,
            currency varchar ,
            balance decimal 
        );
        """)
        self.conn.commit()


    def close_connection(self):
        self.conn.close()

    def _save(self, account: Account) -> None:
        if account.id_ is None:
            account.id_ = uuid4()

        cur = self.conn.cursor()
        cur.execute("""
                UPDATE accounts SET currency = %s, balance = %s WHERE id = %s;
        """, (account.currency, account.balance, str(account.id_)))
        rows_count = cur.rowcount
        self.conn.commit()

        print("ROWS COUNT", rows_count)
        if rows_count == 0:
            cur = self.conn.cursor()
            cur.execute("""
                    INSERT INTO accounts (id, currency, balance) VALUES (%s, %s, %s);
                    """, (str(account.id_), account.currency, account.balance))
            self.conn.commit()

    def clear_all(self) -> None:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM accounts;")
        self.conn.commit()

    def get_objects(self) -> List[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts;")
        data = cur.fetchall()
        cols = [x[0] for x in cur.description]
        df = pd.DataFrame(data, columns=cols)
        return [self.pandas_row_to_account(row) for index, row in df.iterrows()]

    def pandas_row_to_account(self, row: Series) -> Account:
        return Account(
            id_=UUID(row["id"]),
            currency=row["currency"],
            balance=row["balance"],
        )

    def get_object(self, id_: UUID) -> Optional[Account]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM accounts WHERE id = %s;", (str(id_),))
        print("Trying to find", str(id_))
        data = cur.fetchall()
        if len(data) == 0:
            raise ObjectNotFound("Postgres: Object not found")
        cols = [x[0] for x in cur.description]
        # This is the implementation without Pandas
        # for i in range(len(cols)):
        #     if str(cols[i]) == "id":
        #         account_id = data[0][i]
        #     if str(cols[i]) == "balance":
        #         account_balance = data[0][i]
        #     if str(cols[i]) == "currency":
        #         account_currency = data[0][i]
        # return Account(
        #     id_=UUID(account_id),
        #     balance=account_balance,
        #     currency=account_currency,
        # )

        df = pd.DataFrame(data, columns=cols)
        return self.pandas_row_to_account(row=df.iloc[0])
