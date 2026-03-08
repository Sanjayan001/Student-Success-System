# import streamlit as st
# import pandas as pd
# from google import genai  # Switching to the NEW 2026 SDK
# from google.genai import types
# #import google.generativeai as genai
# import os
# import time
# from datetime import datetime

# # --- DATABASE PATH ---
# DB_PATH = os.path.join("database", "student_success.db")

# def run_ai_counselor():
#     st.markdown("# 🤖 Hyper-Personalized AI Counselor")
#     st.caption("Strategic Intervention Engine v3.1 | Powered by Gemini 3.0 Flash")
    
#     # --- 1. SECURITY VAULT (API KEY) ---
#     # --- 1. SECURITY VAULT (API KEY & CLIENT) ---
#     try:
#         # Check if the client is already alive. If not, build it and save it.
#         if "gemini_client" not in st.session_state:
#             api_key = st.secrets["GEMINI_API_KEY"]
#             st.session_state.gemini_client = genai.Client(api_key=api_key)
        
#         # Always use the persistent client
#         client = st.session_state.gemini_client
        
#     except KeyError:
#         st.error("🔒 Security Vault Locked: Could not find 'GEMINI_API_KEY' in your secrets.toml file.")
#         st.stop()
#     except Exception as e:
#         st.error(f"⚠️ Initialization Error: {e}")
#         st.stop()

#     # Initialize session state variables
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
#     if "current_mood" not in st.session_state:
#         st.session_state.current_mood = "Neutral"

#     # --- 2. SIDEBAR: CLINICAL DASHBOARD ---
#     with st.sidebar:
#         st.markdown("### 📊 Session Intelligence")
#         st.write("🟢 **Gemini Core:** Linked & Active")

#         default_id = st.session_state.get('last_student_id', "STU-001")
#         student_id = st.text_input("Sync Student ID:", value=default_id)
        
#         mood_colors = {"Positive": "🟢", "Neutral": "⚪", "Frustrated": "🟠", "Anxious": "🔴", "Defeated": "💀"}
#         st.markdown(f"**Student Vitals:** {mood_colors.get(st.session_state.current_mood, '⚪')} {st.session_state.current_mood}")
        
#         st.divider()
#         if st.button("Clear Session History"):
#             st.session_state.chat_history = []
#             st.session_state.current_mood = "Neutral"
#             st.rerun()

#     # --- 3. CONTEXT HANDOVER LOGIC ---
#     live_data = st.session_state.get('last_run_data')
    
#     if student_id and live_data and st.session_state.get('last_student_id') == student_id:
#         risk_status = live_data.get('status', 'High Risk')
#         risk_prob = live_data.get('risk_score', 0.5)
        
#         st.success(f"⚡ **Live-Sync Active:** Information for {student_id} inherited.")
        
#         # 1. First, we DEFINE the instruction
#         system_instruction = f"""
#         SYSTEM ROLE: Professional University Counselor.
#         STUDENT ID: {student_id} | RISK: {risk_status} ({risk_prob:.4f})
#         PROTOCOL: Use clinical empathy. Reference diagnostic trajectories (Sleep/Motivation).
#         """
        
#         # --- INITIALIZE CHAT MEMORY ---
#         if "chat_session" not in st.session_state:
#             st.session_state.chat_session = client.chats.create(
#                 model="gemini-3-flash-preview",
#                 config=types.GenerateContentConfig(
#                     system_instruction=system_instruction,
#                     temperature=0.7,
#                 )
#             )
            

#         # 3. Display Chat History
#         for message in st.session_state.chat_history:
#             with st.chat_message(message["role"]):
#                 st.markdown(message["content"])

#         # --- 4. THE INTERACTION ENGINE ---
#         if prompt := st.chat_input("How can I support your academic journey today?"):
            
#             st.session_state.chat_history.append({"role": "user", "content": prompt})
#             with st.chat_message("user"):
#                 st.markdown(prompt)

#             with st.chat_message("assistant"):
#                 try:
#                     # STEP A: SENTIMENT ANALYSIS (New SDK Style)
#                     mood_check = client.models.generate_content(
#                         model="gemini-3-flash-preview", # Using the latest 2026 model
#                         contents=f"Analyze sentiment: '{prompt}'. Return one word: Positive, Neutral, Frustrated, Anxious, or Defeated."
#                     )
#                     st.session_state.current_mood = "".join(filter(str.isalpha, mood_check.text.strip()))

#                     # STEP B: REAL-TIME STREAMING RESPONSE
#                     contextual_prompt = f"[STUDENT MOOD DETECTED AS: {st.session_state.current_mood}] \n\n {prompt}"
                    
#                     response_stream = st.session_state.chat_session.send_message_stream(contextual_prompt)
                    
#                     def generate_chunks():
#                         for chunk in response_stream:
#                             if chunk.text:
#                                 yield chunk.text
                    
#                     # Streamlit handles writing it live natively!
#                     full_response = st.write_stream(generate_chunks())
#                     st.session_state.chat_history.append({"role": "assistant", "content": full_response})

