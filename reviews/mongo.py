from pymongo import MongoClient
from decouple import config

class Mongo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Mongo, cls).__new__(cls)
            cls._instance.client = MongoClient(config('MONGODB_URI'))
            cls._instance.db = cls._instance.client[config('DB_NAME')]
        return cls._instance

    @property
    def database(self):
        return self.db

# Usage
mongo_instance = Mongo()
db = mongo_instance.database
