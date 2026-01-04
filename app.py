import streamlit as st
import google.generativeai as genai
import numpy as np
import time

# --- INITIAL SETUP ---
st.set_page_config(page_title="Project Health Plus", page_icon="💊")

# Securely load your API Key from Streamlit Secrets
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("API Key not found in Secrets!")

# --- 15-DAY MEMORY (Session State) ---
if 'baseline' not in st.session_state:
    # Simulating the first 15 days for now
    st.session_state.baseline = 72.0 

# --- UI FOR SENIORS (Large Text) ---
st.title("🛡️ Project Health Plus")
st.subheader("Your Medical Guardian")

tab1, tab2 = st.tabs(["📸 Pill Scanner", "🏠 Guardian Status"])

with tab1:
    st.write("### Scan your medicine below")
    img_file = st.camera_input("Take a photo of the pill")

    if img_file:
        with st.spinner("Guardian is analyzing..."):
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Using your specific prompt logic
            prompt = "Identify this medicine. Provide name, uses, and a confidence score (0-1)."
            
            # Process image
            img_bytes = img_file.getvalue()
            response = model.generate_content([
                prompt,
                {'mime_type': 'image/jpeg', 'data': img_bytes}
            ])
            
            st.success("Analysis Complete!")
            st.write(response.text)

with tab2:
    st.write(f"### Hello, Champ!")
    st.metric(label="Normal Heart Rate (15-Day Avg)", value=f"{st.session_state.baseline} BPM")
    
    # Simple Anomaly Simulation
    current_hr = st.slider("Simulate Current Heart Rate", 60, 120, 75)
    
    if current_hr > (st.session_state.baseline + 20):
        st.error("🚨 ANOMALY DETECTED!")
        if st.button("I'M OKAY", use_container_width=True):
            st.success("Guardian Standby: Resetting...")
        else:
            st.warning("Triggering auto-call to Suresh in 10 seconds...")