#                     # STEP C: CLINICAL INTERVENTION DASHBOARD
#                     with st.expander("📝 AI Intervention Summary"):
#                         st.write(f"**Risk Priority:** {'🔴 High' if risk_status == 'High Risk' else '🟢 Low'}")
#                         st.write(f"**Current Sentiment:** {st.session_state.current_mood}")
#                         st.info("AI Recommendation: Focus on workload re-prioritization and sleep hygiene based on student's longitudinal trend.")

#                     if st.session_state.current_mood in ["Anxious", "Defeated"]:
#                         st.toast(f"Mood Alert: {st.session_state.current_mood}", icon="⚠️")

#                 except Exception as e:
#                     st.error(f"AI Service Interruption: {e}")
#                     st.info("💡 Solution: Go to Google Cloud Console and click ENABLE on the 'Generative Language API'.")
#     else:
#         st.warning("⚠️ **Waiting for Context:** Please run the 'Risk Diagnostic' first.")












import streamlit as st
import pandas as pd
from google import genai
from google.genai import types, errors
import os
from datetime import datetime

# 🧠 The Auto-Failover Fleet (Using UNIVERSAL hardcoded tags to bypass 404 errors)
# 🧠 The Auto-Failover Fleet (Modern SOTA Models Only)
MODEL_LIST = [
    "gemini-2.5-flash",       # The latest, ultra-fast free-tier champion
    "gemini-2.0-flash",       # The highly stable fallback
    "gemini-2.5-pro"          # The heavy reasoning engine
]

def inject_chatgpt_css():
    st.markdown("""
        <style>
        /* 1. 🚀 THE ULTIMATE IFRAME FIX: UN-PIN THE CHAT BAR */
        div[data-testid="stChatInput"] {
            position: relative !important;
            bottom: auto !important;
            width: 100% !important;
            margin-top: 10px !important;
            padding-bottom: 20px !important;
            background-color: transparent !important;
        }

        /* 2. ChatGPT Zero-State Aesthetic */
        .chatgpt-greeting {
            text-align: center;
            font-size: 2.2rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-top: 5vh;
            letter-spacing: -1px;
        }

        /* 3. The Persona 'Thinking' Animation */
        @keyframes glow { 0% { opacity: 0.5; } 50% { opacity: 1; color: #10a37f; } 100% { opacity: 0.5; } }
        .persona-tag {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 800;
            color: #64748b;
            animation: glow 2s infinite;
            margin-bottom: 10px;
            display: inline-block;
        }

        /* 4. Message Styling */
        .stChatMessage {
            background-color: transparent !important;
            border: none !important;
            padding: 1.2rem 0 !important;
        }
        
        .back-btn-container { margin-bottom: 10px; }
        
        /* Clean up top padding */
        .block-container { padding-top: 1rem !important; max-width: 900px; margin: 0 auto; }
        </style>
    """, unsafe_allow_html=True)

def get_or_create_chat_session(client, system_instruction: str, model_name: str):
    session_key = (model_name, system_instruction)
    
    if st.session_state.get("chat_session_key") != session_key:
        st.session_state.chat_session = client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.75,
                max_output_tokens=1500,
            ),
        )
        st.session_state.chat_session_key = session_key
        
    return st.session_state.chat_session

def clear_chat_session():
    for key in ("chat_session", "chat_session_key"):
        st.session_state.pop(key, None)

