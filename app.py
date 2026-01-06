import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. PROFESSIONAL UI (Hiding the Hurdles) ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

st.markdown("""
    <style>
    /* Hides the Streamlit Header, Footer, and 'Manage app' button */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    /* This line specifically targets the 'Manage app' button overlay */
    [data-testid="stStatusWidget"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MEMORY SYSTEM ---
USER_FILE = "user_data.txt"

def load_user():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                d = f.read().split("|")
                return {"name": d[0], "phone": d[1], "emergency": d[2], "signup_date": d[3]}
        except: return None
    return None

if "user_profile" not in st.session_state:
    st.session_state.user_profile = load_user()

# --- 3. THE GATEKEEPER ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        emergency = st.text_input("Emergency Contact")
        if st.form_submit_button("Start Protection"):
            if name and phone and emergency:
                profile = {
                    "name": name, "phone": phone, "emergency": emergency,
                    "signup_date": datetime.now().strftime("%Y-%m-%d")
                }
                with open(USER_FILE, "w") as f:
                    f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}|{profile['signup_date']}")
                st.session_state.user_profile = profile
                st.rerun()
    
    st.info("📲 TO INSTALL: Click 3-dots (⋮) at top right & select 'Install App'")
    st.stop()

# --- 4. THE MAIN APP (This was the missing part!) ---
# This part ONLY runs if st.session_state.user_profile is NOT None
st.write(f"✨ **Welcome back, {st.session_state.user_profile['name']}!**")

# Calibration Logic
start_dt = datetime.strptime(st.session_state.user_profile["signup_date"], "%Y-%m-%d")
days_passed = (datetime.now() - start_dt).days

if days_passed < 15:
    st.warning(f"🧬 Calibration: Day {days_passed + 1}/15")
    st.progress((days_passed + 1) / 15)

# --- 5. THE PROFESSIONAL TOOLS ---
tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "📸 Scanner", "⚙️ Settings"])

with tab1:
    st.subheader("Health Assistant")
    st.caption("How are you feeling right now?")
    # Chat logic would go here

with tab2:
    st.subheader("Medicine Scanner")
    st.camera_input("Scan your pill bottle")

with tab3:
    st.subheader("Profile Settings")
    st.write(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    if st.button("Logout / Reset App"):
        if os.path.exists(USER_FILE): os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
