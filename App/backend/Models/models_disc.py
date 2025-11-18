from typing import Optional, Dict, List
from bson import ObjectId


class Disc:
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
        return self._avg_distance.get(skill_level, 0)

    def is_suitable_for_beginner(self) -> bool:
        return self._speed <= 7 and self._stability in ['stable', 'understable']

    def calculate_high_speed_stability(self) -> float:
        return self._turn

    def calculate_low_speed_stability(self) -> float:
        return self._fade

    def predict_flight_path(self, wind_speed: float = 0, wind_direction: int = 0) -> str:
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
        return {
            'speed_diff': self._speed - other_disc.speed,
            'glide_diff': self._glide - other_disc.glide,
            'turn_diff': self._turn - other_disc.turn,
            'fade_diff': self._fade - other_disc.fade,
            'more_stable': self._fade > other_disc.fade
        }

    def to_dict(self) -> Dict:
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
        if not isinstance(other, Disc):
            return False
        return self._name == other.name and self._manufacturer == other.manufacturer
