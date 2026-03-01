import streamlit as st
import pandas as pd
from google import genai  # Switching to the NEW 2026 SDK
import os
import time
from datetime import datetime

# --- DATABASE PATH ---
DB_PATH = os.path.join("database", "student_success.db")

def run_ai_counselor():
    st.markdown("# 🤖 Hyper-Personalized AI Counselor")
    st.caption("Strategic Intervention Engine v3.1 | Powered by Gemini 3.0 Flash")
    
    # --- 1. NEW SDK CONFIGURATION ---
    # The new client automatically handles API versioning to prevent 404s
    API_KEY = "AIzaSyDZqVL9fcfnl7vgdsK82ZDsz5bz8RYuEqE" 
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Client Gateway Error: {e}")
        return

    # Initialize session state variables
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_mood" not in st.session_state:
        st.session_state.current_mood = "Neutral"

    # --- 2. SIDEBAR: CLINICAL DASHBOARD ---
    with st.sidebar:
        st.markdown("### 📊 Session Intelligence")
        st.write("🟢 **Gemini Core:** Linked & Active")

        default_id = st.session_state.get('last_student_id', "STU-001")
        student_id = st.text_input("Sync Student ID:", value=default_id)
        
        mood_colors = {"Positive": "🟢", "Neutral": "⚪", "Frustrated": "🟠", "Anxious": "🔴", "Defeated": "💀"}
        st.markdown(f"**Student Vitals:** {mood_colors.get(st.session_state.current_mood, '⚪')} {st.session_state.current_mood}")
        
        st.divider()
        if st.button("Clear Session History"):
            st.session_state.chat_history = []
            st.session_state.current_mood = "Neutral"
            st.rerun()

    # --- 3. CONTEXT HANDOVER LOGIC ---
    live_data = st.session_state.get('last_run_data')
    
    if student_id and live_data and st.session_state.get('last_student_id') == student_id:
        risk_status = live_data.get('status', 'High Risk')
        risk_prob = live_data.get('risk_score', 0.5)
        
        st.success(f"⚡ **Live-Sync Active:** Information for {student_id} inherited.")
        
        system_instruction = f"""
        SYSTEM ROLE: Professional University Counselor.
        STUDENT ID: {student_id} | RISK: {risk_status} ({risk_prob:.4f})
        PROTOCOL: Use clinical empathy. Reference diagnostic trajectories (Sleep/Motivation).
        """

        # Display Chat History
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # --- 4. THE INTERACTION ENGINE ---
        if prompt := st.chat_input("How can I support your academic journey today?"):
            
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    # STEP A: SENTIMENT ANALYSIS (New SDK Style)
                    mood_check = client.models.generate_content(
                        model="gemini-3-flash-preview", # Using the latest 2026 model
                        contents=f"Analyze sentiment: '{prompt}'. Return one word: Positive, Neutral, Frustrated, Anxious, or Defeated."
                    )
                    st.session_state.current_mood = "".join(filter(str.isalpha, mood_check.text.strip()))

                    # STEP B: COUNSELING RESPONSE
                    response = client.models.generate_content(
                        model="gemini-3-flash-preview",
                        contents=f"{system_instruction}\n[MOOD: {st.session_state.current_mood}]\nStudent: {prompt}"
                    )
                    
                    # Professional Typing Animation
                    full_text = response.text
                    placeholder = st.empty()
                    typed_text = ""
                    for word in full_text.split():
                        typed_text += word + " "
                        placeholder.markdown(typed_text + "▌")
                        time.sleep(0.04)
                    placeholder.markdown(full_text)
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": full_text})

                    # STEP C: CLINICAL INTERVENTION DASHBOARD
                    with st.expander("📝 AI Intervention Summary"):
                        st.write(f"**Risk Priority:** {'🔴 High' if risk_status == 'High Risk' else '🟢 Low'}")
                        st.write(f"**Current Sentiment:** {st.session_state.current_mood}")
                        st.info("AI Recommendation: Focus on workload re-prioritization and sleep hygiene based on student's longitudinal trend.")

                    if st.session_state.current_mood in ["Anxious", "Defeated"]:
                        st.toast(f"Mood Alert: {st.session_state.current_mood}", icon="⚠️")

                except Exception as e:
                    st.error(f"AI Service Interruption: {e}")
                    st.info("💡 Solution: Go to Google Cloud Console and click ENABLE on the 'Generative Language API'.")
    else:
        st.warning("⚠️ **Waiting for Context:** Please run the 'Risk Diagnostic' first.")