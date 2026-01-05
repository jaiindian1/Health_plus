import streamlit as st
import google.generativeai as genai
import time

# --- 1. SETUP & AI CONFIG ---
st.set_page_config(page_title="Health Plus Assistant", layout="wide")

# FIX: Using 'gemini-1.5-flash-latest' to avoid the NotFound error
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# --- 2. MEMORY (Session State) ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None # Stores {name, phone, emergency}
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PROFILE SETUP SCREEN (The Gatekeeper) ---
if st.session_state.user_profile is None:
    st.title("🏥 Welcome to Health Plus")
    st.subheader("Please set up your medical profile to continue")
    
    with st.form("setup_form"):
        name = st.text_input("Your Full Name")
        phone = st.text_input("Your Phone Number")
        emergency_no = st.text_input("Emergency Contact Number (Suresh/Doctor)")
        
        submit = st.form_submit_button("Save Profile & Enter App")
        
        if submit:
            if name and phone and emergency_no:
                st.session_state.user_profile = {
                    "name": name,
                    "phone": phone,
                    "emergency": emergency_no
                }
                st.success(f"Welcome, {name}! Profile saved.")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Please fill in all fields so we can keep you safe!")
    st.stop() # Stops the rest of the app from running until profile is done

# --- 4. MAIN APP (Only shows after setup) ---
st.title(f"🛡️ Health Plus: Monitoring {st.session_state.user_profile['name']}")

tab_chat, tab_pill = st.tabs(["💬 AI Mentor Chat", "📸 Medicine Scanner"])

with tab_chat:
    st.write(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    
    # Chat Logic
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("How are you feeling?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # We tell the AI who it is talking to for better advice
            context = f"User: {st.session_state.user_profile['name']}. Prompt: {prompt}"
            response = model.generate_content(context)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

with tab_pill:
    st.subheader("Medicine Scanner")
    img = st.camera_input("Take a photo of the medicine")
    if img:
        st.info("Guardian AI is analyzing your medicine...")
        # (AI Vision logic goes here)

# Sidebar: Emergency Button
with st.sidebar:
    st.header("🆘 Emergency")
    if st.button("🚨 TRIGGER EMERGENCY CALL"):
        st.error(f"CALLING EMERGENCY CONTACT: {st.session_state.user_profile['emergency']}")
        st.write("Sending GPS location and health data...")
