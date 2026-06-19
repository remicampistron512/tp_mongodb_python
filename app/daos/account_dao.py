from decimal import Decimal

from .mongo_connection import MongoConnection
from models.account import Account


class AccountDao:
    def __init__(self):
        self.collection = MongoConnection.accounts

    def create(
            self,
            customer,
            account_number: str,
            overdraft_limit,
            daily_withdrawal_limit,
    ):
        data_dict = {
            "customerId": customer.id,
            "account_number": account_number,
            "balance": "0",
            "overdraft_limit": str(overdraft_limit),
            "daily_withdrawal_limit": str(daily_withdrawal_limit),
        }

        self.collection.insert_one(data_dict)

    def find_by_account_number(self, account_number: str):
        account_doc = self.collection.find_one({
            "account_number": account_number
        })

        if account_doc is None:
            return None

        return Account(
            account_number=account_doc["account_number"],
            balance=Decimal(account_doc["balance"]),
            overdraft_limit=Decimal(account_doc["overdraft_limit"]),
            daily_withdrawal_limit=Decimal(account_doc["daily_withdrawal_limit"]),
        )

    def find_by_customer(self, customer):
        account_docs = self.collection.find({
            "customerId": customer.id
        })

        accounts = []

        for account_doc in account_docs:
            account = Account(
                account_number=account_doc["account_number"],
                balance=Decimal(account_doc["balance"]),
                overdraft_limit=Decimal(account_doc["overdraft_limit"]),
                daily_withdrawal_limit=Decimal(account_doc["daily_withdrawal_limit"]),
            )

            accounts.append(account)

        return accounts

    def find_all(self):
        account_docs = self.collection.find()
        accounts = []

        for account_doc in account_docs:
            account = Account(
                account_number=account_doc["account_number"],
                balance=Decimal(account_doc["balance"]),
                overdraft_limit=Decimal(account_doc["overdraft_limit"]),
                daily_withdrawal_limit=Decimal(account_doc["daily_withdrawal_limit"]),
            )

            accounts.append(account)

        return accounts

    def update(self, old_account_number, account):
        self.collection.update_one(
            {"account_number": old_account_number},
            {
                "$set": {
                    "account_number": account.account_number,
                    "balance": str(account.balance),
                    "overdraft_limit": str(account.overdraft_limit),
                    "daily_withdrawal_limit": str(account.daily_withdrawal_limit),
                }
            }
        )

    def delete(self, account_number: str):
        self.collection.delete_one({
            "account_number": account_number
        })

    def delete_all(self) -> None:
        self.collection.delete_many({})