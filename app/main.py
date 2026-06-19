from decimal import Decimal, InvalidOperation

from business.bank import Bank


def print_menu() -> None:
    print("""\
1. Se connecter
2. Créer un client
3. Rechercher un client
4. Modifier un client
5. Supprimer un client
0. Quitter""")


def print_dev_menu() -> None:
    print("D. Réinitialiser les données")


def print_customer_menu() -> None:
    print("""\
1. Consulter mes comptes
2. Créer un compte bancaire
3. Déposer de l'argent
4. Retirer de l'argent
5. Faire un virement
6. Voir l'historique d'un compte
0. Se déconnecter""")


def read_decimal(message: str) -> Decimal:
    while True:
        value = input(message).strip().replace(",", ".")

        try:
            amount = Decimal(value)

            if amount <= 0:
                print("Le montant doit être supérieur à 0.")
            else:
                return amount

        except InvalidOperation:
            print("Montant invalide.")


def show_login_menu(bank: Bank) -> None:
    email = input("Email du client: ").strip()
    customer = bank.find_customer_by_email(email)

    if customer is None:
        print("Client introuvable.")
        return

    print(f"Bienvenue {customer.first_name} {customer.last_name}.")
    show_customer_menu(bank, email)


def show_create_user_menu(bank: Bank) -> None:
    first_name = input("Prénom: ").strip()
    last_name = input("Nom: ").strip()
    email = input("Email: ").strip()

    bank.create_customer(first_name, last_name, email)
    print("Client créé.")


def show_create_account_menu(bank: Bank, customer_email: str) -> None:
    account_number = input("Numéro du compte: ").strip()
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
    account_number = input("Numéro du compte: ").strip()
    amount = read_decimal("Montant à déposer: ")

    bank.deposit(account_number, amount)
    print("Dépôt effectué.")


def show_withdraw_menu(bank: Bank) -> None:
    account_number = input("Numéro du compte: ").strip()
    amount = read_decimal("Montant à retirer: ")

    bank.withdraw(account_number, amount)
    print("Retrait effectué.")


def show_transfer_menu(bank: Bank) -> None:
    source_account_number = input("Numéro du compte source: ").strip()
    target_account_number = input("Numéro du compte cible: ").strip()
    amount = read_decimal("Montant à transférer: ")

    bank.transfer(source_account_number, target_account_number, amount)
    print("Virement effectué.")


def show_history_menu(bank: Bank) -> None:
    account_number = input("Numéro du compte: ").strip()
    operations = bank.get_account_history(account_number)

    if not operations:
        print("Aucune opération trouvée.")
        return

    print("Historique des opérations:")

    for operation in operations:
        print(operation)


def show_accounts_menu(bank, customer_email):
    accounts = bank.list_customer_accounts(customer_email)
    for account in accounts:
        print(account)


def show_customer_menu(bank: Bank, customer_email: str) -> None:
    while True:
        print_customer_menu()
        choice = input("Votre choix: ").strip()

        if choice == "1":
            show_accounts_menu(bank, customer_email)
        elif choice == "2":
            show_create_account_menu(bank, customer_email)
        elif choice == "3":
            show_deposit_menu(bank)
        elif choice == "4":
            show_withdraw_menu(bank)
        elif choice == "5":
            show_transfer_menu(bank)
        elif choice == "6":
            show_history_menu(bank)
        elif choice == "0":
            print("Déconnexion.")
            break
        else:
            print("Choix invalide.")


def show_modify_user_menu(bank):
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

        if choice == "1":
            show_login_menu(bank)
        elif choice == "2":
            show_create_user_menu(bank)
        elif choice == "3":
            search_term = input("Personne à rechercher: ").strip()
            search_results = bank.search_customer(search_term)
            if search_results:
                print(bank.search_customer(search_term))
            else:
                print('aucun résultat')
        elif choice == "4":
            show_modify_user_menu(bank)
        elif choice == "5":
            show_delete_user_menu(bank)
        elif choice.upper() == "D" and dev:
            confirm = input(
                "ATTENTION: cette action va réinitialiser les données. "
                "Confirmer ? (o/N) : "
            ).strip().lower()

            if confirm == "o":
                bank.reset_data()
                print("Réinitialisation effectuée.")
            else:
                print("Réinitialisation annulée.")
        elif choice == "0":
            print("Au revoir.")
            break
        else:
            print("Choix invalide.")


if __name__ == "__main__":
    main(True)
