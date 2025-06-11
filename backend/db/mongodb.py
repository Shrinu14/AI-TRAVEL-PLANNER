import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
from pymongo.errors import ConnectionFailure

# Load environment variables from .env
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Get MongoDB URI and database name from environment
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

# Validate environment variables
if not MONGO_URI:
    raise EnvironmentError("MONGO_URI is not set in .env")

if not MONGO_DB:
    raise EnvironmentError("MONGO_DB is not set in .env")

try:
    # Initialize MongoDB client and database
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5 sec timeout
    # Trigger server selection to test connection
    client.admin.command('ping')
    print("Connected to MongoDB successfully.")
    
    db = client[MONGO_DB]

    # Define your collections
    users_collection = db["users"]
    itineraries_collection = db["itineraries"]

except ConnectionFailure as e:
    raise ConnectionError(f"Could not connect to MongoDB: {e}")
