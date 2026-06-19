from decimal import Decimal, InvalidOperation

from business.bank import Bank
from ui.input_utils import read_decimal
from ui.messages import (
    ACCOUNT_NUMBER_MSG,
    INVALID_AMOUNT_MSG,
    INVALID_CHOICE_MSG,
    MENU,
    print_error,
    print_info,
    print_success,
    print_warning,
)


def show_create_account_menu(bank: Bank, customer_email: str) -> None:
    """
    Crée un compte bancaire pour le client connecté.

    Args:
        bank: Objet principal permettant de gérer les comptes.
        customer_email: Email du client propriétaire du compte.

    Returns:
        None.
    """
    account_number = input(ACCOUNT_NUMBER_MSG).strip()
    overdraft_limit = read_decimal("Découvert autorisé: ")
    daily_withdrawal_limit = read_decimal("Limite de retrait journalière: ")

    bank.create_account(
        customer_email,
        account_number,
        overdraft_limit,
        daily_withdrawal_limit,
    )

    print_success("Compte bancaire créé.")


def show_deposit_menu(bank: Bank) -> None:
    """
    Effectue un dépôt sur un compte bancaire.

    Args:
        bank: Objet principal permettant de gérer les opérations.

    Returns:
        None.
    """
    account_number = input(ACCOUNT_NUMBER_MSG).strip()
    amount = read_decimal("Montant à déposer: ")

    bank.deposit(account_number, amount)
    print_success("Dépôt effectué.")


def show_withdraw_menu(bank: Bank) -> None:
    """
    Effectue un retrait sur un compte bancaire.

    Args:
        bank: Objet principal permettant de gérer les opérations.

    Returns:
        None.
    """
    account_number = input(ACCOUNT_NUMBER_MSG).strip()
    amount = read_decimal("Montant à retirer: ")

    bank.withdraw(account_number, amount)
    print_success("Retrait effectué.")


def show_transfer_menu(bank: Bank) -> None:
    """
    Effectue un virement entre deux comptes bancaires.

    Args:
        bank: Objet principal permettant de gérer les opérations.

    Returns:
        None.
    """
    source_account_number = input("Numéro du compte source: ").strip()
    target_account_number = input("Numéro du compte cible: ").strip()
    amount = read_decimal("Montant à transférer: ")

    bank.transfer(source_account_number, target_account_number, amount)
    print_success("Virement effectué.")


def show_history_menu(bank: Bank) -> None:
    """
    Affiche l'historique des opérations d'un compte.

    Args:
        bank: Objet principal permettant de récupérer les opérations.

    Returns:
        None.
    """
    account_number = input(ACCOUNT_NUMBER_MSG).strip()
    operations = bank.get_account_history(account_number)

    if not operations:
        print_warning("Aucune opération trouvée.")
        return

    print_info("Historique des opérations:")

    for operation in operations:
        print(operation)


def show_accounts_menu(bank: Bank, customer_email: str) -> None:
    """
    Affiche les comptes bancaires d'un client.

    Args:
        bank: Objet principal permettant de récupérer les comptes.
        customer_email: Email du client connecté.

    Returns:
        None.
    """
    accounts = bank.list_customer_accounts(customer_email)

    for account in accounts:
        print(account)


def show_delete_account_menu(bank: Bank, customer_email: str) -> None:
    """
    Supprime un compte bancaire après confirmation de l'utilisateur.

    Args:
        bank: Objet principal permettant de gérer les comptes.
        customer_email: Email du client connecté.

    Returns:
        None.
    """
    for account in bank.list_customer_accounts(customer_email):
        print(account)

    account_number = input("Entrez le numéro du compte à supprimer : ").strip()

    if not account_number:
        print_warning("Aucun numéro de compte saisi.")
        return

    account = bank.find_account(account_number)

    if account is None:
        print_error("Aucun compte trouvé avec ce numéro.")
        return

    print_warning(f"Voulez-vous supprimer le compte : {account} ?")
    choice = input("Oui/Non : ").strip().lower()

    match choice:
        case "o" | "oui":
            bank.delete_account(account)
            print_success("Compte supprimé !")

        case "n" | "non":
            print_info("Annulation !")

        case _:
            print_error("Réponse invalide. Suppression annulée.")


def show_modify_account_menu(bank: Bank, customer_email: str) -> None:
    """
    Modifie les informations d'un compte bancaire.

    Args:
        bank: Objet principal permettant de gérer les comptes.
        customer_email: Email du client connecté.

    Returns:
        None.
    """
    for account in bank.list_customer_accounts(customer_email):
        print(account)

    account_number = input("Entrez le numéro du compte à modifier : ").strip()

    if not account_number:
        print_warning("Aucun numéro de compte saisi.")
        return

    account = bank.find_account(account_number)

    if account is None:
        print_error("Aucun compte trouvé avec ce numéro.")
        return

    old_account_number = account.account_number

    print_info(f"Compte sélectionné : {account}")

    print(f"{MENU}\nQue voulez-vous modifier ?")
    print("1. Numéro du compte")
    print("2. Solde du compte")
    print("3. Découvert autorisé")
    print("4. Plafond de retrait")
    print("0. Annuler")

    choice = input("Votre choix : ").strip()

    match choice:
        case "1":
            new_account_number = input("Nouveau numéro de compte : ").strip()

            if not new_account_number:
                print_error("Numéro invalide.")
                return

            existing_account = bank.find_account(new_account_number)

            if existing_account is not None:
                print_error("Un compte avec ce numéro existe déjà.")
                return

            account.account_number = new_account_number

        case "2":
            new_balance = input("Nouveau solde : ").strip()

            try:
                account.balance = Decimal(new_balance)
            except InvalidOperation:
                print_error("Solde invalide.")
                return

        case "3":
            new_overdraft_limit = input("Nouveau découvert autorisé : ").strip()

            try:
                account.overdraft_limit = Decimal(new_overdraft_limit)
            except InvalidOperation:
                print_error(INVALID_AMOUNT_MSG)
                return

        case "4":
            new_daily_withdrawal_limit = input("Nouveau plafond de retrait : ").strip()

            try:
                account.daily_withdrawal_limit = Decimal(new_daily_withdrawal_limit)
            except InvalidOperation:
                print_error(INVALID_AMOUNT_MSG)
                return

        case "0":
            print_info("Modification annulée.")
            return

        case _:
            print_error(INVALID_CHOICE_MSG)
            return

    bank.update_account(old_account_number, account)
    print_success("Compte modifié avec succès !")
