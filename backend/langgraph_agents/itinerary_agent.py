from backend.llm.ollama_llm import generate_response

def generate_itinerary(destination: str, days: int, preferences: list):
    prompt = (
        f"Plan a {days}-day travel itinerary to {destination} for someone who enjoys "
        f"{', '.join(preferences)}. Provide day-wise plan with places to visit, activities, and local food."
    )
    return generate_response(prompt)
