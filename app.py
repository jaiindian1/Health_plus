import streamlit as st
import google.generativeai as genai

# --- 1. MOBILE & ICON SETUP ---
# Centered layout is better for small phone screens
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# This is the "Magic Link" that makes your mobile icon work
st.markdown('<link rel="manifest" href="manifest.json">', unsafe_allow_html=True)

# CSS to make the app look clean and keep errors to one line
st.markdown("""
    <style>
    .stApp { max-width: 450px; margin: 0 auto; }
    .stAlert { padding: 5px 15px; font-size: 14px; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# AI CONFIG - Using the most stable model name
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("Missing API Key! Please check your Streamlit Secrets.")

# --- 2. MEMORY MANAGEMENT ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. THE GATEKEEPER (Profile Setup) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup_form"):
        u_name = st.text_input("Full Name")
        u_phone = st.text_input("Your Phone Number")
        u_emergency = st.text_input("Emergency Contact (e.g. Suresh)")
        
        if st.form_submit_button("Save & Enter App"):
            if u_name and u_phone and u_emergency:
                st.session_state.user_profile = {
                    "name": u_name, 
                    "phone": u_phone, 
                    "emergency": u_emergency
                }
                st.rerun()
            else:
                st.warning("Please fill in all details.")
    st.stop()

# --- 4. MAIN APP INTERFACE ---
st.header(f"🛡️ Hello, {st.session_state.user_profile['name']}")

tab_chat, tab_pill = st.tabs(["💬 AI Advisor", "📸 Scanner"])

with tab_chat:
    st.caption(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    
    # Show Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Tell me how you feel..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Attempt to get AI response
                response = model.generate_content(f"User {st.session_state.user_profile['name']} says: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # ONE-LINE ERROR: Catches 404, 500, or API errors quietly
                st.warning("⚠️ AI is busy right now. Please try again in a moment.")

with tab_pill:
    st.subheader("Medicine Scanner")
    img = st.camera_input("Scan your medicine")
    if img:
        st.info("Pill analysis feature coming soon!")

# Sidebar Emergency Button
with st.sidebar:
    if st.button("🚨 TRIGGER EMERGENCY", type="primary"):
        st.error(f"Calling Emergency Contact: {st.session_state.user_profile['emergency']}")
