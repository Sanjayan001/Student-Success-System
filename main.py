import streamlit as st
import streamlit.components.v1 as components

# --- 0. PAGE CONFIG MUST BE FIRST ---
st.set_page_config(page_title="Student Success Ecosystem", page_icon="🎓", layout="wide")

# --- 1. STYLING (The "Apple" Look) ---
st.markdown("""
    <style>
    .main-title { font-size: 55px; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 5px; margin-top: -20px;}
    .sub-title { font-size: 20px; text-align: center; color: #64748b; margin-bottom: 40px; }
    .card {
        background: white; border: 1px solid #e2e8f0; padding: 25px;
        border-radius: 20px; text-align: center; transition: 0.3s;
        height: 320px; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
    }
    .card h2 { font-size: 24px !important; line-height: 1.3; margin-bottom: 12px; margin-top: 0px; }
    .card:hover { transform: translateY(-10px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #3b82f6; }
    .icon { font-size: 60px; margin-bottom: 10px; margin-top: 5px;}
    </style>
""", unsafe_allow_html=True)

# --- 2. THE NAVIGATION ENGINE ---
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'Lobby'

def navigate(view_name):
    st.session_state.current_view = view_name
    st.rerun()

# --- 3. LAYER 1: THE GRAND LOBBY (HOME PAGE) ---
if st.session_state.current_view == 'Lobby':
    st.markdown('<div class="main-title">🎓 Student Success System</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Integrated Research Framework | 2026 Batch</div>', unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card"><div class="icon">🔍</div><h2>Risk & Intervention</h2><p>Predictive Modeling, AI Counseling, and Progress Tracking</p></div>', unsafe_allow_html=True)
        # This stays on the same page and triggers the IFrame!
        if st.button("Enter Risk Suite", use_container_width=True):
            navigate('Risk_Suite')

    with col2:
        st.markdown('<div class="card"><div class="icon">📊</div><h2>Student Profiling</h2><p>Member B: Grading Trends and Enrollment Analysis</p></div>', unsafe_allow_html=True)
        if st.button("Enter Profiling Suite", use_container_width=True):
            st.info("Module under development by Mr. Nazib.")

    with col3:
        st.markdown('<div class="card"><div class="icon">🤝</div><h2>Course Recommendation</h2><p>Member C: Student Engagement and Wellbeing Indices</p></div>', unsafe_allow_html=True)
        # Activating Malshika's Doorway!
        if st.button("Enter Course Rec Suite", use_container_width=True):
            navigate('Course_Rec_Suite')

# --- 4. LAYER 2: THE EMBEDDED IFRAMES ---
elif st.session_state.current_view == 'Risk_Suite':
    
    with st.spinner("Connecting to Risk Prediction Core..."):
        # We use a raw HTML iframe here to inject the 'allow-top-navigation' security bypass!
        st.markdown("""
            <iframe src="http://localhost:8502/?embed=true" 
                    width="100%" 
                    height="850px" 
                    style="border:none; margin:0; padding:0; overflow:hidden;"
                    sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
            </iframe>
        """, unsafe_allow_html=True)

elif st.session_state.current_view == 'Course_Rec_Suite':
    with st.spinner("Connecting to Course Recommendation Engine..."):
        st.markdown("""
            <iframe src="http://localhost:8504/?embed=true" 
                    width="100%" 
                    height="850px" 
                    style="border:none; margin:0; padding:0; overflow:hidden;"
                    sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
            </iframe>
        """, unsafe_allow_html=True)