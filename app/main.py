from decimal import Decimal, InvalidOperation

from business.bank import Bank


def print_menu() -> None:
    print("""\
1. Se connecter
2. Créer un client
0. Quitter""")


def print_dev_menu() -> None:
    print("D. Réinitialiser les données")


def print_customer_menu() -> None:
    print("""\
1. Créer un compte bancaire
2. Déposer de l'argent
3. Retirer de l'argent
4. Faire un virement
5. Voir l'historique d'un compte
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


def show_customer_menu(bank: Bank, customer_email: str) -> None:
    while True:
        print_customer_menu()
        choice = input("Votre choix: ").strip()

        if choice == "1":
            show_create_account_menu(bank, customer_email)
        elif choice == "2":
            show_deposit_menu(bank)
        elif choice == "3":
            show_withdraw_menu(bank)
        elif choice == "4":
            show_transfer_menu(bank)
        elif choice == "5":
            show_history_menu(bank)
        elif choice == "0":
            print("Déconnexion.")
            break
        else:
            print("Choix invalide.")


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