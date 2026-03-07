import streamlit as st
import os
import sys

# 1. PAGE CONFIG
st.set_page_config(page_title="Risk Suite", page_icon="🎯", layout="wide")

# --- AGGRESSIVE CSS STRIPPER & CUSTOM CARDS ---
st.markdown("""
    <style>
        header { display: none !important; }
        footer { display: none !important; }
        .block-container { padding-top: 0rem !important; margin-top: -1rem !important; }
        
        .suite-card {
            background: white; border: 1px solid #e2e8f0; padding: 20px;
            border-radius: 10px; height: 120px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        }
        .suite-card h3 { margin-top: 0px; margin-bottom: 5px; color: #1E3A8A; font-size: 20px;}
        .suite-card p { color: #4b5563; font-size: 14px; line-height: 1.4; margin-bottom: 0px;}
        
        /* CORRECTED HTML BUTTON: Applied directly to the 'a' tag */
        .html-back-btn {
            background-color: white; border: 1px solid rgba(49, 51, 63, 0.2); 
            border-radius: 0.5rem; padding: 0.35rem 0.85rem; color: #31333F; 
            cursor: pointer; font-size: 1rem; margin-bottom: 1rem; transition: 0.2s;
            text-decoration: none; display: inline-block; font-weight: 600;
        }
        .html-back-btn:hover { border-color: #ff4b4b; color: #ff4b4b; text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# 2. LOCAL IMPORTS
try:
    from modules.risk_prediction import run_risk_module
    from modules.ai_counselor import run_ai_counselor
    from modules.progress_tracking import run_progress_tracking 
except Exception as e:
    st.error(f"Import Error: {e}")
    st.stop()

# 3. NAVIGATION STATE
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'MySuite'

def navigate(view_name):
    st.session_state.current_view = view_name
    st.rerun()

# --- 4. YOUR SUB-PORTAL ---
if st.session_state.current_view == 'MySuite':
    
    # 🚀 THE BREAKOUT BUTTON: Only appears on this main component page!
    st.markdown("""
        <a href="http://localhost:8501" target="_top" style="
            background-color: #3b82f6; color: white; padding: 0.5rem 1rem; 
            border-radius: 0.5rem; text-decoration: none; font-weight: 600; 
            display: inline-block; margin-bottom: 1rem; border: none; cursor: pointer;">
            🏠 Main Lobby
        </a>
    """, unsafe_allow_html=True)

    st.markdown("## 🎯 Risk Prediction & Intervention Suite")
    st.write("Welcome to the specialized lab for student dropout prevention and clinical goal setting.")
    st.divider()
    
    card1, card2, card3 = st.columns(3)
    with card1: st.markdown('<div class="suite-card"><h3>🔍 Risk Diagnostic</h3><p>Analyze 73 behavioral variables and simulate recovery paths.</p></div>', unsafe_allow_html=True)
    with card2: st.markdown('<div class="suite-card"><h3>🤖 AI Counselor</h3><p>Consult the LLM Clinical assistant for intervention advice.</p></div>', unsafe_allow_html=True)
    with card3: st.markdown('<div class="suite-card"><h3>📈 Progress Tracking</h3><p>Analyze the gap between actual performance and locked goals.</p></div>', unsafe_allow_html=True)
        
    st.write("") 
    btn1, btn2, btn3 = st.columns(3)
    
    with btn1:
        if st.button("Launch Diagnostic", use_container_width=True):
            st.session_state.active_tool = 'Risk'
            navigate('Tool')
    with btn2:
        if st.button("Launch AI Bot", use_container_width=True):
            st.session_state.active_tool = 'Counselor'
            navigate('Tool')
    with btn3:
        if st.button("Launch Tracker", use_container_width=True):
            st.session_state.active_tool = 'Tracking'
            navigate('Tool')

# --- 5. YOUR TOOLS ---
elif st.session_state.current_view == 'Tool':
    
    # Native Streamlit button to go back ONE step to your Suite Portal
    if st.button("«", help="Back to Risk Suite Portal"): 
        navigate('MySuite')
        
    st.divider()
    
    if st.session_state.active_tool == 'Risk':
        run_risk_module()
    elif st.session_state.active_tool == 'Counselor':
        run_ai_counselor()
    elif st.session_state.active_tool == 'Tracking':
        run_progress_tracking()