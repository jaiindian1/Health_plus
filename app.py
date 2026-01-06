import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime

# --- 1. THE PWA ENGINE (Fixes the "Install" issue) ---
# Replace 'YOUR_APP_URL' with your actual streamlit link (e.g., health-plus.streamlit.app)
APP_URL = "https://health-plus.streamlit.app" 

st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# This block forces the phone to see the Manifest and hides the browser UI
st.markdown(f"""
    <head>
        <link rel="manifest" href="{APP_URL}/manifest.json?v=15">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
    </head>
    <style>
    header {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    .stDeployButton {{display:none !important;}}
    .stApp {{ max-width: 450px; margin: 0 auto; }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT MEMORY & CALIBRATION ---
USER_FILE = "user_data.txt"

def save_user(profile):
    with open(USER_FILE, "w") as f:
        # Saving: Name | Phone | Emergency | SignupDate
        f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}|{profile['signup_date']}")

def load_user():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                d = f.read().split("|")
                return {"name": d[0], "phone": d[1], "emergency": d[2], "signup_date": d[3]}
        except: return None
    return None

# --- 3. SESSION & AI SETUP ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = load_user()

@st.cache_resource
def init_ai():
    if "API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["API_KEY"])
        return genai.GenerativeModel('gemini-1.5-flash')
    return None

model = init_ai()

# --- 4. THE SETUP FORM ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.write("Welcome! Let's start your 15-day calibration.")
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
    st.stop()

# --- 5. CALIBRATION LOGIC ---
start_dt = datetime.strptime(st.session_state.user_profile["signup_date"], "%Y-%m-%d")
days_passed = (datetime.now() - start_dt).days

# --- 6. MAIN INTERFACE ---
st.header(f"🛡️ {st.session_state.user_profile['name']}")

if days_passed < 15:
    st.info(f"🧬 Calibration Mode: Day {days_passed + 1} of 15")
    st.progress((days_passed + 1) / 15)
else:
    st.success("✅ Calibration Complete. Monitoring Active.")

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📸 Scanner", "⚙️ Profile"])

with tab1:
    if prompt := st.chat_input("How are you today?"):
        st.chat_message("user").write(prompt)
        if model:
            res = model.generate_content(f"User {st.session_state.user_profile['name']} says: {prompt}")
            st.chat_message("assistant").write(res.text)

with tab2:
    st.subheader("Pill Scanner")
    st.camera_input("Scan Medicine")

with tab3:
    if st.button("🗑️ Reset All"):
        if os.path.exists(USER_FILE): os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
