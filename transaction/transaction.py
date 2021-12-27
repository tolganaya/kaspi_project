from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass
class Transaction:
    id_: UUID
    source_account: UUID
    target_account: UUID
    balance_brutto: Decimal
    balance_netto: Decimal
    currency: str
    status: str