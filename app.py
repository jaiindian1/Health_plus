import streamlit as st
import google.generativeai as genai

# --- 1. CLEAN INTERFACE & ICON CONFIG ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# CSS: Hides Header, Menu, Footer, and styles the Install Button
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    .stApp { max-width: 450px; margin: 0 auto; }
    
    .install-container {
        background-color: #e6f3ff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #007bff;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    <link rel="manifest" href="./manifest.json">
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
if "install_prompt" not in st.session_state:
    st.session_state.install_prompt = False

# --- 3. STEP 1: SETUP FORM ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus Setup")
    with st.form("setup"):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        emergency = st.text_input("Emergency Number")
        if st.form_submit_button("Save & Start"):
            if name and phone and emergency:
                st.session_state.user_profile = {"name": name, "phone": phone, "emergency": emergency}
                st.session_state.install_prompt = True # Trigger the button
                st.rerun()
    st.stop()

# --- 4. STEP 2: THE INSTALL BUTTON ---
if st.session_state.install_prompt:
    st.markdown(f"""
        <div class="install-container">
            <h3>✅ Profile Saved, {st.session_state.user_profile['name']}!</h3>
            <p>To use this like a real app, install the icon on your screen.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📲 CLICK HERE TO INSTALL ICON"):
        # This gives instructions for the manual browser step
        st.info("Tap your browser menu (3 dots or share) and select 'Add to Home screen'.")
        if st.button("Done! Go to App"):
            st.session_state.install_prompt = False
            st.rerun()
    st.stop()

# --- 5. STEP 3: MAIN APP ---
st.header(f"🛡️ {st.session_state.user_profile['name']}")
if st.button("🔄 REBOOT APP"):
    st.session_state.clear()
    st.rerun()

tab1, tab2 = st.tabs(["💬 AI Advisor", "📸 Scanner"])
with tab1:
    if prompt := st.chat_input("How are you?"):
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
            except:
                st.warning("⚠️ Offline. Try again.")
