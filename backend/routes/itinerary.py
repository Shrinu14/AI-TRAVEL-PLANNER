from fastapi import APIRouter, HTTPException, Query
from typing import List

router = APIRouter()

@router.get("/estimate")
def estimate_budget(duration: int = Query(...), budget: int = Query(...), destination: str = Query(...)):
    # Example logic
    cost_per_day = 3000
    total = duration * cost_per_day
    remaining = budget - total

    suggestions = []
    if remaining < 0:
        suggestions.append("Try shortening your trip or choosing cheaper hotels.")
    else:
        suggestions.append("You can explore premium stays or activities.")

    return {
        "estimated_cost": total,
        "remaining_budget": remaining,
        "suggestions": suggestions,
    }


@router.get("/flights")
def get_flights(destination: str, date: str):
    # Mock response; replace with real API integration
    return {
        "destination": destination,
        "date": date,
        "flights": [
            {"airline": "IndiGo", "price": 4500, "departure": "10:00", "arrival": "12:30"},
            {"airline": "Air India", "price": 5000, "departure": "14:00", "arrival": "16:30"},
        ]
    }

@router.get("/hotels")
def get_hotels(destination: str, checkin: str, nights: int):
    # Mock response; replace with real API integration
    return {
        "destination": destination,
        "hotels": [
            {"name": "Hotel Paradise", "price_per_night": 1500, "rating": 4.2},
            {"name": "Budget Inn", "price_per_night": 900, "rating": 3.8},
        ],
        "total_estimated_cost": nights * 1500
    }
