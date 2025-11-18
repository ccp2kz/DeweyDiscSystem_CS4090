"""
User Model
Represents a user in the Dewey Disc System
"""

from datetime import datetime
from typing import Optional, Dict
from bson import ObjectId


class User:
    """
    User domain model with encapsulation
    Represents a disc golf player in the system
    """

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
        """
        Initialize User object
        
        Args:
            email: User's email address
            password_hash: Hashed password
            first_name: User's first name
            last_name: User's last name
            skill_level: beginner, intermediate, advanced, or pro
            username: Optional username
            user_id: MongoDB ObjectId (set by database)
            throwing_style: RHBH, LHBH, RHFH, or LHFH
            max_distance: Maximum throwing distance in feet
            created_at: Account creation timestamp
            last_login: Last login timestamp
        """
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

    # Getters (Properties)
    @property
    def id(self) -> Optional[ObjectId]:
        """Get user ID"""
        return self._id

    @property
    def email(self) -> str:
        """Get email"""
        return self._email

    @property
    def password_hash(self) -> str:
        """Get password hash"""
        return self._password_hash

    @property
    def first_name(self) -> str:
        """Get first name"""
        return self._first_name

    @property
    def last_name(self) -> str:
        """Get last name"""
        return self._last_name

    @property
    def full_name(self) -> str:
        """Get full name"""
        return f"{self._first_name} {self._last_name}"

    @property
    def username(self) -> str:
        """Get username"""
        return self._username

    @property
    def skill_level(self) -> str:
        """Get skill level"""
        return self._skill_level

    @property
    def throwing_style(self) -> str:
        """Get throwing style"""
        return self._throwing_style

    @property
    def max_distance(self) -> int:
        """Get max throwing distance"""
        return self._max_distance

    @property
    def created_at(self) -> datetime:
        """Get account creation date"""
        return self._created_at

    @property
    def last_login(self) -> Optional[datetime]:
        """Get last login date"""
        return self._last_login

    @property
    def settings(self) -> Dict:
        """Get user settings"""
        return self._settings.copy()

    # Setters (where appropriate)
    @email.setter
    def email(self, value: str):
        """Set email (with validation)"""
        if '@' not in value:
            raise ValueError("Invalid email format")
        self._email = value

    @skill_level.setter
    def skill_level(self, value: str):
        """Set skill level (with validation)"""
        valid_levels = ['beginner', 'intermediate', 'advanced', 'pro']
        if value not in valid_levels:
            raise ValueError(f"Skill level must be one of: {', '.join(valid_levels)}")
        self._skill_level = value

    @max_distance.setter
    def max_distance(self, value: int):
        """Set max distance (with validation)"""
        if value < 0 or value > 1000:
            raise ValueError("Max distance must be between 0 and 1000 feet")
        self._max_distance = value

    # Business Logic Methods
    def update_last_login(self):
        """Update last login timestamp"""
        self._last_login = datetime.utcnow()

    def update_setting(self, key: str, value):
        """
        Update a user setting
        
        Args:
            key: Setting key
            value: New setting value
        """
        if key in self._settings:
            self._settings[key] = value
        else:
            raise KeyError(f"Invalid setting key: {key}")

    def can_throw_disc(self, disc_speed: float) -> bool:
        """
        Check if user can effectively throw a disc based on speed
        
        Args:
            disc_speed: Speed rating of the disc
            
        Returns:
            True if user can throw the disc, False otherwise
        """
        skill_speed_map = {
            'beginner': 7,
            'intermediate': 10,
            'advanced': 12,
            'pro': 14
        }
        max_speed = skill_speed_map.get(self._skill_level, 7)
        return disc_speed <= max_speed

    def to_dict(self) -> Dict:
        """
        Convert User object to dictionary for database storage
        
        Returns:
            Dictionary representation of User
        """
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
        """
        Create User object from dictionary
        
        Args:
            data: Dictionary containing user data
            
        Returns:
            User object
        """
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
