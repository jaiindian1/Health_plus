import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. PROFESSIONAL UI CONFIG (HIDDEN HURDLES) ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# This CSS hides the "Manage App", "Made with Streamlit", and the Header
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebarNav"] {display: none;}
    /* Hides the "Manage App" floating button for users */
    .viewerBadge_container__1QSob {display: none !important;}
    </style>
    
    <head>
        <link rel="manifest" href="./manifest.json?v=30">
        <meta name="theme-color" content="#FF4B4B">
    </head>
    """, unsafe_allow_html=True)

# --- 2. DATA STORAGE ---
USER_FILE = "user_data.txt"

def save_user(profile):
    with open(USER_FILE, "w") as f:
        f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}|{profile['signup_date']}")

def load_user():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                d = f.read().split("|")
                return {"name": d[0], "phone": d[1], "emergency": d[2], "signup_date": d[3]}
        except: return None
    return None

# Initialize session
if "user_profile" not in st.session_state:
    st.session_state.user_profile = load_user()

# --- 3. THE GATEKEEPER (FORM) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        emergency = st.text_input("Emergency Contact")
        if st.form_submit_button("Save & Start"):
            if name and phone and emergency:
                profile = {
                    "name": name, "phone": phone, "emergency": emergency,
                    "signup_date": datetime.now().strftime("%Y-%m-%d")
                }
                save_user(profile)
                st.session_state.user_profile = profile
                st.rerun()
    
    st.info("📲 TO INSTALL: Click 3-dots (⋮) at top right & select 'Install App'")
    st.stop() # App stops here ONLY if there is no user profile

# --- 4. THE PROFESSIONAL APP CONTENT (Everything after Setup) ---
st.header(f"🛡️ Health Plus: {st.session_state.user_profile['name']}")

# Calibration Logic
start_dt = datetime.strptime(st.session_state.user_profile["signup_date"], "%Y-%m-%d")
days_passed = (datetime.now() - start_dt).days

if days_passed < 15:
    st.warning(f"🧬 Calibration: Day {days_passed + 1}/15")
    st.progress((days_passed + 1) / 15)

tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "📸 Scanner", "⚙️ Settings"])

with tab1:
    st.write("How can I help you today?")
    # Add your Chat logic here...

with tab2:
    st.camera_input("Scan Medicine")

with tab3:
    if st.button("Logout / Reset"):
        if os.path.exists(USER_FILE): os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
