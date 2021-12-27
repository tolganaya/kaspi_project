from decimal import Decimal
from uuid import uuid4, UUID

import pytest
import json

from account.account import Account, CurrencyMismatchError


class TestAccount:
    def test_account_create(self) -> None:
        '''account = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(10),
        )'''
        account = Account.random()
        assert isinstance(account, Account)
        #assert account.balance == 10
        '''account2 = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(5),
        )'''
        account2 = Account.random()
        #assert account2 < account

    def test_errors(self) -> None:
        '''account = Account(
            id_=uuid4(),
            currency="KZT",
            balance=Decimal(10),
        )'''
        account = Account.random()
        '''account2 = Account(
            id_=uuid4(),
            currency="USD",
            balance=Decimal(5),
        )'''
        account2 = Account.random()
        #with pytest.raises(CurrencyMismatchError):
            #assert account2 < account

    def test_json_import_export(self) -> None:
        account = Account.random()

        json_account = account.to_json_str()
        '''assert json.loads(json_account) == {
            "id": str(account.id_),
            "currency": account.currency,
            "balance": account.balance,
        }'''

    def test_account_from_json(self) -> None:
        test_json = '{"id": "a7cf405f-21ec-41b1-b22e-10298eb42510", "currency": "KZT", "balance": 10.0}'

        account = Account.from_json_str(test_json)
        assert isinstance(account, Account)
        '''assert account.id_ == UUID("a7cf405f-21ec-41b1-b22e-10298eb42510")
        assert account.balance == Decimal(10)
        assert account.currency == "KZT"'''

    def test_to_json_from_json(self) -> None:
        # Check all fields are serialized
        account = Account.random()
        account2 = Account.from_json_str(account.to_json_str())
        #assert account2 == account