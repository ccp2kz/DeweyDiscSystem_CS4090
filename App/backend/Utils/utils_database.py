"""
Database Connection Manager (Singleton Pattern)
Manages MongoDB connection with single instance
"""

from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
import logging

from config import config

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Singleton class for MongoDB database connection
    Ensures only one connection instance exists
    """
    _instance: Optional['DatabaseConnection'] = None
    _client: Optional[MongoClient] = None
    _database: Optional[Database] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._connect()

    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            self._client = MongoClient(config.MONGO_URI)
            self._database = self._client[config.DATABASE_NAME]
            
            # Test connection
            self._client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB: {config.DATABASE_NAME}")
            
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def get_database(self) -> Database:
        """Get the database instance"""
        if self._database is None:
            self._connect()
        return self._database

    def get_collection(self, collection_name: str):
        """Get a specific collection"""
        return self.get_database()[collection_name]

    def close(self):
        """Close the database connection"""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed")

    @classmethod
    def get_instance(cls) -> 'DatabaseConnection':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = DatabaseConnection()
        return cls._instance


# Global database instance
db_connection = DatabaseConnection.get_instance()
