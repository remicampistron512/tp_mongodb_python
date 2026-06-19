from business.bank import Bank
from ui.main_menu import show_main_menu


def main(dev: bool = False) -> None:
    """
    Lance l'application bancaire.

    Args:
        dev: Active ou non le mode développement.

    Returns:
        None.
    """
    bank = Bank()
    show_main_menu(bank, dev)


if __name__ == "__main__":
    main(True)
