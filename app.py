import streamlit as st
import google.generativeai as genai
import os

# --- 1. DESIGN & IDENTITY ---
# This changes the browser tab title and the "Logo" to a pill/heart
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="❤️")

# Clean Mobile Look (Hiding Streamlit's default headers)
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .stApp { max-width: 450px; margin: 0 auto; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERSISTENT MEMORY (The "Filing Cabinet") ---
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

# --- 3. AI CONFIG (THE FAST BRAIN) ---
@st.cache_resource
def get_ai_model():
    if "API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["API_KEY"])
        # We try the most stable 2026 model first
        for model_name in ['gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                m.generate_content("test") # Wake up call
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
        if st.form_submit_button("Start Protection"):
            if name and phone and emergency:
                profile = {"name": name, "phone": phone, "emergency": emergency}
                save_user_to_disk(profile)
                st.session_state.user_profile = profile
                st.rerun()
            else:
                st.warning("Please fill all details so I can keep you safe!")
    st.stop()

# --- 6. MAIN INTERFACE ---
st.header(f"🛡️ {st.session_state.user_profile['name']}'s Health")

tab1, tab2, tab3 = st.tabs(["💬 AI Chat", "📸 Scanner", "⚙️ Profile"])

with tab1:
    st.caption(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    
    # Simple Chat logic
    if prompt := st.chat_input("How are you feeling right now?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            if model:
                try:
                    # System instruction inside the prompt
                    context = f"Instruction: You are a medical assistant for {st.session_state.user_profile['name']}. If they mention a life-threatening emergency, tell them to call {st.session_state.user_profile['emergency']} immediately. Message: {prompt}"
                    response = model.generate_content(context)
                    st.markdown(response.text)
                except Exception as e:
                    st.error("The AI Brain is resting. Try again in a minute.")
            else:
                st.error("AI not connected. Check your API Key.")

with tab2:
    st.subheader("Medicine Scanner")
    st.camera_input("Take a photo of your medicine")
    st.info("Scanner will analyze the dose and safety...")

with tab3:
    st.subheader("Profile Settings")
    st.write(f"**Name:** {st.session_state.user_profile['name']}")
    st.write(f"**Phone:** {st.session_state.user_profile['phone']}")
    st.write(f"**Emergency:** {st.session_state.user_profile['emergency']}")
    
    if st.button("🗑️ Log Out / Reset App"):
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)
        st.session_state.clear()
        st.rerun()
