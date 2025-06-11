from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    user_id: str
    name: Optional[str] = None
    email: Optional[str] = None

class Place(BaseModel):
    name: str
    type: str  # 'hotel', 'restaurant', 'tourist_spot'
    description: Optional[str] = None
    coordinates: Optional[dict] = None

class Itinerary(BaseModel):
    user_id: str
    destination: str
    days: int
    preferences: Optional[List[str]] = []
    itinerary: List[dict]  # day-wise plan
    created_at: datetime = Field(default_factory=datetime.utcnow)
