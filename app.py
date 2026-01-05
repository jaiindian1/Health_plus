import streamlit as st
import google.generativeai as genai
import numpy as np
import time

# --- INITIAL SETUP ---
st.set_page_config(page_title="Project Health Plus", page_icon="💊")

# Securely load your API Key
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("API Key not found in Secrets!")

# --- MEMORY (Session State) ---
if 'baseline' not in st.session_state:
    st.session_state.baseline = 72.0 

# NEW: State to track if we are waiting for the Guardian
if 'guardian_photo_ready' not in st.session_state:
    st.session_state.guardian_photo_ready = False
if 'request_sent' not in st.session_state:
    st.session_state.request_sent = False

# --- UI FOR SENIORS ---
st.title("🛡️ Project Health Plus")
st.subheader("Your Medical Guardian")

tab1, tab2 = st.tabs(["📸 Pill Scanner", "🏠 Guardian Status"])

with tab1:
    st.write("### Medicine Verification")
    
    if not st.session_state.request_sent:
        st.info("Tap below to ask your Guardian to take a photo of your pill.")
        if st.button("🔔 Request Photo from Guardian", use_container_width=True):
            st.session_state.request_sent = True
            st.rerun()
            
    elif st.session_state.request_sent and not st.session_state.guardian_photo_ready:
        with st.spinner("Waiting for Guardian to upload photo..."):
            # SIMULATION: In reality, your code would check a Database/GitHub here
            time.sleep(3) 
            st.session_state.guardian_photo_ready = True
            st.rerun()

    elif st.session_state.guardian_photo_ready:
        st.success("✅ Photo received from Guardian!")
        # For now, we use a placeholder image to represent the Guardian's upload
        guardian_img = "https://via.placeholder.com/400x300.png?text=Guardian+Pill+Photo"
        st.image(guardian_img, caption="Verified Image")
        
        if st.button("🔍 Analyze with Gemini AI", use_container_width=True):
            with st.spinner("Guardian AI is analyzing..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "Identify this medicine. Provide name, uses, and a confidence score (0-1)."
                # Note: In real use, we'd pass the actual Guardian image bytes here
                st.write("🤖 **AI Result:** This is Paracetamol 500mg. Safe to take as per schedule.")
        
        if st.button("Reset Scanner"):
            st.session_state.request_sent = False
            st.session_state.guardian_photo_ready = False
            st.rerun()

with tab2:
    st.write(f"### Hello, Champ!")
    st.metric(label="Normal Heart Rate (15-Day Avg)", value=f"{st.session_state.baseline} BPM")
    current_hr = st.slider("Simulate Current Heart Rate", 60, 120, 75)
    
    if current_hr > (st.session_state.baseline + 20):
        st.error("🚨 ANOMALY DETECTED!")
        if st.button("I'M OKAY", use_container_width=True):
            st.success("Guardian Standby: Resetting...")
        else:
            st.warning("Triggering auto-call to Suresh in 10 seconds...")
