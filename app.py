import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime

# --- 1. HIDING HURDLES & BRANDING ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

st.markdown("""
    <style>
    /* Hiding Streamlit Branding and 'Manage App' */
    header, footer, .stDeployButton, #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QSob {display: none !important;}
    iframe[title="Manage app"] {display: none !important;}
    
    .emergency-box {
        background-color: #ffe6e6; padding: 20px; 
        border-radius: 15px; border: 3px solid red;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING (Safety First) ---
USER_FILE = "user_data.txt"
profile = None
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        d = f.read().split("|")
        if len(d) >= 4:
            profile = {"name": d[0], "phone": d[1], "emergency": d[2], "date": d[3]}

# --- 3. GATEKEEPER (The Intro) ---
if profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup"):
        u_name = st.text_input("Full Name")
        e_phone = st.text_input("Emergency Contact Number")
        if st.form_submit_button("Start Protection"):
            with open(USER_FILE, "w") as f:
                f.write(f"{u_name}|000|{e_phone}|{datetime.now().strftime('%Y-%m-%d')}")
            st.rerun()
    st.stop()

# --- 4. THE AGENTIC SMS LOGIC (Safely wrapped) ---
def send_agentic_sms(target, body):
    try:
        from twilio.rest import Client
        # Replace these with your actual Twilio details
        sid = 'YOUR_SID_HERE'
        token = 'YOUR_TOKEN_HERE'
        t_num = 'YOUR_TWILIO_NUMBER'
        
        client = Client(sid, token)
        client.messages.create(body=body, from_=t_num, to=target)
        return True
    except Exception as e:
        return f"Wait for Twilio Setup: {e}"

# --- 5. MAIN INTERFACE ---
st.title(f"🛡️ Guardian: {profile['name']}")

if prompt := st.chat_input("How are you feeling?"):
    st.chat_message("user").write(prompt)
    
    if any(w in prompt.lower() for w in ["pain", "severe", "heart"]):
        # Automatic Agentic Action
        msg = f"EMERGENCY! {profile['name']} reported {prompt}."
        status = send_agentic_sms(profile['emergency'], msg)
        
        st.markdown(f"""
            <div class="emergency-box">
                <h2 style="color:red;">🚨 AGENTIC PROTOCOL</h2>
                <p>Status: {status if status != True else "✅ Auto-SMS Sent"}</p>
                <a href="tel:{profile['emergency']}" style="display:block; padding:15px; background:red; color:white; border-radius:10px; text-align:center; text-decoration:none;">
                    📞 CLICK TO CALL NOW
                </a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.chat_message("assistant").write("I am monitoring. No emergency detected.")
