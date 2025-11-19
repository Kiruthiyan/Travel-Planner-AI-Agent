import streamlit as st
import os
import traceback
from datetime import datetime
from agents.researcher import ResearcherAgent
from agents.planner import PlannerAgent
from agents.hotel_finder import HotelFinderAgent
from agno.models.google import Gemini
from concurrent.futures import ThreadPoolExecutor

# ---------- ENV ----------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not GEMINI_API_KEY:
    st.error("❌ GEMINI_API_KEY missing!")
    st.stop()
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
MODEL_ID = "models/gemini-pro-latest"

# ---------- UI ----------
st.set_page_config(page_title="🌍 AI Travel Planner", layout="wide")
st.title("✈️ AI-Powered Travel Planner")

source = st.text_input("Departure City (IATA Code):", "BOM")
destination = st.text_input("Destination (IATA Code):", "DEL")
num_days = st.slider("Trip Duration (days):", 1, 14, 5)
travel_theme = st.selectbox("Select Travel Theme:", ["Couple Getaway", "Family Vacation", "Adventure Trip", "Solo Exploration"])
activity_preferences = st.text_area("Favorite activities (comma separated):", "beach, sightseeing, food")
departure_date = st.date_input("Departure Date")
return_date = st.date_input("Return Date")
budget = st.sidebar.radio("Budget:", ["Economy", "Standard", "Luxury"])
flight_class = st.sidebar.radio("Flight Class:", ["Economy", "Business"])
hotel_rating = st.sidebar.selectbox("Hotel Rating:", ["Any", "3⭐", "4⭐", "5⭐"])

# ---------- SESSION MEMORY ----------
if "user_session" not in st.session_state:
    st.session_state.user_session = {}

st.session_state.user_session.update({
    "source": source,
    "destination": destination,
    "num_days": num_days,
    "travel_theme": travel_theme,
    "activity_preferences": activity_preferences,
    "departure_date": str(departure_date),
    "return_date": str(return_date),
    "budget": budget,
    "flight_class": flight_class,
    "hotel_rating": hotel_rating
})

# ---------- AGENT SETUP ----------
researcher = ResearcherAgent(model=Gemini(id=MODEL_ID))
hotel_finder = HotelFinderAgent(model=Gemini(id=MODEL_ID))
planner = PlannerAgent(model=Gemini(id=MODEL_ID))

# ---------- HELPER ----------
def format_datetime(dt):
    return datetime.strptime(str(dt), "%Y-%m-%d").strftime("%b %d, %Y")

def log_agent(name, message):
    st.text(f"[{name}] {message}")  # Streamlit logging
    # Optionally save to file
    with open("logs/agent_logs.txt", "a") as f:
        f.write(f"[{name}] {message}\n")

# ---------- GENERATE TRAVEL PLAN ----------
if st.button("Generate Travel Plan"):
    st.info("Contacting Gemini AI agents...")
    try:
        # Run Researcher & HotelFinder in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_research = executor.submit(lambda: researcher.run(
                f"Research top attractions, culture, climate, and safety tips for {destination}.",
                stream=False
            ))
            log_agent("Researcher", "Submitted task...")

            future_hotel = executor.submit(lambda: hotel_finder.run(
                f"Find best hotels and restaurants for {travel_theme} trip in {destination} with budget {budget} and hotel rating {hotel_rating}.",
                stream=False
            ))
            log_agent("HotelFinder", "Submitted task...")

            research_results = future_research.result()
            log_agent("Researcher", "Completed research.")

            hotel_results = future_hotel.result()
            log_agent("HotelFinder", "Completed hotel search.")

        # Planner runs after both complete (A2A protocol)
        planning_prompt = (
            f"Create a {num_days}-day itinerary for a {travel_theme} trip from {source} to {destination} "
            f"({format_datetime(departure_date)} to {format_datetime(return_date)}). "
            f"Activities: {activity_preferences}. Budget: {budget}. Flight Class: {flight_class}. "
            f"Include flights, hotels, restaurants, and daily schedule. "
            f"Research info: {research_results.content}. Hotels info: {hotel_results.content}."
        )
        itinerary = planner.run(planning_prompt, stream=False)
        log_agent("Planner", "Itinerary generated.")

        # ---------- DISPLAY ----------
        st.subheader("🗺️ Destination Research")
        st.write(research_results.content)
        st.subheader("🏨 Hotels & Restaurants")
        st.write(hotel_results.content)
        st.subheader("🗓️ Personalized Itinerary")
        st.write(itinerary.content)
        st.success("✅ Travel plan generated successfully!")

    except Exception as e:
        st.error("❌ Error generating travel plan. Check GEMINI_API_KEY and Model ID.")
        st.write(traceback.format_exc())
