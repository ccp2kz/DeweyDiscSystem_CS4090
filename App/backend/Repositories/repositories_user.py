from typing import Optional, List
from pymongo.database import Database
from bson import ObjectId

from repositories_base import BaseRepository
from models_user import User


class UserRepository(BaseRepository):
    def __init__(self, database: Database):
        super().__init__(database, 'users')
        self._ensure_indexes()

    def _ensure_indexes(self):
        # Unique index on email
        self.collection.create_index('email', unique=True)
        # Unique index on username
        self.collection.create_index('username', unique=True)
        # Index on last_login for analytics
        self.collection.create_index('last_login')

    def find_by_email(self, email: str) -> Optional[User]:
        user_data = self.find_one_by_query({'email': email})
        if user_data:
            return User.from_dict(user_data)
        return None

    def find_by_username(self, username: str) -> Optional[User]:
        user_data = self.find_one_by_query({'username': username})
        if user_data:
            return User.from_dict(user_data)
        return None

    def email_exists(self, email: str) -> bool:
        return self.find_one_by_query({'email': email}) is not None

    def username_exists(self, username: str) -> bool:
        return self.find_one_by_query({'username': username}) is not None

    def create_user(self, user: User) -> str:
        # Check for existing email
        if self.email_exists(user.email):
            raise ValueError(f"Email {user.email} is already registered")
        
        # Check for existing username
        if self.username_exists(user.username):
            raise ValueError(f"Username {user.username} is already taken")
        
        # Insert user
        user_dict = user.to_dict()
        user_id = self.insert(user_dict)
        return user_id

    def update_user(self, user_id: str, user: User) -> bool:
        user_dict = user.to_dict()
        # Remove _id from updates
        user_dict.pop('_id', None)
        return self.update(user_id, user_dict)

    def update_last_login(self, user_id: str) -> bool:
        from datetime import datetime
        return self.update(user_id, {'last_login': datetime.utcnow()})

    def update_skill_level(self, user_id: str, skill_level: str) -> bool:
        valid_levels = ['beginner', 'intermediate', 'advanced', 'pro']
        if skill_level not in valid_levels:
            raise ValueError(f"Invalid skill level. Must be one of: {valid_levels}")
        
        return self.update(user_id, {'skill_level': skill_level})

    def get_users_by_skill_level(self, skill_level: str) -> List[User]:
        users_data = self.find_by_query({'skill_level': skill_level})
        return [User.from_dict(data) for data in users_data]

    def get_active_users(self, days: int = 30) -> List[User]:
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        query = {
            'last_login': {'$gte': cutoff_date}
        }
        
        users_data = self.find_by_query(query)
        return [User.from_dict(data) for data in users_data]

    def search_users(self, search_term: str) -> List[User]:
        query = {
            '$or': [
                {'first_name': {'$regex': search_term, '$options': 'i'}},
                {'last_name': {'$regex': search_term, '$options': 'i'}},
                {'username': {'$regex': search_term, '$options': 'i'}}
            ]
        }
        
        users_data = self.find_by_query(query)
        return [User.from_dict(data) for data in users_data]

    def delete_user(self, user_id: str) -> bool:
        return self.delete(user_id)

    def get_user_count(self) -> int:
        return self.count()

    def get_user_count_by_skill(self) -> dict:
        pipeline = [
            {
                '$group': {
                    '_id': '$skill_level',
                    'count': {'$sum': 1}
                }
            }
        ]
        
        result = self.collection.aggregate(pipeline)
        return {doc['_id']: doc['count'] for doc in result}

    def __repr__(self):
        return f"<UserRepository(collection=users, count={self.get_user_count()})>"
