"""
Dewey Disc System - FastAPI Application
Enhanced with proper architecture, MongoDB, and OOP patterns
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from uuid import uuid4

# Import our new architecture components
from config import config
from utils.database import db_connection
from utils.security import hash_password, verify_password, generate_token, verify_token
from repositories.user_repository import UserRepository
from repositories.disc_repository import DiscRepository
from repositories.bag_repository import BagRepository
from services.authentication_service import AuthenticationService
from services.recommendation_engine import RecommendationEngine
from models.user import User as UserModel
from models.disc import Disc as DiscModel

# -----------------------
# Data Models
# -----------------------
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

# -----------------------
# Mock Databases
# -----------------------
users: List[User] = []
bags: List[Bag] = []
courses = [
    Course(id="1", name="Water Works Park", location="Kansas City, MO"),
    Course(id="2", name="Maple Hill", location="Leicester, MA"),
    Course(id="3", name="La Mirada Regional Park", location="La Mirada, CA"),
]
discs = [
    Disc(id="1", name="Innova Destroyer", speed=12, glide=5, turn=-1, fade=3),
    Disc(id="2", name="Discraft Buzzz", speed=5, glide=4, turn=-1, fade=1),
    Disc(id="3", name="Innova Aviar", speed=3, glide=3, turn=0, fade=1),
]

# -----------------------
# Routes
# -----------------------
@app.post("/register")
def register_user(username: str, email: str, password: str):
    for u in users:
        if u.email == email:
            raise HTTPException(status_code=400, detail="Email already registered.")
    new_user = User(id=str(uuid4()), username=username, email=email, password=password)
    users.append(new_user)
    bags.append(Bag(user_id=new_user.id, discs=[]))
    return {"message": "User registered successfully.", "user_id": new_user.id}

@app.get("/courses")
def get_courses():
    return courses

@app.post("/bag/add")
def add_disc_to_bag(user_id: str, disc_id: str):
    for bag in bags:
        if bag.user_id == user_id:
            disc = next((d for d in discs if d.id == disc_id), None)
            if not disc:
                raise HTTPException(status_code=404, detail="Disc not found")
            bag.discs.append(disc)
            return {"message": f"{disc.name} added to bag."}
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/bag/remove")
def remove_disc_from_bag(user_id: str, disc_id: str):
    for bag in bags:
        if bag.user_id == user_id:
            bag.discs = [d for d in bag.discs if d.id != disc_id]
            return {"message": "Disc removed from bag."}
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/bag/view/{user_id}")
def view_bag(user_id: str):
    for bag in bags:
        if bag.user_id == user_id:
            return bag.discs
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/recommend")
def recommend_disc(req: RecommendationRequest):
    # Placeholder logic
    if req.distance_to_pin > 250:
        disc = discs[0]
    elif 80 < req.distance_to_pin <= 250:
        disc = discs[1]
    else:
        disc = discs[2]

    return {
        "recommended_disc": disc.name,
        "course": next((c.name for c in courses if c.id == req.course_id), "Unknown"),
        "reasoning": f"Distance {req.distance_to_pin}ft, Wind {req.wind_speed}mph, Course {req.course_id}",
    }

