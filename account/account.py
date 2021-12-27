import random
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID, uuid4
import json
import xml
import xml.etree.ElementTree as ET

class CurrencyMismatchError(ValueError):
    pass


@dataclass
class Account:
    id_: Optional[UUID]
    currency: str
    balance: Decimal

    def __lt__(self, other: "Account") -> bool:
        assert isinstance(other, Account)
        if self.currency != other.currency:
            raise CurrencyMismatchError
        return self.balance < other.balance

    def to_json(self) -> dict:
        return {
            "id": str(self.id_),
            "currency": self.currency,
            "balance": float(self.balance),
        }

    def to_json_str(self) -> str:
        return json.dumps(self.to_json())

    @classmethod
    def from_json_str(cls, json_str: str) -> "Account":  # Factory
        obj = json.loads(json_str)
        assert "currency" in obj
        assert "balance" in obj

        if "id" not in obj:
            raise ValueError("id should be in json string!")

        return cls(
            id_=UUID(obj["id"]),
            currency=obj["currency"],
            balance=Decimal(obj["balance"]),
        )

    def to_xml(self) -> str:
        root = ET.Element("account", id=str(self.id_), balance=str(self.balance), currency=self.currency)
        return xml.etree.ElementTree.tostring(root, encoding="utf8")

    @classmethod
    def from_xml(cls, xml_str: str) -> "Account":
        root = ET.fromstring(xml_str)
        if root.tag != "account":
            raise ValueError("This is not an account xml")
        id_ = UUID(root.attrib["id"])
        currency = root.attrib["currency"]
        balance = Decimal(root.attrib["balance"])
        return Account(
            id_=id_,
            currency=currency,
            balance=balance,
        )

    @classmethod
    def random(cls) -> "Account":  # Factory
        return cls(
            id_=uuid4(),
            currency=random.choice(["AMD","AZN","BTC","CNH","EUR","HKD","JPY","KGS","KRW","KZT",
                                    "MNT","RUB","TJS","TMT","TRY","UAH","USD","UZS"]),
            balance=Decimal(random.randint(100, 1000000)),
        )