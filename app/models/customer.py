from dataclasses import dataclass, field

from .account import Account


@dataclass
class Customer:
    id: str
    first_name: str
    last_name: str
    email: str
    accounts: list[Account] = field(default_factory=list)
