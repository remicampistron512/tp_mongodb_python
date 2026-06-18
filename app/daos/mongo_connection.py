from pymongo import MongoClient  # type: ignore 


class MongoConnection:
    client = MongoClient("mongodb://localhost:27017/")
    database = client["bank_db"]

    customers = database["customers"]
    accounts = database["accounts"]
    operations = database["operations"]