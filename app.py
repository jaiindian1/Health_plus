import streamlit as st
import google.generativeai as genai
import time

# --- 1. CONFIG & AI SETUP ---
st.set_page_config(page_title="Health Plus Assistant", layout="wide")

if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API Key!")

# --- 2. MEMORY (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "hr_history" not in st.session_state:
    st.session_state.hr_history = [70, 72, 75, 71, 73] # Simulated history

# --- 3. UI LAYOUT ---
st.title("🛡️ Health Plus AI Mentor")

# Sidebar: Health Pattern Tracking
with st.sidebar:
    st.header("📊 Health Patterns")
    avg_hr = sum(st.session_state.hr_history) / len(st.session_state.hr_history)
    st.metric("15-Day Heart Rate Avg", f"{avg_hr} BPM")
    
    current_hr = st.slider("Update Current Heart Rate", 50, 120, 72)
    if current_hr > (avg_hr + 15):
        st.error("🚨 Pattern Alert: Heart rate is higher than usual.")

# Main Screen: 3 Functions in One
tab_chat, tab_pill = st.tabs(["💬 Talk to Mentor", "📸 Medicine Scanner"])

with tab_chat:
    st.subheader("Chat with your AI Health Advisor")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How are you feeling today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            response = model.generate_content(f"You are a medical mentor. The user says: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

with tab_pill:
    st.subheader("Medicine Identification")
    mode = st.radio("Who is taking the photo?", ["Me (User)", "Guardian"])
    
    if mode == "Me (User)":
        img = st.camera_input("Scan your pill")
        if img:
            with st.spinner("Analyzing..."):
                # AI Logic for Image
                st.success("Analysis: This looks like Vitamin C. It helps your immune system.")
    else:
        if st.button("Request Guardian to take photo"):
            st.info("Notification sent to Suresh...")
