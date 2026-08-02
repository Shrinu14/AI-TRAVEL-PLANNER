import os
import logging

logger = logging.getLogger(__name__)

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FALLBACK_MESSAGE = (
    "AI-generated text is unavailable right now (no LLM backend is "
    "configured or reachable). Set OPENAI_API_KEY, or run Ollama and set "
    "OLLAMA_BASE_URL, to enable this feature."
)


def generate_response(prompt: str) -> str:
    """
    Generate a response from an LLM. Prefers OpenAI (if OPENAI_API_KEY is
    set), falls back to a local/reachable Ollama server over HTTP.

    Previously this shelled out to an `ollama` CLI binary via subprocess,
    which is never installed in the Docker image (docker/Dockerfile has no
    Ollama install step) -- every call failed with a FileNotFoundError in
    any deployed environment, silently swallowed and returned as
    "Error: ...", so /generate-itinerary and /rag-chat always returned
    garbage. Talking to Ollama's HTTP API (when available) instead of
    shelling out to a CLI, and preferring a cloud LLM, makes this actually
    work once deployed.
    """
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.warning(f"OpenAI generation failed: {e}")

    try:
        import requests

        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        logger.warning(f"Ollama generation failed: {e}")
        return FALLBACK_MESSAGE
