from .mongo_connection import MongoConnection
from models.customer import Customer  # type: ignore


class CustomerDao:
    def __init__(self):
        self.collection = MongoConnection.customers

    def create(self, first_name: str, last_name: str, email: str):
        return self.collection.insert_one({
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        })

    def find_by_email(self, email: str):
        email_query = {"email": email}
        customer_doc = self.collection.find_one(email_query)

        if customer_doc is None:
            return None

        return Customer(
            id=customer_doc["_id"],
            first_name=customer_doc["firstName"],
            last_name=customer_doc["lastName"],
            email=customer_doc["email"],
        )

    def find_all(self):
        customer_docs = self.collection.find()
        customers = []

        for customer_doc in customer_docs:
            customer = Customer(
                first_name=customer_doc["firstName"],
                last_name=customer_doc["lastName"],
                email=customer_doc["email"],
            )

            customers.append(customer)

        return customers

    def update(self, customer):
        return self.collection.update_one(
            {"email": customer.email},
            {
                "$set": {
                    "firstName": customer.first_name,
                    "lastName": customer.last_name,
                    "email": customer.email,
                }
            }
        )

    def delete(self, email: str):
        return self.collection.delete_one({
            "email": email
        })

    def delete_all(self) -> None:
        self.collection.delete_many({})