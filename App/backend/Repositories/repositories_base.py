"""
Base Repository (Repository Pattern)
Abstract base class for all repositories
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.database import Database


class IRepository(ABC):
    """
    Abstract base repository interface
    Defines common CRUD operations for all repositories
    """

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Dict]:
        """
        Find entity by ID
        
        Args:
            entity_id: Entity ID (string or ObjectId)
            
        Returns:
            Entity dictionary or None if not found
        """
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, skip: int = 0) -> List[Dict]:
        """
        Find all entities with pagination
        
        Args:
            limit: Maximum number of results
            skip: Number of results to skip
            
        Returns:
            List of entity dictionaries
        """
        pass

    @abstractmethod
    def insert(self, entity: Dict) -> str:
        """
        Insert new entity
        
        Args:
            entity: Entity dictionary
            
        Returns:
            Inserted entity ID as string
        """
        pass

    @abstractmethod
    def update(self, entity_id: str, updates: Dict) -> bool:
        """
        Update existing entity
        
        Args:
            entity_id: Entity ID
            updates: Dictionary of fields to update
            
        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """
        Delete entity by ID
        
        Args:
            entity_id: Entity ID
            
        Returns:
            True if successful, False otherwise
        """
        pass


class BaseRepository(IRepository):
    """
    Base repository implementation for MongoDB
    Provides common functionality for all repositories
    """

    def __init__(self, database: Database, collection_name: str):
        """
        Initialize repository
        
        Args:
            database: MongoDB database instance
            collection_name: Name of the collection
        """
        self.db = database
        self.collection = database[collection_name]

    def find_by_id(self, entity_id: str) -> Optional[Dict]:
        """Find entity by ID"""
        try:
            obj_id = ObjectId(entity_id) if isinstance(entity_id, str) else entity_id
            return self.collection.find_one({'_id': obj_id})
        except Exception as e:
            print(f"Error finding entity by ID: {e}")
            return None

    def find_all(self, limit: int = 100, skip: int = 0) -> List[Dict]:
        """Find all entities with pagination"""
        try:
            cursor = self.collection.find().limit(limit).skip(skip)
            return list(cursor)
        except Exception as e:
            print(f"Error finding all entities: {e}")
            return []

    def find_by_query(self, query: Dict, limit: int = 100, skip: int = 0) -> List[Dict]:
        """
        Find entities matching a query
        
        Args:
            query: MongoDB query dictionary
            limit: Maximum results
            skip: Results to skip
            
        Returns:
            List of matching entities
        """
        try:
            cursor = self.collection.find(query).limit(limit).skip(skip)
            return list(cursor)
        except Exception as e:
            print(f"Error finding by query: {e}")
            return []

    def find_one_by_query(self, query: Dict) -> Optional[Dict]:
        """
        Find single entity matching query
        
        Args:
            query: MongoDB query dictionary
            
        Returns:
            Entity dictionary or None
        """
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print(f"Error finding one by query: {e}")
            return None

    def insert(self, entity: Dict) -> str:
        """Insert new entity"""
        try:
            result = self.collection.insert_one(entity)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting entity: {e}")
            raise

    def insert_many(self, entities: List[Dict]) -> List[str]:
        """
        Insert multiple entities
        
        Args:
            entities: List of entity dictionaries
            
        Returns:
            List of inserted IDs
        """
        try:
            result = self.collection.insert_many(entities)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            print(f"Error inserting multiple entities: {e}")
            raise

    def update(self, entity_id: str, updates: Dict) -> bool:
        """Update existing entity"""
        try:
            obj_id = ObjectId(entity_id) if isinstance(entity_id, str) else entity_id
            result = self.collection.update_one(
                {'_id': obj_id},
                {'$set': updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating entity: {e}")
            return False

    def update_many(self, query: Dict, updates: Dict) -> int:
        """
        Update multiple entities matching query
        
        Args:
            query: MongoDB query
            updates: Updates to apply
            
        Returns:
            Number of documents modified
        """
        try:
            result = self.collection.update_many(query, {'$set': updates})
            return result.modified_count
        except Exception as e:
            print(f"Error updating multiple entities: {e}")
            return 0

    def delete(self, entity_id: str) -> bool:
        """Delete entity by ID"""
        try:
            obj_id = ObjectId(entity_id) if isinstance(entity_id, str) else entity_id
            result = self.collection.delete_one({'_id': obj_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting entity: {e}")
            return False

    def delete_many(self, query: Dict) -> int:
        """
        Delete multiple entities matching query
        
        Args:
            query: MongoDB query
            
        Returns:
            Number of documents deleted
        """
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting multiple entities: {e}")
            return 0

    def count(self, query: Optional[Dict] = None) -> int:
        """
        Count documents
        
        Args:
            query: Optional query filter
            
        Returns:
            Document count
        """
        try:
            if query:
                return self.collection.count_documents(query)
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0

    def exists(self, entity_id: str) -> bool:
        """
        Check if entity exists
        
        Args:
            entity_id: Entity ID
            
        Returns:
            True if exists, False otherwise
        """
        return self.find_by_id(entity_id) is not None

    def __repr__(self):
        return f"<{self.__class__.__name__}(collection={self.collection.name})>"
