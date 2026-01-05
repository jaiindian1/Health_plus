import streamlit as st
import google.generativeai as genai

# --- 1. FULL INTERFACE CLEANUP ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# CSS: This is the "Invisibility Cloak" for all Streamlit branding
st.markdown("""
    <style>
    /* Hides the top header (GitHub, Menu, etc.) */
    header {visibility: hidden !important;}
    /* Hides the footer */
    footer {visibility: hidden !important;}
    /* Hides the Deploy button */
    .stDeployButton {display:none !important;}
    /* Hides the small pencil and manage app button */
    #viewer-badge {display: none !important;}
    /* Centers the app and makes it look like a phone */
    .stApp { 
        max-width: 450px; 
        margin: 0 auto; 
        border-left: 1px solid #f0f0f0; 
        border-right: 1px solid #f0f0f0;
    }
    /* Styles the Install button */
    .install-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #FF4B4B;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    
    <link rel="manifest" href="./manifest.json">
    """, unsafe_allow_html=True)

# AI CONFIG - Using stable model name
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

# Sidebar for Reboot (hidden by default CSS, accessible if needed)
with st.sidebar:
    if st.button("🔄 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()

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
