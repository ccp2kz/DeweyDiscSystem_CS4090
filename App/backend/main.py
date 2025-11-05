from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Dewey Disc System API")

# Data Models
class User(BaseModel):
    id: int
    username: str
    email: str
    password: str

class Disc(BaseModel):
    id: int
    name: str
    speed: float
    glide: float
    turn: float
    fade: float

class Bag(BaseModel):
    user_id: int
    discs: List[Disc] = []

class RecommendationRequest(BaseModel):
    user_id: int
    distance_to_pin: float
    wind_speed: float
    wind_direction: str
    obstacles: Optional[str] = None

# Mock Data
users = []
bags = []
discs = [
    Disc(id=1, name="Innova Destroyer", speed=12, glide=5, turn=-1, fade=3),
    Disc(id=2, name="Discraft Buzzz", speed=5, glide=4, turn=-1, fade=1),
    Disc(id=3, name="Innova Aviar", speed=3, glide=3, turn=0, fade=1)
]

# Endpoints
@app.post("/register")
def register_user(user: User):
    for u in users:
        if u.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered.")
    users.append(user)
    return {"message": "User registered successfully."}

@app.post("/bag/add")
def add_to_bag(bag: Bag):
    bags.append(bag)
    return {"message": f"Added {len(bag.discs)} discs to user {bag.user_id}'s bag."}

@app.post("/recommend")
def recommend_disc(request: RecommendationRequest):
    # Placeholder logic
    if request.distance_to_pin > 200:
        disc = discs[0]  # Distance driver
    elif 80 < request.distance_to_pin <= 200:
        disc = discs[1]  # Midrange
    else:
        disc = discs[2]  # Putter

    return {
        "recommended_disc": disc.name,
        "reasoning": f"Distance of {request.distance_to_pin} ft and wind speed {request.wind_speed} mph."
    }
