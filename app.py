import streamlit as st
import streamlit.components.v1 as components

# --- 1. AGENTIC LOCATION SCRIPT ---
# This script asks the phone for GPS coordinates
loc_script = """
<script>
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  }
}
function showPosition(position) {
  const lat = position.coords.latitude;
  const lon = position.coords.longitude;
  window.parent.postMessage({
    type: 'streamlit:set_component_value',
    value: {lat: lat, lon: lon}
  }, '*');
}
getLocation();
</script>
"""

# --- 2. THE APP LOGIC ---
st.title("🛡️ Agentic Health Guardian")

# Hidden component to get location
location_data = components.html(loc_script, height=0)

# Simulate user profile data
em_phone = "9876543210" # Replace with your saved emergency number

if prompt := st.chat_input("Describe your feeling..."):
    st.chat_message("user").write(prompt)
    
    if "pain" in prompt.lower() or "severe" in prompt.lower():
        st.error("🚨 AGENTIC PROTOCOL ACTIVATED")
        
        # Get location from the script
        lat = 27.89  # Default or fetched
        lon = 78.08  # Default or fetched
        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        
        sms_body = f"EMERGENCY! {profile['name']} needs help. Location: {google_maps_link}"
        
        # The Agentic Action Box
        st.markdown(f"""
            <div style="background-color:#ffe6e6; padding:20px; border-radius:15px; border:2px solid red;">
                <h3 style="color:red;">Taking Action Now:</h3>
                <a href="sms:{em_phone}?body={sms_body}" style="display:block; padding:15px; background:blue; color:white; border-radius:10px; margin-bottom:10px; text-align:center; text-decoration:none;">
                    ✉️ SEND LOCATION SMS TO CONTACT
                </a>
                <a href="tel:{em_phone}" style="display:block; padding:15px; background:red; color:white; border-radius:10px; text-align:center; text-decoration:none;">
                    📞 START EMERGENCY CALL
                </a>
            </div>
        """, unsafe_allow_html=True)
