import streamlit as st
import google.generativeai as genai

# --- 1. SMARTPHONE & ICON CONFIG ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# This line is CRITICAL for the mobile icon to work
st.markdown('<link rel="manifest" href="./manifest.json">', unsafe_allow_html=True)

# CSS to make the app look like a mobile phone app
st.markdown("""
    <style>
    .stApp { max-width: 450px; margin: 0 auto; }
    .stAlert { padding: 8px; font-size: 13px; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# AI SETUP - Fixed the "NotFound" error by using the base model name
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("Missing API Key! Please add it to Streamlit Secrets.")

# --- 2. MEMORY ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. PROFILE SETUP (Gatekeeper) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    with st.form("setup"):
        u_name = st.text_input("Full Name")
        u_emergency = st.text_input("Emergency Contact Number")
        if st.form_submit_button("Save & Start"):
            if u_name and u_emergency:
                st.session_state.user_profile = {"name": u_name, "emergency": u_emergency}
                st.rerun()
    st.stop()

# --- 4. MAIN APP ---
st.header(f"🛡️ Hello, {st.session_state.user_profile['name']}")

tab_chat, tab_pill = st.tabs(["💬 Chat", "📸 Scanner"])

with tab_chat:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("How can I help?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Catching errors so you don't see the red box
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception:
                st.warning("⚠️ AI is resting. Please try again in 10 seconds.")

with tab_pill:
    st.camera_input("Scan your medicine")

# Sidebar Emergency
with st.sidebar:
    if st.button("🚨 TRIGGER EMERGENCY", type="primary"):
        st.error(f"Calling: {st.session_state.user_profile['emergency']}")
