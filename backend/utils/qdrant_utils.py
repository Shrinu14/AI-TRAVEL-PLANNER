import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from backend.utils.logger import logger

# Environment-based collection name and default vector size
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "places")

# Global client instance
_qdrant_client: QdrantClient = None


def get_qdrant_client() -> QdrantClient:
    """
    Get or initialize a singleton Qdrant client.
    """
    global _qdrant_client
    if _qdrant_client is None:
        host = os.getenv("QDRANT_HOST", "localhost")
        port = int(os.getenv("QDRANT_PORT", 6333))
        try:
            _qdrant_client = QdrantClient(
                host=host,
                port=port,
                prefer_grpc=False,
                timeout=30,
                https=False
            )
            logger.info(f"Connected to Qdrant at {host}:{port}")
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {e}")
            raise
    return _qdrant_client


def setup_schema(vector_size: int = 1536) -> None:
    """
    Sets up a Qdrant collection with the specified vector size and cosine distance metric.
    If the collection already exists, it logs and does nothing.

    Args:
        vector_size (int): Dimensionality of the vector embeddings.

    Raises:
        Exception: If Qdrant setup fails.
    """
    if not isinstance(vector_size, int):
        raise ValueError(f"vector_size must be an integer, got {type(vector_size)}")

    try:
        client = get_qdrant_client()

        collections = client.get_collections().collections
        existing_collections = [col.name for col in collections]

        if COLLECTION_NAME not in existing_collections:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            logger.info(f"Created collection '{COLLECTION_NAME}' in Qdrant.")
        else:
            logger.info(f"Collection '{COLLECTION_NAME}' already exists.")
    except Exception as e:
        logger.error(f"Failed to set up Qdrant schema: {e}")
        raise
