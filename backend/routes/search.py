from fastapi import APIRouter, Query, HTTPException
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter, SearchParams
from backend.utils.qdrant_utils import get_qdrant_client, COLLECTION_NAME
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Load embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

@router.get("/search-places")
def search_places(query: str = Query(..., min_length=3), top_k: int = 5):
    try:
        # 1. Get vector embedding of the query
        vector = embedding_model.encode(query).tolist()

        # 2. Perform semantic search in Qdrant
        client = get_qdrant_client()
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=top_k,
            search_params=SearchParams(hnsw_ef=128, exact=False),
        )

        if not search_results:
            logger.info(f"🔍 No results found for query: {query}")
            return {"query": query, "results": []}

        places = [hit.payload["place_name"] for hit in search_results]

        return {
            "query": query,
            "results": places
        }

    except Exception as e:
        logger.error(f"❌ Search failed for query '{query}': {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
