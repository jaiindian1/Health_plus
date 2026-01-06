import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from twilio.rest import Client  # Added for Agentic Auto-SMS

# --- 1. SETUP & BRANDING ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# Nuclear CSS to hide Streamlit branding and 'Manage App'
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QSob {display: none !important;}
    iframe[title="Manage app"] {display: none !important;}
    .emergency-box {
        background-color: #ffe6e6; padding: 20px; 
        border-radius: 15px; border: 3px solid red;
    }
    </style>
    <head><link rel="manifest" href="./manifest.json?v=400"></head>
    """, unsafe_allow_html=True)

# --- 2. THE AGENTIC SMS BRAIN ---
def send_auto_sms(target_number, body_text):
    try:
        # Get these from your Twilio Console (twilio.com)
        account_sid = 'YOUR_TWILIO_SID' 
        auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
        twilio_number = 'YOUR_TWILIO_PHONE_NUMBER'
        
        client = Client(account_sid, auth_token)
        client.messages.create(body=body_text, from_=twilio_number, to=target_number)
        return True
    except Exception as e:
        st.error(f"Agentic SMS Failed: {e}")
        return False

# --- 3. GPS SCRIPT (JavaScript "Waiter") ---
loc_js = """
<script>
navigator.geolocation.getCurrentPosition((post) => {
    window.parent.postMessage({
        type: 'streamlit:set_component_value',
        value: {lat: post.coords.latitude, lon: post.coords.longitude}
    }, '*');
});
</script>
"""
components.html(loc_js, height=0)

# --- 4. PROFILE & DATA LOADING ---
USER_FILE = "user_data.txt"
profile = None
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        d = f.read().split("|")
        if len(d) >= 4:
            profile = {"name": d[0], "phone": d[1], "emergency": d[2], "date": d[3]}

if profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup"):
        u_name = st.text_input("Name")
        e_phone = st.text_input("Emergency Number (with +country code)")
        if st.form_submit_button("Activate Agent"):
            with open(USER_FILE, "w") as f:
                f.write(f"{u_name}|000|{e_phone}|{datetime.now().strftime('%Y-%m-%d')}")
            st.rerun()
    st.stop()

# --- 5. MAIN AGENTIC CHAT ---
st.title(f"🛡️ Guardian: {profile['name']}")

if prompt := st.chat_input("Describe your feeling..."):
    st.chat_message("user").write(prompt)
    
    # Check for Danger
    if any(w in prompt.lower() for w in ["pain", "severe", "heart", "breath"]):
        lat = st.session_state.get('loc_data', {}).get('lat', '27.89')
        lon = st.session_state.get('loc_data', {}).get('lon', '78.08')
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        
        # AGENTIC ACTION: Send SMS Automatically in background!
        sms_msg = f"EMERGENCY! {profile['name']} needs help. Location: {maps_link}"
        success = send_auto_sms(profile['emergency'], sms_msg)
        
        st.markdown(f"""
            <div class="emergency-box">
                <h2 style="color:red;">🚨 AGENTIC PROTOCOL ACTIVATED</h2>
                <p>{"✅ Auto-SMS Sent to Contact" if success else "❌ Auto-SMS Failed"}</p>
                <a href="tel:{profile['emergency']}" style="display:block; padding:15px; background:red; color:white; border-radius:10px; text-align:center; text-decoration:none; font-weight:bold;">
                    📞 CLICK TO START VOICE CALL
                </a>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.chat_message("assistant").write("I am monitoring. No immediate danger detected.")