def run_ai_counselor():
    inject_chatgpt_css()

    # Initialize Failover Index
    if "active_model_idx" not in st.session_state:
        st.session_state.active_model_idx = 0

    # =====================================================================
    # 🔙 LOCAL NAVIGATION BUTTON
    # =====================================================================
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    if st.button("« Back to Suite Portal", key="counselor_back_btn"):
        st.session_state.current_view = 'MySuite'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    try:
        if "gemini_client" not in st.session_state:
            api_key = st.secrets["GEMINI_API_KEY"]
            st.session_state.gemini_client = genai.Client(api_key=api_key)
        client = st.session_state.gemini_client
    except Exception:
        st.error("🔒 Security Vault Locked: API Key missing in secrets.toml")
        st.stop()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    live_data = st.session_state.get("last_run_data")
    student_id = st.session_state.get("last_student_id", "STU-001")

    # =====================================================================
    # 🗂️ SIDEBAR: LANGUAGE SELECTOR & TELEMETRY
    # =====================================================================
    with st.sidebar:
        st.markdown("<h2 style='font-size:1.1rem;'>Intervention OS</h2>", unsafe_allow_html=True)

        st.divider()
        st.markdown("#### 🗣️ Language Protocol")
        selected_lang = st.selectbox(
            "Primary Chat Language:",
            ["English", "Sinhala (සිංහල)", "Tamil (தமிழ்)"],
            index=0,
            key="counselor_lang_selector"
        )

        if st.button("➕ Reset Session", use_container_width=True):
            st.session_state.chat_history = []
            clear_chat_session()
            st.rerun()

        if live_data:
            st.divider()
            st.metric("Failure Risk Vector", f"{live_data.get('risk_score', 0) * 100:.1f}%")
            st.markdown("#### Expert Personas Active")
            st.caption("🩺 CLINICIAN (Bio-markers)")
            st.caption("🧠 PSYCHOLOGIST (CBT/Mood)")
            st.caption("⚔️ STRATEGIST (Grade Recovery)")
            
            # Show the active model for panel presentation transparency
            st.divider()
            st.caption(f"⚙️ Core Engine: {MODEL_LIST[st.session_state.active_model_idx]}")

    if not live_data:
        st.warning("⚠️ Waiting for Diagnostic Context. Please run the Risk module first.")
        return

    details = live_data.get("details", {})
    risk_status = live_data.get("status", "High Risk")

    # Dynamic Language Logic
    lang_map = {
        "English": "Response Language: English.",
        "Sinhala (සිංහල)": "Response Language: Sinhala (සිංහල බසින් පිළිතුරු සපයන්න).",
        "Tamil (தமிழ்)": "Response Language: Tamil (தமிழ் மொழியில் பதிலளிக்கவும்)."
    }
    lang_instruction = lang_map[selected_lang]
    
    interface_labels = {
        "English": {"input": "Enter strategic query...", "welcome": "What can I help with?"},
        "Sinhala (සිංහල)": {"input": "විමසුම ඇතුළත් කරන්න...", "welcome": "මා ඔබට උදව් කරන්නේ කෙසේද?"},
        "Tamil (தமிழ்)": {"input": "கேள்வியினை உள்ளிடவும்...", "welcome": "நான் உங்களுக்கு எப்படி உதவ முடியும்?"}
    }

    # =====================================================================
    # 🧠 SOTA MULTI-PERSONA SYSTEM PROMPT
    # =====================================================================
    system_instruction = f"""
IDENTITY: You are 'NEURALSYNC-X', a world-class Academic Intervention OS.
ORCHESTRATION: You orchestrate a multi-disciplinary intervention for Student {student_id}.

LANGUAGE PROTOCOL:
- {lang_instruction}
- Translate your entire response, including the [THOUGHT TRACE], into the target language.

STUDENT LIVE DOSSIER:
- Risk Vector: {risk_status}
- Academics: CGPA {details.get('CGPA')}, Attendance {details.get('Attendance_Percentage')}/10
- Biology: Sleep {details.get('Sleep_Hours_Phase4')}/4, Stress {details.get('Stress_Phase4')}/5
- Psychology: Motivation {details.get('Motivation_Phase4')}/5, Confidence {details.get('Confidence_Phase4')}/5

YOUR EXPERT MODULES:
1. CLINICIAN: Analyze bio-markers.
2. PSYCHOLOGIST: Address Confidence/Motivation using CBT.
3. STRATEGIST: Calculate Grade Recovery.
4. CATALYST: Performance coaching.

RESPONSE PROTOCOL:
- Start every message with a [THOUGHT TRACE].
- Tone: Professional High-Performance Coaching.
"""

    chat_box = st.container(height=450, border=False)

    with chat_box:
        if not st.session_state.chat_history:
            st.markdown(f'<div class="chatgpt-greeting">{interface_labels[selected_lang]["welcome"]}</div>', unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center; color:#888;'>Intelligence Synchronized for <b>{student_id}</b></p>", unsafe_allow_html=True)
        else:
            for message in st.session_state.chat_history:
                avatar = "👤" if message["role"] == "user" else "❇️"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])

    # UI prompt adjustment
    if prompt := st.chat_input(interface_labels[selected_lang]["input"]):
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with chat_box:
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="❇️"):
                st.markdown('<div class="persona-tag">Orchestrating Expert Perspectives...</div>', unsafe_allow_html=True)
                placeholder = st.empty()

                success = False
                last_error = ""

                # 🛡️ THE SELF-HEALING ENGINE
                for model_name in MODEL_LIST:
                    try:
                        # Update the UI state to track the active engine
                        st.session_state.active_model_idx = MODEL_LIST.index(model_name)
                        
                        chat_session = get_or_create_chat_session(client, system_instruction, model_name)
                        chunks = []
                        for chunk in chat_session.send_message_stream(prompt):
                            text = getattr(chunk, "text", "")
                            if text:
                                chunks.append(text)
                                placeholder.markdown("".join(chunks))

                        full_response = "".join(chunks).strip()
                        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                        success = True
                        break # Success! Break out of the retry loop.

                    except Exception as e:
                        last_error = str(e)
                        clear_chat_session()
                        # Silently try the next one, updating the placeholder briefly
                        placeholder.markdown(f"*(Testing backup neural pathway: {model_name} failed...)*")

                if not success:
                    placeholder.error("⚠️ All API limits have been temporarily exhausted for this Google Cloud Project.")
                    with st.expander("Show Detailed Error Log"):
                        st.write(last_error)