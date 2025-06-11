from sentence_transformers import SentenceTransformer
from backend.utils.logger import logger

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    logger.info(f"Generating embedding for query: '{text}'")
    try:
        return model.encode(text).tolist()
    except Exception as e:
        logger.error(f"❌ Embedding failed for text '{text}': {e}")
        return []
