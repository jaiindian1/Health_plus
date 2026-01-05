import streamlit as st
import google.generativeai as genai

# --- 1. DESIGN & IDENTITY ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .stApp { max-width: 450px; margin: 0 auto; }
    </style>
    <link rel="manifest" href="./manifest.json?v=3">
    """, unsafe_allow_html=True)

# --- 2. AI CONFIG ---
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Missing API_KEY in Streamlit Secrets!")

# --- 3. USER STATE ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- 4. THE SETUP FORM ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        emergency = st.text_input("Emergency No.")
        if st.form_submit_button("Save & Start"):
            if name and phone and emergency:
                st.session_state.user_profile = {"name": name, "phone": phone, "emergency": emergency}
                st.rerun()
    st.stop()

# --- 5. MAIN INTERFACE ---
st.header(f"🛡️ {st.session_state.user_profile['name']}")

tab1, tab2 = st.tabs(["💬 Chat", "📸 Scanner"])

with tab1:
    st.caption(f"Emergency Contact: {st.session_state.user_profile['emergency']}")
    if prompt := st.chat_input("Tell me how you feel..."):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except Exception as e:
                # THIS IS THE TRUTH MICROPHONE
                st.error(f"Developer Log: {e}")

with tab2:
    st.camera_input("Scan your medicine")
    if st.button("🔄 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()
