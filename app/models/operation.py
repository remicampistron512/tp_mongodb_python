from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal

from .operation_status import OperationStatus


@dataclass
class Operation:
    amount: Decimal
    status: OperationStatus
    date: datetime

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} | "
            f"Montant : {self.amount} | "
            f"Statut : {self.status.value} | "
            f"Date : {self.date.strftime('%d/%m/%Y %H:%M')}"
        )