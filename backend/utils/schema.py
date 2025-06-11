from pydantic import BaseModel, Field
from typing import List, Optional


class ItineraryRequest(BaseModel):
    user_id: str = Field(..., description="Unique identifier for the user", example="user_123")
    destination: str = Field(..., min_length=2, description="Travel destination", example="Paris")
    days: int = Field(..., gt=0, le=30, description="Number of days for the trip (1 to 30)", example=7)
    preferences: List[str] = Field(
        ..., 
        description="User's travel preferences (e.g., beaches, museums, adventure)", 
        min_items=1,
        example=["beaches", "food", "culture"]
    )
    budget: Optional[float] = Field(
        None, 
        gt=0, 
        description="Optional budget for the trip in USD", 
        example=1500.0
    )
    travel_month: Optional[str] = Field(
        None, 
        description="Preferred month for travel (e.g., June, December)", 
        example="December"
    )
