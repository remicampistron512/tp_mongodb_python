from dataclasses import dataclass, field
from decimal import Decimal

from .operation import Operation


@dataclass
class Account:
    account_number: str
    balance: Decimal
    overdraft_limit: Decimal
    daily_withdrawal_limit: Decimal
    history: list[Operation] = field(default_factory=list)
