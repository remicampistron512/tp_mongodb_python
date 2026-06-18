from dataclasses import dataclass

from .account import Account
from .operation import Operation


@dataclass
class Transfer(Operation):
    target: Account
