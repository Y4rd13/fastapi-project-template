from pymongo import MongoClient
from src.core.logger_func import logger

class MongoDBUtils:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBUtils, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, mongo_uri):
        if not self._initialized:
            logger.info(f"Connecting to MongoDB at {mongo_uri}")
            self.client = MongoClient(mongo_uri)
            logger.info("MongoDB connection established")
            self._initialized = True

    def get_client(self):
        """Return the MongoClient instance."""
        return self.client