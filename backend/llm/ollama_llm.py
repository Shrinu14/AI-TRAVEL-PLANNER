import subprocess
import os

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

def generate_response(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode(),
            capture_output=True,
            timeout=60,
        )
        return result.stdout.decode().strip()
    except Exception as e:
        return f"Error: {e}"
