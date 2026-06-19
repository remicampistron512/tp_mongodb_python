from datetime import datetime
from decimal import Decimal

from .mongo_connection import MongoConnection
from models.account import Account
from models.deposit import Deposit
from models.operation_status import OperationStatus
from models.transfer import Transfer
from models.withdrawal import Withdrawal


class OperationDao:
    def __init__(self):
        self.collection = MongoConnection.operations
        self.accounts_collection = MongoConnection.accounts

    def create_deposit(self, account, amount):
        amount = Decimal(amount)
        new_balance = account.balance + amount
        operation_date = datetime.now()

        self.accounts_collection.update_one(
            {"account_number": account.account_number},
            {"$set": {"balance": str(new_balance)}}
        )

        operation_doc = {
            "type": "DEPOSIT",
            "account_number": account.account_number,
            "amount": str(amount),
            "status": OperationStatus.COMPLETED.value,
            "date": operation_date,
        }

        self.collection.insert_one(operation_doc)

        return Deposit(
            amount=amount,
            status=OperationStatus.COMPLETED,
            date=operation_date,
        )

    def create_withdrawal(self, account, amount):
        amount = Decimal(amount)
        operation_date = datetime.now()

        new_balance = account.balance - amount

        if new_balance < -account.overdraft_limit:
            status = OperationStatus.FAILED
        else:
            status = OperationStatus.COMPLETED

            self.accounts_collection.update_one(
                {"account_number": account.account_number},
                {"$set": {"balance": str(new_balance)}}
            )

        operation_doc = {
            "type": "WITHDRAWAL",
            "account_number": account.account_number,
            "amount": str(amount),
            "status": status.value,
            "date": operation_date,
        }

        self.collection.insert_one(operation_doc)

        return Withdrawal(
            amount=amount,
            status=status,
            date=operation_date,
        )

    def create_transfer(self, source_account, target_account, amount):
        amount = Decimal(amount)
        operation_date = datetime.now()

        new_source_balance = source_account.balance - amount
        new_target_balance = target_account.balance + amount

        if new_source_balance < -source_account.overdraft_limit:
            status = OperationStatus.FAILED
        else:
            status = OperationStatus.COMPLETED

            self.accounts_collection.update_one(
                {"account_number": source_account.account_number},
                {"$set": {"balance": str(new_source_balance)}}
            )

            self.accounts_collection.update_one(
                {"account_number": target_account.account_number},
                {"$set": {"balance": str(new_target_balance)}}
            )

        operation_doc = {
            "type": "TRANSFER",
            "account_number": source_account.account_number,
            "target_account_number": target_account.account_number,
            "amount": str(amount),
            "status": status.value,
            "date": operation_date,
        }

        self.collection.insert_one(operation_doc)

        return Transfer(
            amount=amount,
            status=status,
            date=operation_date,
            target=target_account,
        )

    def find_by_account(self, account):
        operation_docs = self.collection.find({
            "$or": [
                {"account_number": account.account_number},
                {"target_account_number": account.account_number},
            ]
        })

        operations = []

        for operation_doc in operation_docs:
            operations.append(self._document_to_operation(operation_doc))

        return operations

    def find_all(self):
        operation_docs = self.collection.find()
        operations = []

        for operation_doc in operation_docs:
            operations.append(self._document_to_operation(operation_doc))

        return operations

    def update(self, operation):
        return self.collection.update_one(
            {
                "amount": str(operation.amount),
                "date": operation.date,
            },
            {
                "$set": {
                    "status": operation.status.value,
                }
            }
        )

    def delete(self, operation):
        return self.collection.delete_one({
            "amount": str(operation.amount),
            "date": operation.date,
        })

    def delete_all(self) -> None:
        self.collection.delete_many({})

    def _document_to_operation(self, operation_doc):
        operation_type = operation_doc["type"]
        amount = Decimal(operation_doc["amount"])
        status = OperationStatus(operation_doc["status"])
        date = operation_doc["date"]

        if operation_type == "DEPOSIT":
            return Deposit(
                amount=amount,
                status=status,
                date=date,
            )

        if operation_type == "WITHDRAWAL":
            return Withdrawal(
                amount=amount,
                status=status,
                date=date,
            )

        if operation_type == "TRANSFER":
            target_account = self._find_account_by_number(
                operation_doc["target_account_number"]
            )

            return Transfer(
                amount=amount,
                status=status,
                date=date,
                target=target_account,
            )

        return None

    def _find_account_by_number(self, account_number: str):
        account_doc = self.accounts_collection.find_one({
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
