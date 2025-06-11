from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from backend.utils.qdrant_utils import get_qdrant_client, COLLECTION_NAME
from qdrant_client.models import SearchParams
from backend.langgraph_agents.rag_agent import generate_rag_answer

router = APIRouter()

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
client = get_qdrant_client()

class RAGQuery(BaseModel):
    question: str

@router.post("/rag-chat")
def rag_chat(query: RAGQuery):
    try:
        # Step 1: Embed the question
        query_embedding = embedding_model.encode(query.question).tolist()

        # Step 2: Semantic search in Qdrant
        search_results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3,
            search_params=SearchParams(hnsw_ef=128, exact=False),
        )

        if not search_results:
            return {
                "question": query.question,
                "answer": "Sorry, I couldn't find relevant info.",
                "context": []
            }

        docs = [hit.payload["text"] for hit in search_results if "text" in hit.payload]

        # Step 3: RAG-style answer generation
        context = "\n".join(docs)
        answer = generate_rag_answer(query.question, context)

        return {
            "question": query.question,
            "answer": answer,
            "context": docs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Error: {str(e)}")
