import streamlit as st
import os
import sys

# --- 1. SYSTEM BRIDGE ---
current_dir = os.path.dirname(os.path.abspath(__file__))

# A. Tell Python where the 'database' folder lives
component_root = os.path.join(current_dir, "Risk-Prediction")
if component_root not in sys.path:
    sys.path.append(component_root)

# B. Tell Python where the scripts live
my_suite_path = os.path.join(component_root, "modules")
if my_suite_path not in sys.path:
    sys.path.append(my_suite_path)

# --- 2. SYSTEM IMPORTS (Strict Mode) ---
try:
    from risk_prediction import run_risk_module
    from ai_counselor import run_ai_counselor
    from progress_tracking import run_progress_tracking 
except Exception as e:
    st.error(f"🚨 Module Import Failed: {e}")
    st.warning("Path mapping error. Please check your folder structure.")
    st.stop()

# --- 2. THE NAVIGATION ENGINE ---
# Views: 'Lobby' (Home), 'MySuite' (Your 3 tools), 'Tool' (The active script)
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'Lobby'

def navigate(view_name):
    st.session_state.current_view = view_name
    st.rerun()

# --- 3. STYLING (The "Apple" Look) ---
st.set_page_config(page_title="Student Success Ecosystem", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 50px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    .sub-title { font-size: 20px; text-align: center; color: #64748b; margin-bottom: 40px; }
    .card {
        background: white; border: 1px solid #e2e8f0; padding: 30px;
        border-radius: 20px; text-align: center; transition: 0.3s;
    }
    .card:hover { transform: translateY(-10px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #3b82f6; }
    .icon { font-size: 60px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. LAYER 1: THE GRAND LOBBY (HOME PAGE) ---
if st.session_state.current_view == 'Lobby':
    st.markdown('<div class="main-title">🎓 Student Success Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Integrated Research Framework | 2026 Batch</div>', unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card"><div class="icon">🔍</div><h2>Risk & Intervention</h2><p>Predictive Modeling, AI Counseling, and Progress Tracking</p></div>', unsafe_allow_html=True)
        if st.button("Enter Risk Suite", width="stretch", key="enter_my"):
            navigate('MySuite')

    with col2:
        st.markdown('<div class="card"><div class="icon">📊</div><h2>Academic Metrics</h2><p>Member B: Grading Trends and Enrollment Analysis</p></div>', unsafe_allow_html=True)
        if st.button("Enter Member B Suite", width="stretch"):
            st.info("Module under development by Team Member B.")

    with col3:
        st.markdown('<div class="card"><div class="icon">🤝</div><h2>Social Integration</h2><p>Member C: Student Engagement and Wellbeing Indices</p></div>', unsafe_allow_html=True)
        if st.button("Enter Member C Suite", width="stretch"):
            st.info("Module under development by Team Member C.")

# --- 5. LAYER 2: YOUR SUB-PORTAL (MY COMPONENT PAGE) ---
elif st.session_state.current_view == 'MySuite':
    if st.button("⬅️ Back to Grand Lobby"): navigate('Lobby')
    
    st.markdown("## 🎯 Risk Prediction & Intervention Suite")
    st.write("Welcome to the specialized lab for student dropout prevention and clinical goal setting.")
    
    st.divider()
    
    # Your 3 Sub-Modules as Bento Cards
    sub1, sub2, sub3 = st.columns(3)
    
    with sub1:
        with st.container(border=True):
            st.write("### 🔍 Risk Diagnostic")
            st.write("Analyze 73 behavioral variables and simulate recovery paths.")
            if st.button("Launch Diagnostic", width="stretch"):
                st.session_state.active_tool = 'Risk'
                navigate('Tool')

    with sub2:
        with st.container(border=True):
            st.write("### 🤖 AI Counselor")
            st.write("Consult the LLM Clinical assistant for intervention advice.")
            if st.button("Launch AI Bot", width="stretch"):
                st.session_state.active_tool = 'Counselor'
                navigate('Tool')

    with sub3:
        with st.container(border=True):
            st.write("### 📈 Progress Tracking")
            st.write("Analyze the gap between actual performance and locked goals.")
            if st.button("Launch Tracker", width="stretch"):
                st.session_state.active_tool = 'Tracking'
                navigate('Tool')

# --- 6. LAYER 3: THE ACTUAL TOOLS ---
elif st.session_state.current_view == 'Tool':
    if st.button("⬅️ Back to Suite Portal"): navigate('MySuite')
    
    if st.session_state.active_tool == 'Risk':
        run_risk_module()
    elif st.session_state.active_tool == 'Counselor':
        run_ai_counselor()
    elif st.session_state.active_tool == 'Tracking':
        run_progress_tracking()