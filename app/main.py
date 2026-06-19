from decimal import Decimal, InvalidOperation

from business.bank import Bank
from services.dummy_data_service import DummyDataService

INVALID_CHOICE_MSG = "Choix invalide"
ACCOUNT_NUMBER_MSG = "Numéro de compte"
INVALID_AMOUNT_MSG = "Montant invalide"


def print_menu() -> None:
    """
    Affiche le menu principal de l'application.

    Args:
        Aucun.

    Returns:
        None.
    """
    print("""\
1. Se connecter
2. Créer un client
3. Rechercher un client
4. Modifier un client
5. Supprimer un client
0. Quitter""")


def print_dev_menu() -> None:
    """
    Affiche le menu réservé au mode développement.

    Args:
        Aucun.

    Returns:
        None.
    """
    print("D. Réinitialiser les données")


def print_customer_menu() -> None:
    """
    Affiche le menu disponible pour un client connecté.

    Args:
        Aucun.

    Returns:
        None.
    """
    print("""\
1. Consulter mes comptes
2. Créer un compte bancaire
3. Déposer de l'argent
4. Retirer de l'argent
5. Faire un virement
6. Voir l'historique d'un compte
7. Supprimer un compte
8. Modifier un compte
D. Réinitialiser les données
0. Se déconnecter""")


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
                print("Le montant doit être supérieur à 0.")
            else:
                return amount

        except InvalidOperation:
            print(INVALID_AMOUNT_MSG)


def show_login_menu(bank: Bank) -> None:
    """
    Connecte un client à partir de son adresse email.

    Args:
        bank: Objet principal permettant d'accéder aux services bancaires.

    Returns:
        None.
    """
    email = input("Email du client: ").strip()
    customer = bank.find_customer_by_email(email)

    if customer is None:
        print("Client introuvable.")
        return

    print(f"Bienvenue {customer.first_name} {customer.last_name}.")
    show_customer_menu(bank, email)


def show_create_user_menu(bank: Bank) -> None:
    """
    Demande les informations nécessaires et crée un nouveau client.

    Args:
        bank: Objet principal permettant de gérer les clients.

    Returns:
        None.
    """
    first_name = input("Prénom: ").strip()
    last_name = input("Nom: ").strip()
    email = input("Email: ").strip()

    bank.create_customer(first_name, last_name, email)
    print("Client créé.")


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

    print("Compte bancaire créé.")


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
    print("Dépôt effectué.")


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
    print("Retrait effectué.")


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
    print("Virement effectué.")


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
        print("Aucune opération trouvée.")
        return

    print("Historique des opérations:")

    for operation in operations:
        print(operation)


def show_accounts_menu(bank, customer_email):
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


def show_delete_account_menu(bank: Bank, customer_email):
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
        print("Aucun numéro de compte saisi.")
        return

    account = bank.find_account(account_number)

    if account is None:
        print("Aucun compte trouvé avec ce numéro.")
        return

    print(f"Voulez-vous supprimer le compte : {account} ?")
    choice = input("Oui/Non : ").strip().lower()

    match choice:
        case "o" | "oui":
            bank.delete_account(account)
            print("Compte supprimé !")

        case "n" | "non":
            print("Annulation !")

        case _:
            print("Réponse invalide. Suppression annulée.")


def show_modify_account_menu(bank: Bank, customer_email):
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
        print("Aucun numéro de compte saisi.")
        return

    account = bank.find_account(account_number)

    if account is None:
        print("Aucun compte trouvé avec ce numéro.")
        return

    old_account_number = account.account_number

    print(f"Compte sélectionné : {account}")

    print("\nQue voulez-vous modifier ?")
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
                print("Numéro invalide.")
                return

            existing_account = bank.find_account(new_account_number)

            if existing_account is not None:
                print("Un compte avec ce numéro existe déjà.")
                return

            account.account_number = new_account_number

        case "2":
            new_balance = input("Nouveau solde : ").strip()

            try:
                account.balance = Decimal(new_balance)
            except InvalidOperation:
                print("Solde invalide.")
                return

        case "3":
            new_overdraft_limit = input("Nouveau découvert autorisé : ").strip()

            try:
                account.overdraft_limit = Decimal(new_overdraft_limit)
            except InvalidOperation:
                print(INVALID_AMOUNT_MSG)
                return

        case "4":
            new_daily_withdrawal_limit = input("Nouveau plafond de retrait : ").strip()

            try:
                account.daily_withdrawal_limit = Decimal(new_daily_withdrawal_limit)
            except InvalidOperation:
                print(INVALID_AMOUNT_MSG)
                return

        case "0":
            print("Modification annulée.")
            return

        case _:
            print(INVALID_CHOICE_MSG)
            return

    bank.update_account(old_account_number, account)
    print("Compte modifié avec succès !")


