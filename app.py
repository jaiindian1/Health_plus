import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. IDENTITY & LOGO ---
# page_icon="❤️" replaces the Streamlit logo in the browser tab
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# REPLACE THIS with your actual link so the manifest works!
APP_URL = "https://health-plus.streamlit.app" 

st.markdown(f"""
    <head>
        <link rel="manifest" href="{APP_URL}/manifest.json?v=20">
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2966/2966327.png">
    </head>
    <style>
    header {{visibility: hidden !important;}}
    .stApp {{ max-width: 450px; margin: 0 auto; }}
    /* Styling for our instruction message */
    .install-msg {{
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border: 1px dashed #ff4b4b;
        text-align: center;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOGIC ---
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

# --- 3. THE SETUP FORM ---
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
                with open(USER_FILE, "w") as f:
                    f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}|{profile['signup_date']}")
                st.session_state.user_profile = profile
                st.rerun()

    # --- THE INSTRUCTION MESSAGE YOU ASKED FOR ---
    st.markdown("""
        <div class="install-msg">
            📲 TO INSTALL ON MOBILE:<br>
            1. Click the 3 DOTS (⋮) at the top right.<br>
            2. Tap "Add to Home Screen" or "Install App".
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- 4. MAIN INTERFACE (Only shows after setup) ---
st.success(f"Welcome back, {st.session_state.user_profile['name']}!")
# ... (rest of your chat code goes here)
