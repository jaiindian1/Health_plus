import streamlit as st
import google.generativeai as genai
import time

# --- 1. SMARTPHONE & MANIFEST SETUP ---
st.set_page_config(page_title="Health Plus Assistant", layout="centered", page_icon="💊")

# LINKING YOUR JSON MANIFEST (Allows the mobile icon to work)
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)

# MOBILE CSS: Makes the app look good on a small screen
st.markdown("""
    <style>
    .stApp { max-width: 450px; margin: 0 auto; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# AI CONFIG
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    # Using stable flash model name
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
    st.subheader("Setup Your Profile")
    
    with st.form("setup_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Your Number")
        emergency_no = st.text_input("Emergency Number (Suresh)")
        
        if st.form_submit_button("Save & Enter App"):
            if name and phone and emergency_no:
                st.session_state.user_profile = {"name": name, "phone": phone, "emergency": emergency_no}
                st.rerun()
            else:
                st.warning("Please fill all fields!")
    st.stop()

# --- 4. MAIN MOBILE APP ---
st.header(f"🛡️ Hello, {st.session_state.user_profile['name']}")

tab_chat, tab_pill = st.tabs(["💬 Chat", "📸 Scan"])

with tab_chat:
    st.caption(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("How are you feeling?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            context = f"User: {st.session_state.user_profile['name']}. Prompt: {prompt}"
            response = model.generate_content(context)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

with tab_pill:
    st.subheader("Medicine Scanner")
    img = st.camera_input("Take a photo")
    if img:
        st.info("AI is analyzing...")

# Sidebar: Emergency
with st.sidebar:
    st.header("🆘 Help")
    if st.button("🚨 CALL EMERGENCY"):
        st.error(f"ALERT SENT TO: {st.session_state.user_profile['emergency']}")
