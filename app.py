import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & MOBILE LINK ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# The "Identity Card" for the app icon
st.markdown('<link rel="manifest" href="./manifest.json">', unsafe_allow_html=True)

# CSS for a clean mobile UI and the Install Box
st.markdown("""
    <style>
    .stApp { max-width: 450px; margin: 0 auto; }
    .install-box { 
        background-color: #fff3f3; 
        padding: 15px; 
        border-radius: 15px; 
        border: 2px solid #FF4B4B;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# AI CONFIG
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("Missing API Key!")

# --- 2. MEMORY ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- 3. THE FORM (Now including Phone Number for tracking) ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup_form"):
        name = st.text_input("Full Name")
        phone = st.text_input("Your Phone Number")
        emergency = st.text_input("Emergency Contact Number")
        
        if st.form_submit_button("Save & Start Tracking"):
            if name and phone and emergency:
                st.session_state.user_profile = {"name": name, "phone": phone, "emergency": emergency}
                # This trigger helps the phone realize it's an app
                st.rerun()
            else:
                st.warning("Please fill all fields to start your pattern tracking!")
    st.stop()

# --- 4. THE INSTALLATION GUIDE ---
# This only shows once to help them get the icon on their screen
if "installed" not in st.session_state:
    st.markdown(f"""
        <div class="install-box">
        <strong>📲 Add to Home Screen, {st.session_state.user_profile['name']}!</strong><br>
        To track your patterns daily, tap your browser menu (⋮) and select <b>'Add to Home screen'</b>.
        </div>
    """, unsafe_allow_html=True)
    if st.button("I have added the icon"):
        st.session_state.installed = True
        st.rerun()

# --- 5. MAIN APP ---
st.header(f"🛡️ Tracking: {st.session_state.user_profile['name']}")
st.write(f"Pattern ID: {st.session_state.user_profile['phone']}")

# Your chat and scanner logic continues here...
