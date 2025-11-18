import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from config import config


class SecurityManager:
    @staticmethod
    def hash_password(password: str) -> str:
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)

    @staticmethod
    def generate_token(user_id: str, email: str) -> str:
        payload = {
            'user_id': str(user_id),
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=config.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        
        token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
        return token

    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token has expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    @staticmethod
    def extract_user_id_from_token(token: str) -> Optional[str]:
        payload = SecurityManager.verify_token(token)
        if payload:
            return payload.get('user_id')
        return None


# Convenience functions
def hash_password(password: str) -> str:
    return SecurityManager.hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return SecurityManager.verify_password(password, hashed_password)


def generate_token(user_id: str, email: str) -> str:
    return SecurityManager.generate_token(user_id, email)


def verify_token(token: str) -> Optional[Dict]:
    """Verify JWT token"""
    return SecurityManager.verify_token(token)
