import streamlit as st
import os
from datetime import datetime

# --- 1. ANDROID BRANDING OVERRIDE ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# We use "v=101" to trick Chrome into thinking this is a brand new app
st.markdown("""
    <head>
        <link rel="manifest" href="./manifest.json?v=101">
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2966/2966327.png">
        <meta name="theme-color" content="#FF4B4B">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
    <style>
        /* Hides all professional hurdles */
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        #MainMenu {visibility: hidden !important;}
        /* Hides the 'Manage App' for a clean look */
        div[data-testid="stStatusWidget"] {display: none !important;}
        .viewerBadge_container__1QSob {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. MEMORY SYSTEM ---
USER_FILE = "user_data.txt"

def get_profile():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            d = f.read().split("|")
            return {"name": d[0], "signup_date": d[3]}
    return None

if "user_profile" not in st.session_state:
    st.session_state.user_profile = get_profile()

# --- 3. THE PROFESSIONAL FLOW ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    with st.form("setup"):
        name = st.text_input("Name")
        if st.form_submit_button("Create Account"):
            # Save data logic here...
            st.rerun()
    st.info("📲 INSTALL: Tap 3-dots (⋮) -> 'Install App'")
    st.stop()

# --- 4. MAIN APP CONTENT ---
st.title(f"🛡️ Health Guardian: {st.session_state.user_profile['name']}")
# Rest of your AI and Scanner tabs go here...
