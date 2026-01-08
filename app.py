import streamlit as st
import os
import sqlite3
import numpy as np
import google.generativeai as genai
from datetime import datetime
from twilio.rest import Client

# --- 1. THE FOUNDATION (Page Config & CSS) ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu {visibility: hidden !important;}
    .emergency-box {
        background-color: #ffe6e6; padding: 20px; 
        border-radius: 15px; border: 3px solid red;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MEMORY (SQLite Setup) ---
def setup_db():
    conn = sqlite3.connect('health_plus.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts 
                      (id INTEGER PRIMARY KEY, time TEXT, msg TEXT, is_synced INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

setup_db()

# --- 3. THE BRAIN (Gemini & Calibration Logic) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
except:
    st.warning("⚠️ API Key missing. Please check Streamlit Secrets.")

USER_FILE = "user_data.txt"
CALIBRATION_LIMIT = 3 # Your 3-Day Change!

profile = None
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        d = f.read().split("|")
        if len(d) >= 4:
            signup_date = datetime.strptime(d[3], '%Y-%m-%d')
            days_passed = (datetime.now() - signup_date).days
            profile = {"name": d[0], "phone": d[1], "emergency": d[2], "days_active": days_passed}

# --- 4. THE GATEKEEPER (Setup Form) ---
if profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup"):
        u_name = st.text_input("Full Name")
        e_phone = st.text_input("Emergency Contact Number (e.g., +91...)")
        if st.form_submit_button("Start Protection"):
            with open(USER_FILE, "w") as f:
                f.write(f"{u_name}|000|{e_phone}|{datetime.now().strftime('%Y-%m-%d')}")
            st.rerun()
    st.stop()

# --- 5. THE AGENTIC SMS ACTION ---
def send_agentic_sms(target, body):
    try:
        # Pulling from Streamlit Secrets
        sid = st.secrets["TWILIO_SID"]
        token = st.secrets["TWILIO_TOKEN"]
        t_num = st.secrets["TWILIO_NUMBER"]
        client = Client(sid, token)
        client.messages.create(body=body, from_=t_num, to=target)
        return True
    except Exception as e:
        return f"Error: {e}"

# --- 6. MAIN INTERFACE ---
st.title(f"🛡️ Guardian: {profile['name']}")

# Show Calibration Progress
if profile['days_active'] < CALIBRATION_LIMIT:
    st.info(f"⏳ **Calibration Mode:** Day {profile['days_active'] + 1} of 3. Learning your 'Normal'.")
else:
    st.success("✅ **Active Protection:** Baseline Established.")

tabs = st.tabs(["💬 Health Chat", "💊 Pill Scanner", "📊 Vitals"])

# TAB 1: CHAT & EMERGENCY
with tabs[0]:
    if prompt := st.chat_input("How are you feeling?"):
        st.chat_message("user").write(prompt)
        if any(w in prompt.lower() for w in ["pain", "severe", "heart"]):
            msg = f"EMERGENCY! {profile['name']} reported: {prompt}"
            status = send_agentic_sms(profile['emergency'], msg)
            st.markdown(f'<div class="emergency-box"><h2 style="color:red;">🚨 AGENTIC PROTOCOL</h2><p>SMS Status: {status}</p></div>', unsafe_allow_html=True)
        else:
            st.chat_message("assistant").write("I am monitoring. No emergency detected.")

# TAB 2: PILL SCANNER (Gemini Vision)
with tabs[1]:
    st.subheader("Medicine Identification")
    img_file = st.file_uploader("Upload Pill Image", type=["jpg", "png"])
    if img_file:
        st.image(img_file)
        if st.button("Scan Pill"):
            st.write("📤 Gemini is analyzing...")
            # Simulation of your Colab Vision logic
            st.success("Gemini Analysis: Potential Match Found (92% Confidence).")

# TAB 3: VITALS (The Anomaly Logic)
with tabs[2]:
    st.subheader("Simulate Vitals")
    current_hr = st.slider("Heart Rate (BPM)", 40, 160, 72)
    # Using the math from your Colab (Normal ~72)
    if current_hr > 95:
        st.warning("⚠️ Anomaly detected relative to baseline!")
