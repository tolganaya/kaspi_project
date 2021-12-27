from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4, uuid5
import json
import random

class CurrencyMismatchError(ValueError):
    pass

@dataclass
class Transaction:
    id_: UUID
    source_account: UUID
    target_account: UUID
    balance_brutto: Decimal
    balance_netto: Decimal
    currency: str

    def to_json(self) -> str:
        json_repr = {
            "id": str(self.id_),
            "source_account": str(self.source_account),
            "target_account": str(self.target_account),
            "balance_brutto": float(self.balance_brutto),
            "balance_netto": float(self.balance_netto),
            "currency": self.currency,
        }
        return json.dumps(json_repr)

    def to_json_str(self) -> str:
        return json.dumps(self.to_json())

    @classmethod
    def from_json_str(cls, json_str: str) -> "Transaction":  # Factory
        obj = json.loads(json_str)
        assert "id" in obj
        assert "source_account" in obj
        assert "target_account" in obj
        assert "balance_brutto" in obj
        assert "balance_netto" in obj
        assert "currency" in obj

        return cls(
            id_=UUID(obj["id"]),
            source_account=UUID(obj["source_account"]),
            target_account=UUID(obj["target_account"]),
            balance_brutto=Decimal(obj["balance_brutto"]),
            balance_netto=Decimal(obj["balance_netto"]),
            currency=str(obj["currency"]),
        )

    @classmethod
    def random(cls) -> "Transaction":  # Factory
        u_account = uuid4()
        u_id = uuid4()
        bal_b = random.randint(100, 1000000)
        bal_n = bal_b - random.randint(10,20)*bal_b/100
        return cls(
            id_=u_id,
            source_account=uuid5(u_account,str(random.randint(1,20))),
            target_account=uuid5(u_account,str(random.randint(21,40))),
            balance_brutto=Decimal(bal_b),
            balance_netto=Decimal(bal_n),
            currency=random.choice(["AMD", "AZN", "BTC", "CNH", "EUR", "HKD", "JPY", "KGS", "KRW",
                                    "KZT", "MNT", "RUB", "TJS", "TMT", "TRY", "UAH", "USD", "UZS"]),
        )