def show_customer_menu(bank: Bank, customer_email: str) -> None:
    """
    Affiche et gère le menu d'un client connecté.

    Args:
        bank: Objet principal permettant d'exécuter les actions bancaires.
        customer_email: Email du client connecté.

    Returns:
        None.
    """
    while True:
        print_customer_menu()
        choice = input("Votre choix: ").strip()

        match choice:
            case "1":
                show_accounts_menu(bank, customer_email)

            case "2":
                show_create_account_menu(bank, customer_email)

            case "3":
                show_deposit_menu(bank)

            case "4":
                show_withdraw_menu(bank)

            case "5":
                show_transfer_menu(bank)

            case "6":
                show_history_menu(bank)

            case "7":
                show_delete_account_menu(bank, customer_email)

            case "8":
                show_modify_account_menu(bank, customer_email)

            case "0":
                print("Déconnexion.")
                break

            case _:
                print(INVALID_CHOICE_MSG)


def show_modify_user_menu(bank):
    """
    Modifie les informations d'un client existant.

    Args:
        bank: Objet principal permettant de gérer les clients.

    Returns:
        None.
    """
    for customer in bank.list_customers():
        print(customer)

    email = input("Entrez le mail du client: ").strip()

    if email:
        customer = bank.find_customer_by_email(email)
        print(f"Vous avez sélectionné : {customer}")
        customer.first_name = input("Entrez le nouveau prénom: ").strip()
        customer.last_name = input("Entrez le nouveau nom: ").strip()
        customer.new_email = input("Entrez le nouvel email").strip()

        if bank.update_customer(customer):
            print("Le client a bien été modifié")
        else:
            print("erreur")


def show_delete_user_menu(bank):
    """
    Supprime un client après confirmation de l'utilisateur.

    Args:
        bank: Objet principal permettant de gérer les clients.

    Returns:
        None.
    """
    for customer in bank.list_customers():
        print(customer)

    email = input("Entrez le mail du client : ").strip()

    if not email:
        print("Aucun email saisi.")
    else:
        customer = bank.find_customer_by_email(email)

        if customer is None:
            print("Aucun client trouvé avec cet email.")
        else:
            print(f"Voulez-vous supprimer : {customer} ?")
            choice = input("Oui/Non : ").strip().lower()

            if choice in ("o", "oui"):
                bank.delete_customer(customer.email)
                print("Client supprimé !")

            elif choice in ("n", "non"):
                print("Annulation !")

            else:
                print("Réponse invalide. Suppression annulée.")


def main(dev: bool = False) -> None:
    """
    Lance l'application et affiche le menu principal.

    Args:
        dev: Active ou non le mode développement.

    Returns:
        None.
    """
    print("""\
--------------------------
Bienvenue dans l'application Bank
--------------------------""")

    bank: Bank = Bank()

    while True:
        print_menu()

        if dev:
            print_dev_menu()

        choice = input("Votre choix: ").strip()

        match choice:
            case "1":
                show_login_menu(bank)

            case "2":
                show_create_user_menu(bank)

            case "3":
                search_term = input("Personne à rechercher : ").strip()
                search_results = bank.search_customer(search_term)

                if search_results:
                    print(search_results)
                else:
                    print("Aucun résultat.")

            case "4":
                show_modify_user_menu(bank)

            case "5":
                show_delete_user_menu(bank)

            case "D" | "d" if dev:
                confirm = input(
                    "ATTENTION: cette action va réinitialiser les données. "
                    "Confirmer ? (o/N) : "
                ).strip().lower()

                if confirm == "o":
                    dummy_service = DummyDataService(bank)
                    dummy_service.generate()
                    print("Données de test générées.")
                    print("Réinitialisation effectuée.")
                else:
                    print("Réinitialisation annulée.")

            case "0":
                print("Au revoir.")
                break

            case _:
                print("Choix invalide.")


if __name__ == "__main__":
    main(True)

