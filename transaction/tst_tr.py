from decimal import Decimal
from unicodedata import decimal
from uuid import uuid4, UUID

import pytest
import json

from transaction.tr import Transaction


class TestTransaction:
    def test_transaction_create(self) -> None:
        transaction = Transaction.random()
        assert isinstance(transaction, Transaction)
        transaction2 = Transaction.random()
        assert isinstance(transaction2, Transaction)
    '''def test_errors(self) -> None:
        transaction = Transaction.random()
        transaction2 = Transaction.random()

        with pytest.raises(CurrencyMismatchError):
            assert transaction2 = transaction'''

    def test_json_import_export(self) -> None:
        transaction = Transaction.random()

        json_account = transaction.to_json()

    '''def test_transaction_from_json(self) -> None:
        test_json = '{"id": "0de1375b-e9f5-4d04-afd8-efc388550a8a",' \
                    '"source_account": "0de1375b-e9f5-4d04-afd8-efc388550a8a",' \
                    '"target_account": "0de1375b-e9f5-4d04-afd8-efc388550a8a",' \
                    '"balance_brutto": 6578,' \
                    '"balance_netto": 2345,' \
                    '"currency": "KZT",}'

        transaction = Transaction.from_json_str(test_json)
        assert isinstance(transaction, Transaction)
        assert transaction.id_ == UUID("0de1375b-e9f5-4d04-afd8-efc388550a8a")
        assert transaction.balance_brutto == Decimal(6578)
        assert transaction.currency == "KZT"'''

    def test_to_json_from_json(self) -> None:
        # Check all fields are serialized
        transaction = Transaction.random()
        transaction2 = Transaction.from_json_str(transaction.to_json())
        assert transaction2 == transaction