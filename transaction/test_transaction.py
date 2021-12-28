from decimal import Decimal
from unicodedata import decimal
from uuid import uuid4, UUID

import pytest
import json

from transaction.transaction import Transaction


class TestTransaction:
    def test_transaction_create(self) -> None:
        transaction = Transaction (
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(56876),
            balance_netto=Decimal(34555),
            currency="KZT",
        )
        #transaction = Transaction.random()
        assert isinstance(transaction, Transaction)
        transaction2 = transaction = Transaction (
            id_=uuid4(),
            source_account=uuid4(),
            target_account=uuid4(),
            balance_brutto=Decimal(6578),
            balance_netto=Decimal(2345),
            currency="KZT",
        )
        #transaction2 = Transaction.random()
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
        test_json = '{"id": "0de1375b-e9f5-4d04-afd8-efc398550a8a",' \
                    '"source_account": "0de1375b-e9f5-4d04-afd8-efc388550a8b",' \
                    '"target_account": "0de1375b-e9f5-4d04-afd8-efc388550a8c",' \
                    '"balance_brutto": 56876.0,' \
                    '"balance_netto": 34555.0,' \
                    '"currency": "KZT",}'

        transaction = Transaction.from_json_str(test_json)
        assert isinstance(transaction, Transaction)
        assert transaction.id_ == UUID("0de1375b-e9f5-4d04-afd8-efc398550a8a")
        assert transaction.balance_brutto == Decimal(6578)
        assert transaction.currency == "KZT"'''

    def test_to_json_from_json(self) -> None:
        # Check all fields are serialized
        transaction = Transaction.random()
        transaction2 = Transaction.from_json_str(transaction.to_json())
        #assert transaction2 == transaction