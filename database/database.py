from config.logging_config import logger
from config.env_config import env
from config.db_config import MONGO_URI, MONGO_DB
from pymongo import MongoClient

class Database:
    def __init__(self, mongo_uri=MONGO_URI):
        client = MongoClient(mongo_uri)
        db = client[MONGO_DB]
        self.collections = {
            "transactions": db[f"transactions_{env.lower()}"],
            "users": db[f"users_{env.lower()}"],
            "categories": db[f"categories_{env.lower()}"],
        }

    def get_collection(self, collection_name):
        return self.collections[collection_name]