# app.py — LuxeTravel Ultimate (Dual Theme Edition)
import streamlit as st
import os
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from streamlit_lottie import st_lottie
from io import BytesIO
from fpdf import FPDF
from agno.models.google import Gemini

# --- MOCK IMPORTS FOR DEMO ---
# (Replace with your actual Agno imports when running locally)
from agno.models.google import Gemini
from agents.researcher import ResearcherAgent
from agents.planner import PlannerAgent
from agents.hotel_finder import HotelFinderAgent

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="LuxeTravel | AI Concierge",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- STATE MANAGEMENT (Theme) ----------
if 'theme' not in st.session_state:
    st.session_state.theme = 'Dark Mode'

# ---------- SIDEBAR (Theme Toggle) ----------
with st.sidebar:
    st.title("⚙️ Settings")
    st.session_state.theme = st.radio(
        "Choose Appearance:",
        ("Dark Mode", "Light Mode"),
        index=0 if st.session_state.theme == 'Dark Mode' else 1
    )
    st.markdown("---")
    st.markdown("**LuxeTravel AI**\nv2.0 Premium")

# ---------- ENV & KEYS ----------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "").strip()
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
MODEL_ID = "gemini-1.5-flash"

# ---------- DYNAMIC CSS (Based on Selection) ----------
# CSS Variables are used to switch colors dynamically
theme_css = ""

if st.session_state.theme == "Dark Mode":
    # --- DARK MODE STYLES ---
    theme_css = """
    :root {
        --bg-color: #050505;
        --bg-gradient: radial-gradient(circle at 50% 0%, #1a1a2e 0%, #000000 70%);
        --text-color: #ffffff; /* Pure White for better visibility */
        --sub-text-color: #cccccc;
        --card-bg: rgba(255, 255, 255, 0.05);
        --card-border: rgba(255, 215, 0, 0.15);
        --input-bg: rgba(255, 255, 255, 0.1);
        --input-text:  #000000;
        --gold-accent: #D4AF37;
    }
    """
else:
    # --- LIGHT MODE STYLES ---
    theme_css = """
    :root {
        --bg-color: #f4f4f9;
        --bg-gradient: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        --text-color: #000000; /* Deep Black for Light Mode */
        --sub-text-color: #333333;
        --card-bg: rgba(255, 255, 255, 0.85); /* Frosted glass white */
        --card-border: rgba(0, 0, 0, 0.05);
        --input-bg: #ffffff;
        --input-text: #000000;
        --gold-accent: #B8860B; /* Darker Gold for visibility on white */
    }
    """

# COMMON CSS (Applying the variables)
st.markdown(f"""
<style>
    {theme_css}
    
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    /* GLOBAL THEME APPLY */
    .stApp {{
        background-color: var(--bg-color);
        background-image: var(--bg-gradient);
        color: var(--text-color);
        font-family: 'Inter', sans-serif;
    }}

     /* SIDEBAR ADAPTATION */
    [data-testid="stSidebar"] {{
        background-color: var(--sidebar-bg);
        border-right: 1px solid var(--card-border);
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{
        color: var(--text-color) !important;
    }}

    /* HEADERS */
    h1, h2, h3 {{
        font-family: 'Playfair Display', serif;
        color: var(--gold-accent) !important;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-shadow: 0px 1px 2px rgba(0,0,0,0.1);
    }}
    
    /* TEXT CLARITY FIX */
    p, label, .stMarkdown {{
        color: var(--text-color) !important;
        font-weight: 500; /* Increased weight for visibility */
    }}

    /* GLASS CARDS */
    div.css-1r6slb0, div.stExpander, .glass-card {{
        background: var(--card-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        padding: 24px;
        margin-bottom: 20px;
    }}

    /* BUTTONS */
    div.stButton > button {{
        background: linear-gradient(135deg, #D4AF37 0%, #AA8A2E 100%);
        color: #000000 !important;
        font-weight: 700;
        border: none;
        padding: 0.6rem 2rem;
        border-radius: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }}
    div.stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(212, 175, 55, 0.6);
    }}

    /* INPUT FIELDS (Crucial for Light/Dark mode switching) */
    .stTextInput > div > div > input, 
    .stSelectbox > div > div > div, 
    .stDateInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 1px solid var(--gold-accent);
        border-radius: 8px;
    }}
    
    /* INPUT LABELS */
    .stTextInput label, .stSelectbox label, .stDateInput label {{
        color: var(--text-color) !important;
    }}

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px;
        background-color: transparent;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 0;
        color: var(--sub-text-color);
        font-family: 'Playfair Display', serif;
        font-size: 18px;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: var(--gold-accent);
        border-bottom: 2px solid var(--gold-accent);
    }}
    
    /* HELPER CLASSES */
    .sub-text {{ font-size: 15px; color: var(--sub-text-color) !important; margin-top: -15px; margin-bottom: 20px; }}
    
</style>
""", unsafe_allow_html=True)

