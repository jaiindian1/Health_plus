import streamlit as st
import os
from datetime import datetime

# --- 1. THE ANDROID & PROFESSIONAL SHIELD ---
# Sets the tab icon and title
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# Nuclear CSS: Hides 'Manage App', Header, Footer, and Deploy button
# v=110 forces Android Chrome to refresh the Manifest memory
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QSob {display: none !important;}
    
    /* Emergency Button Styling */
    .emergency-btn {
        background-color: #ff4b4b;
        color: white !important;
        text-align: center;
        padding: 20px;
        border-radius: 15px;
        font-weight: bold;
        text-decoration: none;
        display: block;
        margin-bottom: 20px;
        font-size: 20px;
        border: 2px solid white;
    }
    </style>
    <head>
        <link rel="manifest" href="./manifest.json?v=110">
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2966/2966327.png">
        <meta name="theme-color" content="#FF4B4B">
    </head>
    """, unsafe_allow_html=True)

# --- 2. DATA SYSTEM ---
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

# --- 3. SETUP GATEKEEPER ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.subheader("Setup your Emergency Guardian")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Your Phone")
        em_phone = st.text_input("Emergency Contact Number")
        if st.form_submit_button("Start Protection"):
            if name and phone and em_phone:
                profile = {"name": name, "phone": phone, "emergency": em_phone, "signup_date": datetime.now().strftime("%Y-%m-%d")}
                with open(USER_FILE, "w") as f:
                    f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}|{profile['signup_date']}")
                st.session_state.user_profile = profile
                st.rerun()
    st.info("📲 TO INSTALL: Tap 3-dots (⋮) -> 'Install App'")
    st.stop()

# --- 4. THE PROFESSIONAL DASHBOARD ---
profile = st.session_state.user_profile
st.title(f"🛡️ Guardian: {profile['name']}")

# 15-Day Calibration logic
start_dt = datetime.strptime(profile["signup_date"], "%Y-%m-%d")
days_passed = (datetime.now() - start_dt).days

if days_passed < 15:
    st.warning(f"🧬 Calibration Mode: Day {days_passed + 1}/15")
    st.progress((days_passed + 1) / 15)

tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "📸 Scanner", "⚙️ Profile"])

with tab1:
    # Always visible Panic Button
    st.markdown(f'<a href="tel:{profile["emergency"]}" class="emergency-btn">🚨 CALL EMERGENCY NOW</a>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("How are you feeling?"):
        st.chat_message("user").write(prompt)
        
        # EMERGENCY TRIGGER LOGIC
        danger_keywords = ["pain", "chest", "heart", "breath", "blood", "severe"]
        if any(word in prompt.lower() for word in danger_keywords):
            st.error("⚠️ CRITICAL SYMPTOM DETECTED")
            st.markdown(f"""
                <div style="background-color:#ff4b4b; padding:20px; border-radius:10px; text-align:center;">
                    <h2 style="color:white;">DIALING EMERGENCY...</h2>
                    <a href="tel:{profile['emergency']}" style="color:yellow; font-size:30px; font-weight:bold;">TAP HERE TO CALL {profile['emergency']}</a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.chat_message("assistant").write("I am monitoring your symptoms. Please keep me updated.")

with tab2:
    st.subheader("Medicine Scanner")
    st.camera_input("Scan your pills")

with tab3:
    st.subheader("Account Settings")
    st.write(f"**Emergency Number:** {profile['emergency']}")
    if st.button("Reset / Logout"):
        if os.path.exists(USER_FILE): os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
