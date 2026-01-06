import streamlit as st
import google.generativeai as genai

# --- 1. DESIGN & IDENTITY ---
st.set_page_config(page_title="Health Plus", layout="centered", page_icon="💊")

# The "Invisibility Cloak" (Hides Streamlit menus for a clean mobile look)
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display:none !important;}
    .stApp { max-width: 450px; margin: 0 auto; }
    </style>
    <link rel="manifest" href="./manifest.json?v=6">
    """, unsafe_allow_html=True)

# --- 2. AI CONFIG (THE DIAGNOSTIC BRAIN) ---
if "API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["API_KEY"])
        
        # This part asks Google exactly which models your key can use
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        model_found = False
        # We search for our preferred models in your allowed list
        for target in ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.5-flash-latest']:
            if target in available_models:
                model = genai.GenerativeModel(target)
                model_found = True
                break
        
        # If our favorites aren't there, we grab the first one that exists
        if not model_found and available_models:
            model = genai.GenerativeModel(available_models[0])
            model_found = True
            
    except Exception as e:
        st.error(f"Configuration Error: {e}")
else:
    st.error("Missing API_KEY in Streamlit Secrets!")

# --- 3. USER STATE ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- 4. THE SETUP FORM ---
if st.session_state.user_profile is None:
    st.title("🏥 Health Plus")
    st.write("Please set up your profile to begin.")
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
        with st.chat_message("user"): 
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                # We add context so the AI knows who it is talking to
                full_prompt = f"User: {st.session_state.user_profile['name']}. Message: {prompt}"
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI Error: {e}")

with tab2:
    st.subheader("Medicine Scanner")
    st.camera_input("Scan your medicine")
    
    st.divider()
    if st.button("🔄 RESET PROFILE"):
        st.session_state.clear()
        st.rerun()
