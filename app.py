import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime

# --- 1. SETTINGS & BRANDING (Hiding Hurdles) ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

st.markdown("""
    <style>
    /* Nuclear Hide: Removes Streamlit branding & 'Manage App' */
    header, footer, .stDeployButton, #MainMenu {visibility: hidden !important;}
    div[data-testid="stStatusWidget"], .viewerBadge_container__1QSob {display: none !important;}
    
    /* Hide the black 'Manage App' button specifically */
    iframe[title="Manage app"] {display: none !important;}
    
    .emergency-box {
        background-color: #ffe6e6; padding: 20px; 
        border-radius: 15px; border: 3px solid red;
    }
    .action-link {
        display: block; padding: 15px; color: white !important;
        border-radius: 10px; margin-top: 10px; text-align: center;
        text-decoration: none; font-weight: bold; font-size: 18px;
    }
    </style>
    <head><link rel="manifest" href="./manifest.json?v=300"></head>
    """, unsafe_allow_html=True)

# --- 2. LOCATION SCRIPT (JavaScript "Waiter") ---
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

# --- 3. DATA LOADING (The Fix for NameError) ---
USER_FILE = "user_data.txt"
profile = None # Start with nothing

if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        d = f.read().split("|")
        # Ensure we have all 4 pieces of data
        if len(d) >= 4:
            profile = {"name": d[0], "phone": d[1], "emergency": d[2], "signup_date": d[3]}

# --- 4. GATEKEEPER (If no profile, show Setup) ---
if profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup_form"):
        u_name = st.text_input("Your Name")
        u_phone = st.text_input("Your Phone")
        e_phone = st.text_input("Emergency Contact Number")
        if st.form_submit_button("Save & Start"):
            if u_name and u_phone and e_phone:
                date_str = datetime.now().strftime("%Y-%m-%d")
                with open(USER_FILE, "w") as f:
                    f.write(f"{u_name}|{u_phone}|{e_phone}|{date_str}")
                st.rerun()
    st.stop()

# --- 5. MAIN AGENTIC INTERFACE ---
st.title(f"🛡️ Guardian: {profile['name']}")

tab1, tab2 = st.tabs(["💬 AI Chat", "📸 Scanner"])

with tab1:
    if prompt := st.chat_input("Describe your feeling..."):
        st.chat_message("user").write(prompt)
        
        # Check for danger
        if any(w in prompt.lower() for w in ["pain", "severe", "heart", "breath"]):
            # Get GPS from session or use Aligarh default if not loaded yet
            lat = st.session_state.get('loc_data', {}).get('lat', '27.89')
            lon = st.session_state.get('loc_data', {}).get('lon', '78.08')
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            
            # THE FIX: Now 'profile' is guaranteed to exist here
            sms_body = f"EMERGENCY! {profile['name']} needs help. Location: {maps_url}"
            
            st.markdown(f"""
                <div class="emergency-box">
                    <h2 style="color:red; margin:0;">🚨 AGENTIC PROTOCOL</h2>
                    <p>Critical symptom detected. Actions ready:</p>
                    <a href="sms:{profile['emergency']}?body={sms_body}" class="action-link" style="background: #007bff;">
                        ✉️ SEND LOCATION SMS
                    </a>
                    <a href="tel:{profile['emergency']}" class="action-link" style="background: #dc3545;">
                        📞 START EMERGENCY CALL
                    </a>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.chat_message("assistant").write("I am monitoring. No immediate danger detected.")
