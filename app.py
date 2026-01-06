import streamlit as st
import google.generativeai as genai
import os

# --- 1. DESIGN & IDENTITY ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# This block links your manifest.json and hides Streamlit UI for a "Real App" feel
st.markdown("""
    <link rel="manifest" href="./manifest.json?v=10">
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .stApp { max-width: 450px; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT MEMORY ---
USER_FILE = "user_data.txt"

def save_user_to_disk(profile):
    with open(USER_FILE, "w") as f:
        f.write(f"{profile['name']}|{profile['phone']}|{profile['emergency']}")

def load_user_from_disk():
    if os.path.exists(USER_FILE):
        try:
            with open(USER_FILE, "r") as f:
                data = f.read().split("|")
                return {"name": data[0], "phone": data[1], "emergency": data[2]}
        except:
            return None
    return None

# --- 3. AI CONFIG (OPTIMIZED) ---
@st.cache_resource
def get_ai_model():
    if "API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["API_KEY"])
        # Checking for the most common 2026 models
        for m_name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(m_name)
                m.generate_content("test")
                return m
            except:
                continue
    return None

model = get_ai_model()

# --- 4. SESSION MANAGEMENT ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = load_user_from_disk()

# --- 5. THE SETUP FORM (Gatekeeper) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.subheader("Your Personal AI Guardian")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Your Phone Number")
        emergency = st.text_input("Emergency Contact Number")
        if st.form_submit_button("Save & Start Protection"):
            if name and phone and emergency:
                profile = {"name": name, "phone": phone, "emergency": emergency}
                save_user_to_disk(profile)
                st.session_state.user_profile = profile
                st.rerun()
    st.stop()

# --- 6. MAIN INTERFACE ---
st.header(f"🛡️ {st.session_state.user_profile['name']}")

tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "📸 Scanner", "⚙️ Profile"])

with tab1:
    st.caption(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    if prompt := st.chat_input("How are you feeling?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            if model:
                ctx = f"You are a medical assistant for {st.session_state.user_profile['name']}. If emergency, call {st.session_state.user_profile['emergency']}. Message: {prompt}"
                response = model.generate_content(ctx)
                st.markdown(response.text)
            else:
                st.error("AI Brain not found. Check Secrets.")

with tab2:
    st.subheader("Medicine Scanner")
    st.camera_input("Scan your medicine")

with tab3:
    st.subheader("Profile")
    st.write(f"**Emergency:** {st.session_state.user_profile['emergency']}")
    if st.button("🗑️ Reset All Data"):
        if os.path.exists(USER_FILE): os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
