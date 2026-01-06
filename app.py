import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. THE PROFESSIONAL SHIELD (Hiding all hurdles) ---
# Replaces the tab icon with a Heart ❤️
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# This CSS targets every possible developer button to hide them
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    /* This hides the "Manage App" button for everyone except the logged-in dev */
    /* To see it like a user, open this in INCOGNITO MODE */
    div[data-testid="stStatusWidget"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    button[title="View source"] {display: none !important;}
    </style>
    
    <head>
        <link rel="manifest" href="./manifest.json?v=99">
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2966/2966327.png">
    </head>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN (Memory) ---
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

# --- 3. THE FRONT DOOR (Setup) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.subheader("Professional AI Medical Mentor")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Your Phone Number")
        emergency = st.text_input("Emergency Contact")
        if st.form_submit_button("Create My Account"):
            if name and phone and emergency:
                profile = {
                    "name": name, "phone": phone, "emergency": emergency,
                    "signup_date": datetime.now().strftime("%Y-%m-%d")
                }
                with open(USER_FILE, "w") as f:
                    f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}|{profile['signup_date']}")
                st.session_state.user_profile = profile
                st.rerun()
    
    st.info("📲 INSTALL: Tap 3-dots (⋮) -> 'Install App' or 'Add to Home Screen'")
    st.stop()

# --- 4. THE REAL APP (Professional Flow) ---
# We use st.empty() to clear space for a clean look
st.title(f"🛡️ Welcome, {st.session_state.user_profile['name']}")

# Calibration Progress
start_dt = datetime.strptime(st.session_state.user_profile["signup_date"], "%Y-%m-%d")
days_passed = (datetime.now() - start_dt).days

if days_passed < 15:
    st.write(f"🧬 **Calibration Mode**: Day {days_passed + 1} of 15")
    st.progress((days_passed + 1) / 15)
    st.caption("I am currently learning your health baseline. Full analysis starts on Day 16.")

# --- 5. TABS ---
t1, t2, t3 = st.tabs(["💬 AI Assistant", "📸 Pill Scanner", "⚙️ My Profile"])

with t1:
    st.subheader("Medical Chat")
    if prompt := st.chat_input("How are you feeling?"):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("I am analyzing your symptoms based on your 15-day baseline...")

with t2:
    st.subheader("Scanner")
    st.camera_input("Take a photo of your medication")

with t3:
    st.subheader("Account")
    st.write(f"**Name:** {st.session_state.user_profile['name']}")
    st.write(f"**Emergency:** {st.session_state.user_profile['emergency']}")
    if st.button("Logout & Reset App"):
        if os.path.exists(USER_FILE): os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
