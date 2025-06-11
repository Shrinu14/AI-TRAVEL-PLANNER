from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.routes import search, rag_chat, budget
from backend.utils.schema import ItineraryRequest
from backend.langgraph_agents.itinerary_agent import generate_itinerary
from backend.db.mongodb import itineraries_collection
from backend.db.models import Itinerary
from auth.firebase_auth import verify_token
from backend.utils.qdrant_utils import setup_schema
from sentence_transformers import SentenceTransformer
import logging
import os
import traceback
import requests

# ========== Load .env ==========
load_dotenv()

# ========== Logger Setup ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.main")

# ========== Initialize FastAPI ==========
app = FastAPI(title="AI Travel Planner API")

# ========== Load Global Embedding Model ==========
try:
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("✅ Loaded SentenceTransformer embedding model.")
except Exception as e:
    logger.error(f"❌ Failed to load embedding model: {e}")
    logger.debug(traceback.format_exc())

# ========== CORS Setup ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== Startup Event ==========
@app.on_event("startup")
def startup_event():
    try:
        logger.info("🚀 Starting FastAPI server...")
        setup_schema(vector_size=384)
        logger.info("✅ Qdrant schema setup completed.")
        logger.info("✅ MongoDB connection confirmed.")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        logger.debug(traceback.format_exc())
        raise e

# ========== Root Endpoint ==========
@app.get("/")
def root():
    logger.info("✅ Root endpoint hit.")
    return {"message": "Welcome to the AI Travel Planner backend!"}

# ========== Generate Itinerary ==========
@app.post("/generate-itinerary")
def generate_plan(req: ItineraryRequest):
    try:
        logger.info(f"🧭 Generating itinerary → Destination: {req.destination}, Days: {req.days}, Preferences: {req.preferences}")
        plan = generate_itinerary(req.destination, req.days, req.preferences)

        itinerary = Itinerary(
            user_id=req.user_id,
            destination=req.destination,
            days=req.days,
            preferences=req.preferences,
            itinerary=[
                {"day": i + 1, "plan": p.strip()}
                for i, p in enumerate(plan.split("Day"))
                if p.strip()
            ],
        )

        inserted = itineraries_collection.insert_one(itinerary.dict())
        if inserted.inserted_id:
            logger.info("✅ Itinerary saved to MongoDB.")
            return {"message": "Itinerary created", "data": itinerary.dict()}
        
        logger.error("❌ Failed to save itinerary to MongoDB.")
        raise HTTPException(status_code=500, detail="Could not save itinerary.")
    
    except Exception as e:
        logger.error(f"❌ Itinerary generation failed: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to generate itinerary.")

# ========== Weather Forecast ==========
@app.get("/weather")
def get_weather(destination: str = Query(..., description="City or destination")):
    try:
        WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
        if not WEATHER_API_KEY:
            raise HTTPException(status_code=500, detail="Weather API key not configured.")

        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={destination}"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"]["message"])

        return {
            "location": data["location"]["name"],
            "condition": data["current"]["condition"]["text"],
            "temp_c": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "wind_kph": data["current"]["wind_kph"],
            "icon": data["current"]["condition"]["icon"],
        }

    except Exception as e:
        logger.error(f"❌ Weather API error: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to fetch weather data.")

# ========== Firebase Auth-Protected User Data ==========
@app.get("/user/me")
def get_user_data(user=Depends(verify_token)):
    try:
        logger.info(f"🔐 Authenticated user: {user['email']}")
        return {"user": user["email"], "uid": user["uid"]}
    except Exception as e:
        logger.error(f"❌ Auth error: {e}")
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=401, detail="Unauthorized")

# ========== Include Modular Routers ==========
app.include_router(search.router)
app.include_router(rag_chat.router)
app.include_router(budget.router)
