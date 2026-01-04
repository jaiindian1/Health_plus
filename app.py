import streamlit as st
import google.generativeai as genai

# 1. Page Config (This makes it look like an app)
st.set_page_config(page_title="HealthPlus Pill Scanner", page_icon="💊")

# 2. The Header
st.title("💊 Project Health Plus")
st.write("Scan your medicine bottle to understand your prescription.")

# 3. The Camera Input (The SaaS "Action" button)
picture = st.camera_input("Take a photo of the pill/label")

if picture:
    st.image(picture, caption="Uploaded Image")
    st.write("🔍 Analyzing with Gemini AI...")
    # (We will add the AI logic here in the next step!)