import streamlit as st
from modules.risk_prediction import run_risk_module
from modules.ai_counselor import run_ai_counselor
from modules.progress_tracking import run_progress_tracking  # <--- 1. NEW IMPORT

# 1. GLOBAL PAGE CONFIG
st.set_page_config(
    page_title="Student Success Intelligence",
    page_icon="🎓",
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. CUSTOM CSS FOR BRANDING
st.markdown("""
    <style>
    .main-header {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #1E3A8A;
        margin-bottom: 20px;
    }
    .sidebar-brand {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        padding-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">🏛️ Success Portal</div>', unsafe_allow_html=True)
        st.divider()
        
        # We updated the list to match your professional names
        page = st.radio(
            "Intelligence Modules",
            ["Risk Diagnostic", "AI Counselor Bot", "Progress Tracking"], # <--- 2. UPDATED NAME
            index=0
        )
        
        st.sidebar.divider()
        st.sidebar.caption("v3.1 Build | Gemini 3.0 Integrated")

    # --- PAGE ROUTING ---
    if page == "Risk Diagnostic":
        run_risk_module()
        
    elif page == "AI Counselor Bot":
        run_ai_counselor()
        
    elif page == "Progress Tracking": # <--- 3. LINKED TO REAL MODULE
        run_progress_tracking()

if __name__ == "__main__":
    main()