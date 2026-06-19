from decimal import Decimal, InvalidOperation

from ui.messages import INVALID_AMOUNT_MSG
from ui.messages import print_error, print_warning


def read_decimal(message: str) -> Decimal:
    """
    Demande à l'utilisateur de saisir un montant valide.

    Args:
        message: Message affiché lors de la saisie.

    Returns:
        Le montant saisi sous forme de Decimal.
    """
    while True:
        value = input(message).strip().replace(",", ".")

        try:
            amount = Decimal(value)

            if amount <= 0:
                print_warning("Le montant doit être supérieur à 0.")
            else:
                return amount

        except InvalidOperation:
            print_error(INVALID_AMOUNT_MSG)
