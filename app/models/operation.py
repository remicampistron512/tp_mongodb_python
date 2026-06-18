from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from .operation_status import OperationStatus


@dataclass
class Operation:
    amount: Decimal
    status: OperationStatus
    date: datetime
