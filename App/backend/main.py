import json
import logging
from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from kafka import KafkaProducer

try:
    from backend_config import config
except ImportError:
    from config import config

from utils.database import db_connection
from models.disc import Disc as DiscModel

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DeweyAPI")

app = FastAPI()

# Kafka Setup
try:
    producer = KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    logger.info(f"Connected to Kafka at {config.KAFKA_BOOTSTRAP_SERVERS}")
except Exception as e:
    logger.warning(f"Kafka connection failed: {e}. Ensure Kafka is running for Part 6 features.")
    producer = None

# Data Models
class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    skill_level: str = "beginner"

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class Disc(BaseModel):
    id: str
    name: str
    manufacturer: str
    type: str
    speed: float
    glide: float
    turn: float
    fade: float
    stability: str

class Bag(BaseModel):
    user_id: str
    discs: List[Disc] = []

class Course(BaseModel):
    id: str
    name: str
    location: str

class RecommendationRequest(BaseModel):
    user_id: str
    course_id: str
    distance_to_pin: float
    wind_speed: float
    wind_direction: int
    strategy: str = "moderate"  # conservative, moderate, aggressive

# Mock Data (For validation)
# In a real CQRS app, the Command side would check a 'Write DB' (e.g., SQL)
courses = [
    Course(id="1", name="Water Works Park", location="Kansas City, MO"),
    Course(id="2", name="Maple Hill", location="Leicester, MA"),
    Course(id="3", name="La Mirada Regional Park", location="La Mirada, CA"),
]
# Mock Disc Catalog (Source of Truth for Disc properties)
discs_catalog = [
    Disc(id="1", name="Innova Destroyer", manufacturer="Innova", type="Distance Driver", speed=12, glide=5, turn=-1, fade=3, stability="Overstable"),
    Disc(id="2", name="Discraft Buzzz", manufacturer="Discraft", type="Midrange", speed=5, glide=4, turn=-1, fade=1, stability="Stable"),
    Disc(id="3", name="Innova Aviar", manufacturer="Innova", type="Putter", speed=3, glide=3, turn=0, fade=1, stability="Stable"),
]

# Routes
@app.post("/register")
def register_user(username: str, email: str, password: str):
    # CQRS: Command Side
    new_user_id = str(uuid4())
    
    # 1. Validate (Simulated)
    # 2. Create Event
    event = {
        "event_type": "UserRegistered",
        "payload": {
            "user_id": new_user_id,
            "username": username,
            "email": email,
            # In prod, hash password before sending or saving!
            "password_hash": "hashed_secret" 
        },
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # 3. Publish Event
    if producer:
        producer.send(config.KAFKA_TOPIC_BAG_UPDATES, event)
        
    return {"message": "Registration accepted. Processing in background.", "user_id": new_user_id}

@app.get("/courses")
def get_courses():
    return courses

@app.post("/bag/add")
def add_disc_to_bag(user_id: str, disc_id: str):
    """
    CQRS Command: Add Disc
    Does NOT update the DB directly. Sends an event to Kafka.
    """
    # 1. Validate Disc exists in catalog
    disc = next((d for d in discs_catalog if d.id == disc_id), None)
    if not disc:
        raise HTTPException(status_code=404, detail="Disc not found in catalog")

    # 2. Create Event
    event = {
        "event_type": "DiscAddedToBag",
        "payload": {
            "user_id": user_id,
            "disc_data": disc.dict() # Send full disc data to be stored in Read DB
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    # 3. Publish Event to Kafka
    if producer:
        producer.send(config.KAFKA_TOPIC_BAG_UPDATES, event)
        return {"status": "queued", "message": f"Request to add {disc.name} received."}
    else:
        return {"status": "error", "message": "Kafka Unavailable"}

@app.delete("/bag/remove")
def remove_disc_from_bag(user_id: str, disc_id: str):
    """
    CQRS Command: Remove Disc
    """
    event = {
        "event_type": "DiscRemovedFromBag",
        "payload": {
            "user_id": user_id,
            "disc_id": disc_id
        },
        "timestamp": datetime.utcnow().isoformat()
    }

    if producer:
        producer.send(config.KAFKA_TOPIC_BAG_UPDATES, event)
        return {"status": "queued", "message": "Request to remove disc received."}
    return {"status": "error", "message": "Kafka Unavailable"}

@app.get("/bag/view/{user_id}")
def view_bag(user_id: str):
    """
    CQRS Query: View Bag
    Reads from the MongoDB 'Read Model' which is populated by the Kafka Worker.
    """
    # 1. Connect to Read DB (MongoDB)
    db = db_connection.get_database()
    bags_collection = db['bags'] # The read-optimized collection
    
    # 2. Query
    user_bag = bags_collection.find_one({"user_id": user_id})
    
    if not user_bag:
        # Return empty bag if not found
        return []
        
    # 3. Return Data (Fast, no joins required)
    return user_bag.get("discs", [])

@app.post("/recommend")
def recommend_disc(req: RecommendationRequest):
    # Logic remains mostly the same, using in-memory mock for now or could query Read DB
    if req.distance_to_pin > 250:
        disc = discs_catalog[0]
    elif 80 < req.distance_to_pin <= 250:
        disc = discs_catalog[1]
    else:
        disc = discs_catalog[2]

    return {
        "recommended_disc": disc.name,
        "course": next((c.name for c in courses if c.id == req.course_id), "Unknown"),
        "reasoning": f"Distance {req.distance_to_pin}ft, Wind {req.wind_speed}mph, Course {req.course_id}",
    }
