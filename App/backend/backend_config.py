import os
from typing import Optional
from dotenv import load_dotenv

#load environment variables
load_dotenv()


class Config:
    _instance: Optional['Config'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        # Database Configuration
        self.MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.DATABASE_NAME = os.getenv('DATABASE_NAME', 'dewey_disc_system')
        
        # Security Configuration
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
        self.JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
        
        # External API Configuration
        self.WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
        self.WEATHER_API_URL = os.getenv('WEATHER_API_URL', 'https://api.openweathermap.org/data/2.5')
        self.GPS_API_KEY = os.getenv('GPS_API_KEY', '')
        
        # Cache Configuration
        self.WEATHER_CACHE_DURATION_MINUTES = int(os.getenv('WEATHER_CACHE_DURATION', '15'))
        
        # Application Settings
        self.DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Disc Recommendation Settings
        self.DEFAULT_WIND_SENSITIVITY = os.getenv('DEFAULT_WIND_SENSITIVITY', 'medium')
        self.DEFAULT_STRATEGY = os.getenv('DEFAULT_STRATEGY', 'moderate')
        
        self._initialized = True

    @classmethod
    def get_instance(cls) -> 'Config':
        """Get the singleton instance"""
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

    def validate(self) -> bool:
        """Validate that required configuration is present"""
        required_fields = [
            'MONGO_URI',
            'DATABASE_NAME',
            'SECRET_KEY'
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Required configuration field '{field}' is missing")
        
        return True

    def __repr__(self):
        return f"<Config(database={self.DATABASE_NAME}, debug={self.DEBUG})>"


# Global config instance
config = Config.get_instance()
