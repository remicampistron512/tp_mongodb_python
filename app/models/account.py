from dataclasses import field, dataclass
from decimal import Decimal

from models.operation import Operation


@dataclass
class Account:
    account_number: str
    balance: Decimal
    overdraft_limit: Decimal
    daily_withdrawal_limit: Decimal
    history: list[Operation] = field(default_factory=list)

    def __str__(self) -> str:
        if self.history:
            history_text = "\n".join(f"  - {operation}" for operation in self.history)
        else:
            history_text = "  Aucune opération"

        return (
            f"[Numéro de compte #{self.account_number}]\n"
            f"Solde : {self.balance}\n"
            f"Découvert autorisé : {self.overdraft_limit}\n"
            f"Plafond de retrait journalier : {self.daily_withdrawal_limit}\n"
            f"Historique :\n"
            f"{history_text}"
        )