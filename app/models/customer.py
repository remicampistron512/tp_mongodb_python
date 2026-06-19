from dataclasses import dataclass, field

from .account import Account


@dataclass
class Customer:
    id: str
    first_name: str
    last_name: str
    email: str
    accounts: list[Account] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"{self.first_name} {self.last_name} \n"
            f"{self.email}"
        )