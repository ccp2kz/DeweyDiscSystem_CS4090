"""
Disc Model
Represents a disc golf disc in the system
"""

from typing import Optional, Dict, List
from bson import ObjectId


class Disc:
    """
    Disc domain model
    Represents a disc golf disc with flight characteristics
    """

    def __init__(
        self,
        name: str,
        manufacturer: str,
        disc_type: str,
        speed: float,
        glide: float,
        turn: float,
        fade: float,
        stability: str,
        disc_id: Optional[ObjectId] = None,
        plastic: Optional[str] = None,
        pdga_approved: bool = True,
        weight_range: Optional[Dict] = None,
        best_for: Optional[List[str]] = None,
        image_url: Optional[str] = None,
        avg_distance: Optional[Dict[str, int]] = None
    ):
        """
        Initialize Disc object
        
        Args:
            name: Disc name (e.g., "Buzzz")
            manufacturer: Manufacturer name (e.g., "Discraft")
            disc_type: putter, midrange, fairway_driver, distance_driver
            speed: Speed rating (1-14)
            glide: Glide rating (1-7)
            turn: Turn rating (-5 to 1)
            fade: Fade rating (0-5)
            stability: overstable, stable, or understable
            disc_id: MongoDB ObjectId
            plastic: Plastic type (e.g., "Star", "ESP")
            pdga_approved: PDGA approval status
            weight_range: Min/max weight dict
            best_for: List of use cases
            image_url: URL to disc image
            avg_distance: Average distances by skill level
        """
        self._id = disc_id
        self._name = name
        self._manufacturer = manufacturer
        self._disc_type = disc_type
        self._speed = speed
        self._glide = glide
        self._turn = turn
        self._fade = fade
        self._stability = stability
        self._plastic = plastic
        self._pdga_approved = pdga_approved
        self._weight_range = weight_range or {'min': 165, 'max': 175}
        self._best_for = best_for or []
        self._image_url = image_url
        self._avg_distance = avg_distance or {
            'beginner': int(speed * 35),
            'intermediate': int(speed * 45),
            'advanced': int(speed * 55),
            'pro': int(speed * 65)
        }

    # Getters (Properties)
    @property
    def id(self) -> Optional[ObjectId]:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def disc_type(self) -> str:
        return self._disc_type

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def glide(self) -> float:
        return self._glide

    @property
    def turn(self) -> float:
        return self._turn

    @property
    def fade(self) -> float:
        return self._fade

    @property
    def stability(self) -> str:
        return self._stability

    @property
    def plastic(self) -> Optional[str]:
        return self._plastic

    @property
    def flight_numbers(self) -> str:
        """Get flight numbers in standard format"""
        return f"{self._speed}/{self._glide}/{self._turn}/{self._fade}"

    @property
    def weight_range(self) -> Dict:
        return self._weight_range.copy()

    @property
    def best_for(self) -> List[str]:
        return self._best_for.copy()

    # Business Logic Methods
    def get_expected_distance(self, skill_level: str) -> int:
        """
        Get expected distance for a skill level
        
        Args:
            skill_level: beginner, intermediate, advanced, or pro
            
        Returns:
            Expected distance in feet
        """
        return self._avg_distance.get(skill_level, 0)

    def is_suitable_for_beginner(self) -> bool:
        """Check if disc is suitable for beginners"""
        return self._speed <= 7 and self._stability in ['stable', 'understable']

    def calculate_high_speed_stability(self) -> float:
        """
        Calculate high-speed stability number (HSS)
        Positive = overstable, Negative = understable
        
        Returns:
            HSS value
        """
        return self._turn

    def calculate_low_speed_stability(self) -> float:
        """
        Calculate low-speed stability number (LSS)
        Higher = more overstable
        
        Returns:
            LSS value
        """
        return self._fade

    def predict_flight_path(self, wind_speed: float = 0, wind_direction: int = 0) -> str:
        """
        Predict basic flight path description
        
        Args:
            wind_speed: Wind speed in mph
            wind_direction: Wind direction in degrees
            
        Returns:
            Flight path description
        """
        if self._stability == 'overstable':
            path = "Starts straight, fades hard left (RHBH)"
        elif self._stability == 'understable':
            path = "Turns right early, may flip (RHBH)"
        else:
            path = "Flies straight with gentle fade (RHBH)"
        
        if wind_speed > 10:
            path += f" - Adjust for {wind_speed}mph wind"
        
        return path

    def compare_to(self, other_disc: 'Disc') -> Dict:
        """
        Compare this disc to another disc
        
        Args:
            other_disc: Another Disc object
            
        Returns:
            Comparison dictionary
        """
        return {
            'speed_diff': self._speed - other_disc.speed,
            'glide_diff': self._glide - other_disc.glide,
            'turn_diff': self._turn - other_disc.turn,
            'fade_diff': self._fade - other_disc.fade,
            'more_stable': self._fade > other_disc.fade
        }

    def to_dict(self) -> Dict:
        """Convert Disc object to dictionary"""
        disc_dict = {
            'name': self._name,
            'manufacturer': self._manufacturer,
            'type': self._disc_type,
            'speed': self._speed,
            'glide': self._glide,
            'turn': self._turn,
            'fade': self._fade,
            'stability': self._stability,
            'plastic': self._plastic,
            'pdga_approved': self._pdga_approved,
            'weight_range': self._weight_range,
            'best_for': self._best_for,
            'image_url': self._image_url,
            'avg_distance': self._avg_distance
        }
        
        if self._id:
            disc_dict['_id'] = self._id
            
        return disc_dict

    @classmethod
    def from_dict(cls, data: Dict) -> 'Disc':
        """Create Disc object from dictionary"""
        return cls(
            disc_id=data.get('_id'),
            name=data['name'],
            manufacturer=data['manufacturer'],
            disc_type=data['type'],
            speed=data['speed'],
            glide=data['glide'],
            turn=data['turn'],
            fade=data['fade'],
            stability=data['stability'],
            plastic=data.get('plastic'),
            pdga_approved=data.get('pdga_approved', True),
            weight_range=data.get('weight_range'),
            best_for=data.get('best_for', []),
            image_url=data.get('image_url'),
            avg_distance=data.get('avg_distance')
        )

    def __repr__(self):
        return f"<Disc(name={self._name}, manufacturer={self._manufacturer}, {self.flight_numbers})>"

    def __str__(self):
        return f"{self._manufacturer} {self._name} [{self.flight_numbers}]"

    def __eq__(self, other):
        """Check disc equality based on name and manufacturer"""
        if not isinstance(other, Disc):
            return False
        return self._name == other.name and self._manufacturer == other.manufacturer
