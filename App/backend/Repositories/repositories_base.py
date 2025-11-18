from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from bson import ObjectId
from pymongo.database import Database


class IRepository(ABC):
    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Dict]:
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, skip: int = 0) -> List[Dict]:
        pass

    @abstractmethod
    def insert(self, entity: Dict) -> str:
        pass

    @abstractmethod
    def update(self, entity_id: str, updates: Dict) -> bool:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        pass


class BaseRepository(IRepository):
    def __init__(self, database: Database, collection_name: str):
        self.db = database
        self.collection = database[collection_name]

    def find_by_id(self, entity_id: str) -> Optional[Dict]:
        try:
            obj_id = ObjectId(entity_id) if isinstance(entity_id, str) else entity_id
            return self.collection.find_one({'_id': obj_id})
        except Exception as e:
            print(f"Error finding entity by ID: {e}")
            return None

    def find_all(self, limit: int = 100, skip: int = 0) -> List[Dict]:
        try:
            cursor = self.collection.find().limit(limit).skip(skip)
            return list(cursor)
        except Exception as e:
            print(f"Error finding all entities: {e}")
            return []

    def find_by_query(self, query: Dict, limit: int = 100, skip: int = 0) -> List[Dict]:
        try:
            cursor = self.collection.find(query).limit(limit).skip(skip)
            return list(cursor)
        except Exception as e:
            print(f"Error finding by query: {e}")
            return []

    def find_one_by_query(self, query: Dict) -> Optional[Dict]:
        try:
            return self.collection.find_one(query)
        except Exception as e:
            print(f"Error finding one by query: {e}")
            return None

    def insert(self, entity: Dict) -> str:
        try:
            result = self.collection.insert_one(entity)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting entity: {e}")
            raise

    def insert_many(self, entities: List[Dict]) -> List[str]:
        try:
            result = self.collection.insert_many(entities)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            print(f"Error inserting multiple entities: {e}")
            raise

    def update(self, entity_id: str, updates: Dict) -> bool:
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
        try:
            result = self.collection.update_many(query, {'$set': updates})
            return result.modified_count
        except Exception as e:
            print(f"Error updating multiple entities: {e}")
            return 0

    def delete(self, entity_id: str) -> bool:
        try:
            obj_id = ObjectId(entity_id) if isinstance(entity_id, str) else entity_id
            result = self.collection.delete_one({'_id': obj_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting entity: {e}")
            return False

    def delete_many(self, query: Dict) -> int:
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Error deleting multiple entities: {e}")
            return 0

    def count(self, query: Optional[Dict] = None) -> int:
        try:
            if query:
                return self.collection.count_documents(query)
            return self.collection.count_documents({})
        except Exception as e:
            print(f"Error counting documents: {e}")
            return 0

    def exists(self, entity_id: str) -> bool:
        return self.find_by_id(entity_id) is not None

    def __repr__(self):
        return f"<{self.__class__.__name__}(collection={self.collection.name})>"
