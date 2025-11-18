from datetime import datetime
from typing import Optional, Dict
from bson import ObjectId


class User:
    def __init__(
        self,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str,
        skill_level: str = "beginner",
        username: Optional[str] = None,
        user_id: Optional[ObjectId] = None,
        throwing_style: str = "RHBH",
        max_distance: int = 250,
        created_at: Optional[datetime] = None,
        last_login: Optional[datetime] = None
    ):
        self._id = user_id
        self._email = email
        self._password_hash = password_hash
        self._first_name = first_name
        self._last_name = last_name
        self._skill_level = skill_level
        self._username = username or email.split('@')[0]
        self._throwing_style = throwing_style
        self._max_distance = max_distance
        self._created_at = created_at or datetime.utcnow()
        self._last_login = last_login
        self._settings = {
            'units': 'imperial',
            'wind_sensitivity': 'medium',
            'default_strategy': 'moderate'
        }

    #Getters
    @property
    def id(self) -> Optional[ObjectId]:
        return self._id

    @property
    def email(self) -> str:
        return self._email

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @property
    def username(self) -> str:
        return self._username

    @property
    def skill_level(self) -> str:
        return self._skill_level

    @property
    def throwing_style(self) -> str:
        return self._throwing_style

    @property
    def max_distance(self) -> int:
        return self._max_distance

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def last_login(self) -> Optional[datetime]:
        return self._last_login

    @property
    def settings(self) -> Dict:
        return self._settings.copy()

    # Setters (where appropriate)
    @email.setter
    def email(self, value: str):
        if '@' not in value:
            raise ValueError("Invalid email format")
        self._email = value

    @skill_level.setter
    def skill_level(self, value: str):
        valid_levels = ['beginner', 'intermediate', 'advanced', 'pro']
        if value not in valid_levels:
            raise ValueError(f"Skill level must be one of: {', '.join(valid_levels)}")
        self._skill_level = value

    @max_distance.setter
    def max_distance(self, value: int):
        if value < 0 or value > 1000:
            raise ValueError("Max distance must be between 0 and 1000 feet")
        self._max_distance = value

    # Business Logic Methods
    def update_last_login(self):
        self._last_login = datetime.utcnow()

    def update_setting(self, key: str, value):
        if key in self._settings:
            self._settings[key] = value
        else:
            raise KeyError(f"Invalid setting key: {key}")

    def can_throw_disc(self, disc_speed: float) -> bool:
        skill_speed_map = {
            'beginner': 7,
            'intermediate': 10,
            'advanced': 12,
            'pro': 14
        }
        max_speed = skill_speed_map.get(self._skill_level, 7)
        return disc_speed <= max_speed

    def to_dict(self) -> Dict:
        user_dict = {
            'email': self._email,
            'password_hash': self._password_hash,
            'first_name': self._first_name,
            'last_name': self._last_name,
            'username': self._username,
            'skill_level': self._skill_level,
            'throwing_style': self._throwing_style,
            'max_distance': self._max_distance,
            'created_at': self._created_at,
            'last_login': self._last_login,
            'settings': self._settings
        }
        
        if self._id:
            user_dict['_id'] = self._id
            
        return user_dict

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        return cls(
            user_id=data.get('_id'),
            email=data['email'],
            password_hash=data['password_hash'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data.get('username'),
            skill_level=data.get('skill_level', 'beginner'),
            throwing_style=data.get('throwing_style', 'RHBH'),
            max_distance=data.get('max_distance', 250),
            created_at=data.get('created_at'),
            last_login=data.get('last_login')
        )

    def __repr__(self):
        return f"<User(id={self._id}, email={self._email}, skill={self._skill_level})>"

    def __str__(self):
        return f"{self.full_name} ({self._email})"
