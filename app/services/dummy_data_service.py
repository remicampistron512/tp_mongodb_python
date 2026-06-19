class DummyDataService:
    def __init__(self, bank):
        self.bank = bank

    def generate(self):
        self.bank.reset_data()

        customers = [
            ("John", "Doe", "john.doe@mail.com"),
            ("Jane", "Smith", "jane.smith@mail.com"),
            ("Alice", "Martin", "alice.martin@mail.com"),
            ("Bob", "Durand", "bob.durand@mail.com"),
            ("Claire", "Petit", "claire.petit@mail.com"),
        ]

        for first_name, last_name, email in customers:
            self.bank.create_customer(first_name, last_name, email)

            for i in range(1, 4):
                account_number = f"{email.split('@')[0]}-{i}"

                self.bank.create_account(
                    email,
                    account_number,
                    overdraft_limit=500,
                    daily_withdrawal_limit=1000,
                )

                self.bank.deposit(account_number, 1000)
                self.bank.withdraw(account_number, 100)
