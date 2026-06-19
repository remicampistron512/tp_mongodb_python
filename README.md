# Application de gestion de compte en banque

## Description

Exercice pour comprendre le fonctionnement de MongoDB avec une application console en Python.

L'application permet de gérer des clients, leurs comptes bancaires et les opérations réalisées sur ces comptes. Les données sont enregistrées dans une base MongoDB locale nommée `bank_db`.

## Fonctionnalités

* Gestion des clients
  * Créer un client
  * Rechercher un client
  * Modifier un client
  * Supprimer un client
  * Lister les clients
* Gestion des comptes
  * Créer un compte bancaire
  * Consulter les comptes d'un client
  * Modifier un compte
  * Supprimer un compte
  * Lister les comptes
* Gestion des opérations
  * Effectuer un dépôt
  * Effectuer un retrait
  * Effectuer un virement
  * Consulter l'historique des opérations
* Mode développement
  * Réinitialiser les données
  * Générer des données de test

## Technologies utilisées

* Python
* MongoDB
* PyMongo

## Installation

### 1. Cloner ou récupérer le projet

Placez-vous dans le dossier du projet :

```bash
cd app
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

Activation sous Windows :

```bash
.venv\Scripts\activate
```

Activation sous Linux/macOS :

```bash
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install requirements.txt
```

### 4. Lancer MongoDB

L'application se connecte à MongoDB avec l'URL suivante :

```text
mongodb://localhost:27017/
```

Il faut donc avoir un serveur MongoDB lancé en local avant de démarrer l'application.

La base utilisée est :

```text
bank_db
```

Les collections utilisées sont :

* `customers`
* `accounts`
* `operations`

## Utilisation

Depuis le dossier parent du projet, lancer l'application avec :

```bash
PYTHONPATH=.:./app python app/main.py
```

Sur Windows PowerShell :

```powershell
$env:PYTHONPATH=".;.\app"
python app/main.py
```

Au démarrage, le menu principal propose :

```text
1. Se connecter
2. Créer un client
3. Rechercher un client
4. Modifier un client
5. Supprimer un client
0. Quitter
```

Une fois connecté avec l'email d'un client, l'utilisateur peut gérer ses comptes :

```text
1. Consulter mes comptes
2. Créer un compte bancaire
3. Déposer de l'argent
4. Retirer de l'argent
5. Faire un virement
6. Voir l'historique d'un compte
7. Supprimer un compte
8. Modifier un compte
0. Se déconnecter
```

## Données de test

Le programme contient un service `DummyDataService` permettant de réinitialiser les données et de générer des clients, des comptes et des opérations de test.

Dans la version actuelle, le fichier `main.py` lance l'application en mode développement :

```python
main(True)
```

Cela affiche l'option :

```text
D. Réinitialiser les données
```

## Structure du code

```text
app/
├── main.py
├── business/
│   └── bank.py
├── daos/
│   ├── account_dao.py
│   ├── customer_dao.py
│   ├── mongo_connection.py
│   └── operation_dao.py
├── models/
│   ├── account.py
│   ├── customer.py
│   ├── deposit.py
│   ├── operation.py
│   ├── operation_status.py
│   ├── transfer.py
│   └── withdrawal.py
└── services/
    └── dummy_data_service.py
```

### Rôle des dossiers

* `main.py` : point d'entrée de l'application console et gestion des menus.
* `models/` : classes métier représentant les clients, comptes et opérations.
* `daos/` : couche d'accès aux données MongoDB.
* `business/` : couche métier, avec la classe `Bank` qui centralise les actions principales.
* `services/` : services complémentaires, comme la génération de données de test.

## Règles métier principales

* Un client est identifié par son email.
* Un client peut posséder plusieurs comptes bancaires.
* Un compte contient :
  * un numéro de compte ;
  * un solde ;
  * un découvert autorisé ;
  * une limite de retrait journalière.
* Un dépôt augmente le solde du compte.
* Un retrait diminue le solde du compte si le découvert autorisé n'est pas dépassé.
* Un virement débite un compte source et crédite un compte cible si l'opération est autorisée.
* Chaque opération est enregistrée dans l'historique avec un statut.

