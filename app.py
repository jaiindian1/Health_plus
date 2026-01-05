import streamlit as st
import google.generativeai as genai

# --- 1. DESIGN & IDENTITY ---
# This sets the browser tab name and the little icon in the tab
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# The "Invisibility Cloak" to hide Streamlit buttons and center the app
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .stApp { max-width: 450px; margin: 0 auto; }
    </style>
    <link rel="manifest" href="./manifest.json?v=4">
    """, unsafe_allow_html=True)

# --- 2. AI CONFIG (THE BRAIN) ---
# We use 'gemini-1.5-flash' which is the fastest and most stable
if "API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.error("Missing API_KEY in Streamlit Secrets!")

# --- 3. USER MEMORY ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- 4. THE SETUP FORM (LOGIN) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.write("Please set up your profile to continue.")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        emergency = st.text_input("Emergency Contact Number")
        if st.form_submit_button("Save & Start"):
            if name and phone and emergency:
                st.session_state.user_profile = {"name": name, "phone": phone, "emergency": emergency}
                st.rerun()
            else:
                st.warning("Please fill in all fields!")
    st.stop()

# --- 5. MAIN INTERFACE ---
st.header(f"🛡️ {st.session_state.user_profile['name']}")

tab1, tab2 = st.tabs(["💬 Chat", "📸 Scanner"])

with tab1:
    st.caption(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    
    # Simple Chat Interface
    if prompt := st.chat_input("Tell me how you feel today..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Attempt to get a response from the AI
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                # The 'Truth Microphone' to tell us why Google is failing
                st.error(f"Developer Log: {e}")

with tab2:
    st.write("Use your camera to scan medicine bottles.")
    st.camera_input("Take a photo")
    
    # Reboot Button to clear the profile
    if st.button("🔄 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()
