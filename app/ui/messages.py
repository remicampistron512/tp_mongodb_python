from colorama import Fore, Style, init

init(autoreset=True)

SUCCESS = Fore.GREEN
ERROR = Fore.RED
WARNING = Fore.YELLOW
INFO = Fore.CYAN
TITLE = Fore.MAGENTA + Style.BRIGHT
MENU = Fore.BLUE

INVALID_CHOICE_MSG = "Choix invalide"
ACCOUNT_NUMBER_MSG = "Numéro de compte"
INVALID_AMOUNT_MSG = "Montant invalide"


def print_success(message: str) -> None:
    """
    Affiche un message de réussite en vert.

    Args:
        message: Message à afficher.

    Returns:
        None.
    """
    print(f"{SUCCESS}{message}")


def print_error(message: str) -> None:
    """
    Affiche un message d'erreur en rouge.

    Args:
        message: Message à afficher.

    Returns:
        None.
    """
    print(f"{ERROR}{message}")


def print_warning(message: str) -> None:
    """
    Affiche un message d'avertissement en jaune.

    Args:
        message: Message à afficher.

    Returns:
        None.
    """
    print(f"{WARNING}{message}")


def print_info(message: str) -> None:
    """
    Affiche un message d'information en cyan.

    Args:
        message: Message à afficher.

    Returns:
        None.
    """
    print(f"{INFO}{message}")


def print_main_menu() -> None:
    """
    Affiche le menu principal de l'application.

    Args:
        Aucun.

    Returns:
        None.
    """
    print(f"""{MENU}\
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
    print(f"{WARNING}D. Réinitialiser les données")


def print_customer_menu() -> None:
    """
    Affiche le menu disponible pour un client connecté.

    Args:
        Aucun.

    Returns:
        None.
    """
    print(f"""{MENU}\
1. Consulter mes comptes
2. Créer un compte bancaire
3. Déposer de l'argent
4. Retirer de l'argent
5. Faire un virement
6. Voir l'historique d'un compte
7. Supprimer un compte
8. Modifier un compte
0. Se déconnecter""")
