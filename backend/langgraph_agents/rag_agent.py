import logging
from sentence_transformers import SentenceTransformer
from backend.llm.ollama_llm import generate_response
from backend.utils.qdrant_utils import get_qdrant_client  # properly initialized Qdrant client

from qdrant_client.http.models import SearchRequest, Filter, PointStruct, FieldCondition, MatchValue

# Logger setup
logger = logging.getLogger(__name__)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Qdrant collection name
COLLECTION_NAME = "places"

def retrieve_relevant_docs(question: str, top_k: int = 5) -> str:
    """
    Retrieve top_k relevant place names from Qdrant based on the query embedding.
    """
    try:
        vector = embedding_model.encode(question).tolist()

        search_result = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=vector,
            limit=top_k
        )

        docs = [hit.payload.get("place_name", "") for hit in search_result if hit.payload]
        
        if not docs:
            logger.info(f"No relevant documents found for query: {question}")
            return ""

        return "\n".join(docs)

    except Exception as e:
        logger.error(f"❌ Retrieval failed from Qdrant: {e}")
        return ""


def generate_rag_answer(query: str) -> str:
    """
    Generate a RAG-style answer using retrieved documents from Qdrant.
    """
    context = retrieve_relevant_docs(query)

    if not context:
        return "I'm sorry, I couldn't find relevant travel information for your query."

    prompt = (
        f"You are a helpful AI travel assistant.\n"
        f"Use the following information to answer the user's question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )

    return generate_response(prompt)
