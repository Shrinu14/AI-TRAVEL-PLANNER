import logging
from sentence_transformers import SentenceTransformer
from backend.llm.ollama_llm import generate_response
from backend.utils.qdrant_utils import get_qdrant_client, COLLECTION_NAME

# Logger setup
logger = logging.getLogger(__name__)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_relevant_docs(question: str, top_k: int = 5) -> str:
    """
    Retrieve top_k relevant place names from Qdrant based on the query embedding.
    """
    try:
        vector = embedding_model.encode(question).tolist()

        # Previously referenced an undefined `qdrant_client` name (only
        # `get_qdrant_client` was imported), which raised a NameError on
        # every call. Get the client instance explicitly.
        client = get_qdrant_client()
        search_result = client.search(
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
        logger.error(f"Retrieval failed from Qdrant: {e}")
        return ""


def generate_rag_answer(query: str, context: str = None) -> str:
    """
    Generate a RAG-style answer using retrieved documents from Qdrant.

    `context` is optional: routes/rag_chat.py already retrieves the context
    itself and passes it in (the previous signature only accepted `query`,
    so that call raised "takes 1 positional argument but 2 were given" on
    every /rag-chat request). If context isn't supplied, it's retrieved
    here directly so the function still works standalone.
    """
    if context is None:
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
