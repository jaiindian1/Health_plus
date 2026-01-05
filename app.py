import streamlit as st
import google.generativeai as genai

# --- 1. THE ARCHITECT'S INTERFACE ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# Improved CSS + Manifest Linking
st.markdown("""
    <head>
        <link rel="manifest" href="./manifest.json?v=1">
        <meta name="theme-color" content="#FF4B4B">
    </head>
    <style>
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        .stDeployButton {display:none !important;}
        #viewer-badge {display: none !important;}
        /* The Mobile Phone look */
        .stApp { 
            max-width: 450px; 
            margin: 0 auto; 
            border-left: 1px solid #f0f0f0; 
            border-right: 1px solid #f0f0f0;
        }
    </style>
    """, unsafe_allow_html=True)

# AI CONFIG
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("Missing API Key!")

# --- 2. LOGIC & STATE ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- 3. THE SETUP FORM ---
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

# --- 4. THE MAIN INTERFACE ---
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
            except:
                st.warning("⚠️ AI is busy. Please wait 10 seconds.")

with tab2:
    st.camera_input("Scan your medicine")
