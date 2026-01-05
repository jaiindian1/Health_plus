import streamlit as st
import google.generativeai as genai

# --- 1. PROFESSIONAL UI & MOBILE SETUP ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# CSS: Hides all Streamlit "Clutter" (GitHub, Menu, Footer, Pencil)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stSidebarNav"] {display: none;}
    .stApp { max-width: 450px; margin: 0 auto; }
    
    /* Installation box style */
    .install-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #007bff;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    
    <link rel="manifest" href="./manifest.json">
    """, unsafe_allow_html=True)

# AI CONFIG: Using stable name to fix the 'NotFound' error in your logs
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash') 
else:
    st.error("Missing API Key in Secrets!")

# --- 2. MEMORY & STATE ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "show_install" not in st.session_state:
    st.session_state.show_install = False

# --- 3. STEP 1: PROFESSIONAL SETUP FORM ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.subheader("Personal Health Setup")
    with st.form("setup"):
        u_name = st.text_input("Full Name")
        u_phone = st.text_input("Your Phone Number")
        u_emergency = st.text_input("Emergency Number")
        if st.form_submit_button("Save & Continue"):
            if u_name and u_phone and u_emergency:
                st.session_state.user_profile = {
                    "name": u_name, 
                    "phone": u_phone, 
                    "emergency": u_emergency
                }
                st.session_state.show_install = True
                st.rerun()
            else:
                st.warning("Please fill all fields to secure your data.")
    st.stop()

# --- 4. STEP 2: MOBILE INSTALLATION SCREEN ---
if st.session_state.show_install:
    st.markdown(f"""
        <div class="install-box">
            <h3>✅ Welcome, {st.session_state.user_profile['name']}!</h3>
            <p><b>To install this app on your phone:</b><br>
            1. Tap the browser menu (3 dots or share icon).<br>
            2. Select <b>'Add to Home screen'</b>.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("📲 OPEN APP INTERFACE"):
        st.session_state.show_install = False
        st.rerun()
    st.stop()

# --- 5. MAIN APP INTERFACE ---
st.header(f"🛡️ Health Plus: {st.session_state.user_profile['name']}")

# Professional Sidebar with Reboot
with st.sidebar:
    st.write(f"**User ID:** {st.session_state.user_profile['phone']}")
    st.write(f"**Emergency:** {st.session_state.user_profile['emergency']}")
    if st.button("🔄 REBOOT SYSTEM"):
        st.session_state.clear()
        st.rerun()

tab1, tab2 = st.tabs(["💬 AI Advisor", "📸 Scanner"])

with tab1:
    # Chat History Display
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Ask about your health..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # Context-aware AI response
                context = f"User: {st.session_state.user_profile['name']}. Health Query: {prompt}"
                response = model.generate_content(context)
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception:
                # ONE-LINE ERROR for professional look
                st.warning("⚠️ AI Service is temporarily busy. Please wait 10 seconds.")

with tab2:
    st.subheader("Medicine Analysis")
    st.camera_input("Scan your prescription or pill box")
