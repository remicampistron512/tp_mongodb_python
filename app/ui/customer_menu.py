from business.bank import Bank
from ui.account_menu import (
    show_accounts_menu,
    show_create_account_menu,
    show_delete_account_menu,
    show_deposit_menu,
    show_history_menu,
    show_modify_account_menu,
    show_transfer_menu,
    show_withdraw_menu,
)
from ui.messages import INVALID_CHOICE_MSG, print_customer_menu
from ui.messages import print_error, print_info, print_success, print_warning


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
        print_error("Client introuvable.")
        return

    print_success(f"Bienvenue {customer.first_name} {customer.last_name}.")
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
    print_success("Client créé.")


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
                print_info("Déconnexion.")
                break

            case _:
                print_error(INVALID_CHOICE_MSG)


def show_modify_user_menu(bank: Bank) -> None:
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

        if customer is None:
            print_error("Aucun client trouvé avec cet email.")
            return

        print_info(f"Vous avez sélectionné : {customer}")
        customer.first_name = input("Entrez le nouveau prénom: ").strip()
        customer.last_name = input("Entrez le nouveau nom: ").strip()
        customer.new_email = input("Entrez le nouvel email").strip()

        if bank.update_customer(customer):
            print_success("Le client a bien été modifié")
        else:
            print_error("Erreur lors de la modification du client.")


def show_delete_user_menu(bank: Bank) -> None:
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
        print_warning("Aucun email saisi.")
    else:
        customer = bank.find_customer_by_email(email)

        if customer is None:
            print_error("Aucun client trouvé avec cet email.")
        else:
            print_warning(f"Voulez-vous supprimer : {customer} ?")
            choice = input("Oui/Non : ").strip().lower()

            if choice in ("o", "oui"):
                bank.delete_customer(customer.email)
                print_success("Client supprimé !")

            elif choice in ("n", "non"):
                print_info("Annulation !")

            else:
                print_error("Réponse invalide. Suppression annulée.")