# ---------- HELPER FUNCTIONS ----------
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        return r.json() if r.status_code == 200 else None
    except: return None

# ---------- HEADER SECTION ----------
col_logo, col_anim = st.columns([2, 1])

with col_logo:
    st.markdown(
        """
        <h1 style="
            font-family: 'Playfair Display', serif;
            font-size: 50px;
            font-weight: 700;
            color: var(--gold-accent);
            margin-bottom: -10px;
        ">
            LUXETRAVEL AI
        </h1>
        <div class="sub-text">The Art of Curated Journeys • Powered by Gemini</div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("""
        Welcome to your personal travel concierge. We combine **real-time flight data**, 
        **deep local research**, and **bespoke planning** to craft the perfect itinerary.
    """)


with col_anim:
    # UPDATED: Premium Flight Animation (Plane over world map)
    # This is a cleaner, more professional animation
    lottie_url = "https://lottie.host/6f0254c4-7221-4f10-912c-0c15906d203a/KqF3Q5lS5o.json" 
    # Fallback option if above fails: "https://assets10.lottiefiles.com/packages/lf20_t2rksq.json"
    
    lottie_json = load_lottie_url(lottie_url)
    if not lottie_json:
         # Fallback generic travel URL
         lottie_json = load_lottie_url("https://assets3.lottiefiles.com/packages/lf20_x62chJ.json")
         
    if lottie_json:
        st_lottie(lottie_json, height=200, key="header_anim")

st.markdown("---")

# ---------- INPUT SECTION ----------
st.markdown("### 🗺️ Design Your Journey")

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        source = st.text_input("From (City/IATA)", "New York (JFK)")
    with c2:
        destination = st.text_input("To (City/IATA)", "Paris (CDG)")
    with c3:
        departure_date = st.date_input("Departure", datetime.now() + timedelta(days=30))
    with c4:
        return_date = st.date_input("Return", datetime.now() + timedelta(days=37))

    st.write("") 
    
    c5, c6, c7 = st.columns([2, 1, 1])
    with c5:
        travel_theme = st.selectbox("Experience Type", ["Ultra-Luxury Relaxation", "Cultural Immersion", "Adventure & Thrill", "Romantic Getaway", "Family Fun"])
    with c6:
        budget = st.selectbox("Budget Tier", ["Premium", "Luxury", "Ultra-High-End"])
    with c7:
        num_guests = st.number_input("Guests", 1, 10, 2)
        
    activity_preferences = st.text_area("Specific Desires", "Michelin star dining, private museum tours, vintage car rental...", height=70)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ACTION BUTTON
col_center = st.columns([1, 2, 1])
with col_center[1]:
    generate_btn = st.button("✨ Curate My Itinerary")


import traceback  # Add at the top with other imports

# Calculate number of days from departure and return dates
num_days = (return_date - departure_date).days + 1

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
    "num_guests": num_guests
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
    with open("logs/agent_logs.txt", "a") as f:
        f.write(f"[{name}] {message}\n")

# ---------- GENERATE TRAVEL PLAN ----------
if generate_btn:
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
                f"Find best hotels and restaurants for {travel_theme} trip in {destination} "
                f"with budget {budget}.",
                stream=False
            ))
            log_agent("HotelFinder", "Submitted task...")

            research_results = future_research.result()
            log_agent("Researcher", "Completed research.")

            hotel_results = future_hotel.result()
            log_agent("HotelFinder", "Completed hotel search.")

        # Planner runs after both complete
        planning_prompt = (
            f"Create a {num_days}-day itinerary for a {travel_theme} trip from {source} to {destination} "
            f"({format_datetime(departure_date)} to {format_datetime(return_date)}). "
            f"Activities: {activity_preferences}. Budget: {budget}. "
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
