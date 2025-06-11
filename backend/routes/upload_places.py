from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.search.embedder import get_embedding
from utils.qdrant_utils import get_qdrant_client, COLLECTION_NAME
import uuid
import logging
from qdrant_client.models import PointStruct

router = APIRouter()
logger = logging.getLogger(__name__)

# Pydantic models
class Place(BaseModel):
    place_name: str

class PlaceList(BaseModel):
    places: List[Place]

@router.post("/upload-places")
def upload_places(data: PlaceList):
    if not data.places:
        raise HTTPException(status_code=400, detail="No places provided.")

    client = get_qdrant_client()
    points: List[PointStruct] = []

    for place in data.places:
        try:
            embedding = get_embedding(place.place_name)
        except Exception as e:
            logger.error(f"❌ Embedding failed for '{place.place_name}': {e}")
            raise HTTPException(status_code=500, detail=f"Embedding failed for: {place.place_name}")

        point_id = str(uuid.uuid4())
        payload = {"place_name": place.place_name}

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
        )

    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        logger.info(f"✅ Successfully uploaded {len(points)} places to Qdrant.")
        return {"message": "Places uploaded to Qdrant", "inserted_count": len(points)}
    except Exception as e:
        logger.error(f"❌ Failed to upload to Qdrant: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload data to Qdrant.")
