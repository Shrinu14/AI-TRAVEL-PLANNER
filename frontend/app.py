import os
import streamlit as st
import requests
from datetime import date as dt_date
from streamlit.components.v1 import iframe

# ======== PAGE CONFIG =========
st.set_page_config(page_title="AI Travel Planner", layout="centered")

# ======== TITLE =========
st.title("✈️ AI Travel Itinerary & Budget Planner")

# Backend URL is now configurable (was hardcoded to http://localhost:8000
# everywhere, which only worked if frontend and backend ran on the same
# machine -- broke as soon as either was deployed separately).
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# ======== FIREBASE LOGIN (for real use, switch to JS/Python integration) =========
# st.sidebar.title("🔐 Login")
# st.sidebar.info("Paste your Firebase ID token below if already authenticated.")
# firebase_id_token = st.sidebar.text_input("Firebase ID Token", type="password")
# headers = {"Authorization": f"Bearer {firebase_id_token}"} if firebase_id_token else {}

# `headers` was only ever defined inside the commented-out Firebase login
# block above, so every call to auth_get() raised NameError: headers is not
# defined. Define it unconditionally (empty when there's no token).
headers = {}

# ======== HELPER =========
def auth_get(url, params=None):
    try:
        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"❌ API Error: {e}")
        return None

# ======== GENERATE ITINERARY =========
with st.expander("🗺️ Generate AI Itinerary"):
    with st.form("generate_itinerary_form"):
        uid = st.text_input("User ID")
        destination = st.text_input("Destination")
        days = st.number_input("Days", min_value=1)
        preferences = st.multiselect("Preferences", ["beaches", "museums", "adventure", "food", "culture", "nature"])
        submitted = st.form_submit_button("Generate Itinerary")

    if submitted:
        if not destination or not preferences:
            st.warning("Please provide all inputs!")
        else:
            try:
                res = requests.post(f"{BACKEND_URL}/generate-itinerary", json={
                    "user_id": uid,
                    "destination": destination,
                    "days": days,
                    "preferences": preferences
                })
                res.raise_for_status()
                data = res.json()
                st.success("Generated Itinerary:")
                for item in data['data']['itinerary']:
                    st.markdown(f"**Day {item['day']}**: {item['plan']}")
            except Exception as e:
                st.error(f"Failed to generate itinerary: {e}")

# ======== BUDGET ESTIMATOR =========
with st.expander("🧮 Budget Estimator"):
    duration = st.number_input("Trip Duration (in days)", min_value=1)
    budget = st.number_input("Budget (in INR)", min_value=1000)
    destination = st.text_input("Destination for Budget", key="budget_dest")

    if st.button("Estimate Cost"):
        if not destination:
            st.warning("Please enter a destination.")
        else:
            result = auth_get(f"{BACKEND_URL}/estimate", params={
                "duration": duration,
                "budget": budget,
                "destination": destination
            })
            if result:
                st.success(f"Estimated Cost: ₹{result['estimated_cost']}")
                st.info(f"Remaining Budget: ₹{result['remaining_budget']}")
                st.write("Suggestions:", *result["suggestions"], sep="\n- ")

# ======== FLIGHTS =========
with st.expander("🛫 Best Flight Options"):
    flight_date = st.date_input("Flight Date", min_value=dt_date.today())
    if st.button("Fetch Flights"):
        result = auth_get(f"{BACKEND_URL}/flights", params={"destination": destination, "date": str(flight_date)})
        if result:
            for f in result["flights"]:
                st.write(f"✈️ {f['airline']} - ₹{f['price']} ({f['departure']} → {f['arrival']})")

# ======== HOTELS =========
with st.expander("🏨 Recommended Hotels"):
    nights = st.slider("Nights", 1, 10, 3)
    if st.button("Fetch Hotels"):
        result = auth_get(f"{BACKEND_URL}/hotels", params={
            "destination": destination,
            "checkin": str(flight_date),
            "nights": nights
        })
        if result:
            for h in result["hotels"]:
                st.write(f"🏨 {h['name']} - ₹{h['price_per_night']} per night ({h['rating']}⭐)")
            st.success(f"Total Estimated Cost: ₹{result['total_estimated_cost']}")

# ======== TRANSLATE ITINERARY =========
with st.expander("🌍 Translate Your Itinerary"):
    text = st.text_area("Enter itinerary text")
    lang = st.selectbox("Target Language", ["fr", "de", "es", "hi"])
    if st.button("Translate"):
        try:
            response = requests.post(f"{BACKEND_URL}/translate", json={"text": text, "target_lang": lang})
            response.raise_for_status()
            st.write("**Translated Text:**", response.json()["translated"])
        except Exception as e:
            st.error(f"Translation failed: {e}")

# ======== MAP & WEATHER =========
with st.expander("📍 Google Maps & Weather"):
    location = st.text_input("Enter place for map/weather info")
    if st.button("Show Map & Weather"):
        if location:
            st.markdown(f"**🗺️ Map for {location}:**")
            iframe(f"https://maps.google.com/maps?q={location}&output=embed", height=300)

            # The backend's /weather endpoint expects a "destination" query
            # param and returns {location, condition, temp_c, humidity,
            # wind_kph, icon} -- this used to send "location" (never bound,
            # so the request always failed validation) and then read
            # nonexistent "description"/"temperature" keys from the
            # response.
            weather_data = auth_get(f"{BACKEND_URL}/weather", params={"destination": location})
            if weather_data:
                st.write(f"🌤️ Weather: {weather_data['condition']}, 🌡️ {weather_data['temp_c']}°C")
        else:
            st.warning("Please enter a location.")

# ======== PROTECTED USER CHECK =========
# if firebase_id_token:
#     st.success("✅ Logged in")
#     result = auth_get(f"{BACKEND_URL}/user/me")
#     if result:
#         st.write(result)
# else:
#     st.warning("Please login using your Firebase ID token.")
