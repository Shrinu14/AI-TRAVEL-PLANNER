# 🧭 AI Travel Planner

> A full-stack, AI-powered Travel Itinerary & Budget Planner built with Streamlit, FastAPI, Firebase, and advanced ML/LLM features.

Plan your entire trip — including budget, hotels, flights, itinerary, translation, route map, and weather — using a modern AI stack.

---

## 🌟 Features

- 🔐 **Firebase Auth** – Secure login with Google
- 🧮 **Budget Estimator** – Estimate trip cost and get savings tips
- ✈️ **Flight Search** – Real-time cheapest flight suggestions
- 🏨 **Hotel Recommender** – Hotel options with cost, rating, duration
- 🧠 **AI Itinerary Generator** – Personalized LLM-based travel plans
- 🌍 **Translate Itinerary** – Multilingual support for itinerary
- 📍 **Route Map & Weather** – Google Maps integration + Live Weather
- 📦 **MongoDB + Qdrant** – Store structured plans and semantic search

---

## ⚙️ Tech Stack

| Frontend   | Backend    | AI/NLP        | Storage         | Deployment |
|------------|------------|---------------|------------------|------------|
| Streamlit  | FastAPI    | LangGraph, Ollama, SentenceTransformers | MongoDB, Qdrant, MinIO | Docker, GitHub Actions |

---

## 🧱 Folder Structure

```bash
AI-Travel-Planner/
├── frontend/                 # Streamlit UI
│   ├── app.py               # Main UI logic
│   ├── Dockerfile
├── backend/
│   ├── main.py              # FastAPI entrypoint
│   ├── routes/              # All API routes
│   ├── db/                  # MongoDB connection & models
│   ├── langgraph_agents/    # LLM-based agents
│   ├── utils/               # Embedding, Qdrant, etc.
│   ├── Dockerfile
├── docker-compose.yml       # Full project orchestration
├── requirements.txt
├── README.md

---

## ✅ Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.10+
- Docker & Docker Compose
- Node.js (optional, if modifying Firebase)
- Firebase account (for Auth)
- Git

---

## ⚙️ Environment Setup

Create a `.env` file in the `backend/` directory with these keys:

```env
# backend/.env

MONGO_URI=mongodb://mongo-db:27017
QDRANT_HOST=http://qdrant:6333
OPENAI_API_KEY=your_openai_key_here
WEATHER_API_KEY=your_openweather_key
GOOGLE_MAPS_API_KEY=your_google_maps_key
FIREBASE_PROJECT_ID=your_firebase_project_id

---

## 📦 Local Installation (Alternative to Docker)

> Useful if you want to run frontend or backend individually

### 🔁 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload

### Frontend setup
cd frontend
pip install -r requirements.txt
streamlit run app.py

```markdown
---

## 🔭 Future Scope

- ✈️ Integrate real-time Flight & Hotel APIs (Skyscanner, Amadeus)
- 🧭 Add user location-based suggestions
- 🌍 Multi-user dashboard to manage itineraries
- 💬 Add chat interface with AI travel planner
- 📱 Mobile-friendly UI with React Native / Flutter frontend