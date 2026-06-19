from business.bank import Bank
from services.dummy_data_service import DummyDataService
from ui.customer_menu import (
    show_create_user_menu,
    show_delete_user_menu,
    show_login_menu,
    show_modify_user_menu,
)
from ui.messages import (
    INVALID_CHOICE_MSG,
    TITLE,
    WARNING,
    print_dev_menu,
    print_error,
    print_info,
    print_main_menu,
    print_success,
    print_warning,
)


def show_main_menu(bank: Bank, dev: bool = False) -> None:
    """
    Affiche et gère le menu principal de l'application.

    Args:
        bank: Objet principal permettant d'exécuter les actions bancaires.
        dev: Active ou non le mode développement.

    Returns:
        None.
    """
    print(f"""{TITLE}\
--------------------------
Bienvenue dans l'application Bank
--------------------------""")

    while True:
        print_main_menu()

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
                    print_warning("Aucun résultat.")

            case "4":
                show_modify_user_menu(bank)

            case "5":
                show_delete_user_menu(bank)

            case "D" | "d" if dev:
                confirm = input(
                    f"{WARNING}ATTENTION: cette action va réinitialiser les données. "
                    "Confirmer ? (o/N) : "
                ).strip().lower()

                if confirm == "o":
                    dummy_service = DummyDataService(bank)
                    dummy_service.generate()
                    print_success("Données de test générées.")
                    print_success("Réinitialisation effectuée.")
                else:
                    print_info("Réinitialisation annulée.")

            case "0":
                print_info("Au revoir.")
                break

            case _:
                print_error(INVALID_CHOICE_MSG)
