from app.daos.account_dao import AccountDao
from app.daos.customer_dao import CustomerDao
from app.daos.operation_dao import OperationDao


class Bank:
    """
    Business facade for the bank application.

    This class does not access storage directly. It only delegates to DAO
    classes. The DAO methods are intentionally empty so you can implement
    the database logic yourself.
    """

    def __init__(
        self,
        customer_dao: CustomerDao | None = None,
        account_dao: AccountDao | None = None,
        operation_dao: OperationDao | None = None,
    ) -> None:
        self.customer_dao = customer_dao or CustomerDao()
        self.account_dao = account_dao or AccountDao()
        self.operation_dao = operation_dao or OperationDao()

    def create_customer(self, first_name: str, last_name: str, email: str):
        return self.customer_dao.create(first_name, last_name, email)

    def find_customer_by_email(self, email: str):
        return self.customer_dao.find_by_email(email)

    def list_customers(self):
        return self.customer_dao.find_all()

    def create_account(
        self,
        customer_email: str,
        account_number: str,
        overdraft_limit,
        daily_withdrawal_limit,
    ):
        customer = self.customer_dao.find_by_email(customer_email)
        return self.account_dao.create(
            customer,
            account_number,
            overdraft_limit,
            daily_withdrawal_limit,
        )

    def find_account(self, account_number: str):
        return self.account_dao.find_by_account_number(account_number)

    def list_customer_accounts(self, customer_email: str):
        customer = self.customer_dao.find_by_email(customer_email)
        return self.account_dao.find_by_customer(customer)

    def deposit(self, account_number: str, amount):
        account = self.account_dao.find_by_account_number(account_number)
        return self.operation_dao.create_deposit(account, amount)

    def withdraw(self, account_number: str, amount):
        account = self.account_dao.find_by_account_number(account_number)
        return self.operation_dao.create_withdrawal(account, amount)

    def transfer(self, source_account_number: str, target_account_number: str, amount):
        source_account = self.account_dao.find_by_account_number(source_account_number)
        target_account = self.account_dao.find_by_account_number(target_account_number)
        return self.operation_dao.create_transfer(source_account, target_account, amount)

    def get_account_history(self, account_number: str):
        account = self.account_dao.find_by_account_number(account_number)
        return self.operation_dao.find_by_account(account)

    def reset_data(self) -> None:
        self.operation_dao.delete_all()
        self.account_dao.delete_all()
        self.customer_dao.delete_all()

    def search_customer(self, search_term):
        return self.customer_dao.search_customer(search_term)

    def update_customer(self,customer):
        return self.customer_dao.update(customer)
    def delete_customer(self,email):
        return self.customer_dao.delete(email)