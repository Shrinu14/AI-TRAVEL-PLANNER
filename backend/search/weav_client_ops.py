from backend.utils.qdrant_utils import get_qdrant_client  # renamed utils
from search.embedder import get_embedding
from backend.utils.logger import logger
import uuid

COLLECTION_NAME = "places"  # collection name in Qdrant

def add_place(place_name: str):
    try:
        logger.info(f"Adding place: {place_name}")
        vector = get_embedding(place_name)
        client = get_qdrant_client()
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                {
                    "id": str(uuid.uuid4()),
                    "vector": vector,
                    "payload": {"place_name": place_name}
                }
            ]
        )
        logger.info(f"✅ Added place '{place_name}' to Qdrant.")
    except Exception as e:
        logger.error(f"❌ Failed to add place '{place_name}': {e}")


def search_places(query: str, top_k: int = 5):
    try:
        logger.info(f"Searching Qdrant for: '{query}' (top_k={top_k})")
        vector = get_embedding(query)
        client = get_qdrant_client()
        hits = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=top_k
        )
        results = [hit.payload["place_name"] for hit in hits]
        logger.info(f"✅ Found {len(results)} results for query '{query}'")
        return results
    except Exception as e:
        logger.error(f"❌ Search failed for query '{query}': {e}")
        return []
