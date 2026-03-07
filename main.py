# import streamlit as st
# import streamlit.components.v1 as components

# # --- 0. PAGE CONFIG MUST BE FIRST ---
# st.set_page_config(page_title="Student Success Ecosystem", page_icon="🎓", layout="wide")

# # --- 1. STYLING (The "Apple" Look) ---
# st.markdown("""
#     <style>
#     .main-title { font-size: 55px; font-weight: 900; color: #1E3A8A; text-align: center; margin-bottom: 5px; margin-top: -20px;}
#     .sub-title { font-size: 20px; text-align: center; color: #64748b; margin-bottom: 40px; }
#     .card {
#         background: white; border: 1px solid #e2e8f0; padding: 25px;
#         border-radius: 20px; text-align: center; transition: 0.3s;
#         height: 320px; 
#         display: flex;
#         flex-direction: column;
#         justify-content: flex-start;
#         align-items: center;
#     }
#     .card h2 { font-size: 24px !important; line-height: 1.3; margin-bottom: 12px; margin-top: 0px; }
#     .card:hover { transform: translateY(-10px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #3b82f6; }
#     .icon { font-size: 60px; margin-bottom: 10px; margin-top: 5px;}
#     </style>
# """, unsafe_allow_html=True)

# # --- 2. THE NAVIGATION ENGINE ---
# if 'current_view' not in st.session_state:
#     st.session_state.current_view = 'Lobby'

# def navigate(view_name):
#     st.session_state.current_view = view_name
#     st.rerun()

# # --- 3. LAYER 1: THE GRAND LOBBY (HOME PAGE) ---
# if st.session_state.current_view == 'Lobby':
#     st.markdown('<div class="main-title">🎓 Student Success System</div>', unsafe_allow_html=True)
#     st.markdown('<div class="sub-title">Integrated Research Framework | 2026 Batch</div>', unsafe_allow_html=True)
#     st.divider()

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown('<div class="card"><div class="icon">🔍</div><h2>Risk & Intervention</h2><p>Predictive Modeling, AI Counseling, and Progress Tracking</p></div>', unsafe_allow_html=True)
#         if st.button("Enter Risk Suite", width="stretch"):
#             navigate('Risk_Suite')

#     with col2:
#         st.markdown('<div class="card"><div class="icon">📊</div><h2>Student Profiling</h2><p>Member B: Grading Trends and Enrollment Analysis</p></div>', unsafe_allow_html=True)
#         if st.button("Enter Profiling Suite", width="stretch"):
#             navigate('Profiling_Suite') # Added navigation for Profiling

#     with col3:
#         st.markdown('<div class="card"><div class="icon">🤝</div><h2>Course Recommendation</h2><p>Member C: Student Engagement and Wellbeing Indices</p></div>', unsafe_allow_html=True)
#         if st.button("Enter Course Rec Suite", width="stretch"):
#             navigate('Course_Rec_Suite')

# # Move the Main Lobby button to the Sidebar so it doesn't clash with the iframe UI!
#     # Adds a tiny bit of space between the button and the iframe
#     st.write("")


# # --- 4. LAYER 2: THE EMBEDDED IFRAMES ---

# # # Restore the Main Lobby button ONLY for Profiling and Course Rec suites
# # if st.session_state.current_view in ['Profiling_Suite', 'Course_Rec_Suite']:
# #     if st.button("🏠 Main Lobby", type="primary"):
# #         navigate('Lobby')
# #     st.write("") # Adds a tiny spacer below the button

# # Restore the Main Lobby button ONLY for Profiling and Course Rec suites
# if st.session_state.current_view in ['Profiling_Suite', 'Course_Rec_Suite']:
    
#     # Inject your custom CSS specifically for this Streamlit button
#     st.markdown("""
#         <style>
#         div[data-testid="stButton"] > button {
#             background-color: #3b82f6 !important; 
#             color: white !important; 
#             padding: 0.5rem 1rem !important; 
#             border-radius: 0.5rem !important; 
#             font-weight: 600 !important; 
#             border: none !important;
#         }
#         div[data-testid="stButton"] > button:hover {
#             background-color: #2563eb !important; /* A slightly darker blue for the hover effect */
#             color: white !important;
#             border: none !important;
#         }
#         </style>
#     """, unsafe_allow_html=True)

#     # Note: Removed type="primary" because our CSS is now taking full control!
#     if st.button("🏠 Main Lobby"):
#         navigate('Lobby')
        
#     st.write("") # Adds a tiny spacer below the button

# if st.session_state.current_view == 'Risk_Suite':
#     with st.spinner("Connecting to Risk Prediction Core..."):
#         st.markdown("""
#             <iframe src="http://localhost:8502/?embed=true" 
#                     width="100%" 
#                     height="850px" 
#                     style="border:none; margin:0; padding:0; overflow:hidden;"
#                     sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
#             </iframe>
#         """, unsafe_allow_html=True)

# elif st.session_state.current_view == 'Profiling_Suite':
#     with st.spinner("Connecting to Student Profiling Engine..."):
#         st.markdown("""
#             <iframe src="http://localhost:8504/?embed=true" 
#                     width="100%" 
#                     height="850px" 
#                     style="border:none; margin:0; padding:0; overflow:hidden;"
#                     sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
#             </iframe>
#         """, unsafe_allow_html=True)

# elif st.session_state.current_view == 'Course_Rec_Suite':
#     with st.spinner("Connecting to Course Recommendation Engine..."):
#         st.markdown("""
#             <iframe src="http://localhost:8503/?embed=true" 
#                     width="100%" 
#                     height="850px" 
#                     style="border:none; margin:0; padding:0; overflow:hidden;"
#                     sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
#             </iframe>
#         """, unsafe_allow_html=True)


import streamlit as st
import streamlit.components.v1 as components

# --- 0. PAGE CONFIG MUST BE FIRST ---
st.set_page_config(page_title="Student Success Ecosystem", page_icon="🎓", layout="wide")

# --- 1. STYLING (The High-End Interactive SaaS Look) ---
st.markdown("""
    <style>
    /* Subtle modern background for the whole app */
    .stApp {
        background: radial-gradient(circle at top left, #f8fafc, #ffffff 40%, #eff6ff 100%);
    }

    /* Clean up the main container width and top padding */
    .block-container { 
        max-width: 1200px; 
        padding-top: 3rem !important; 
    }

    /* Keyframe Animations */
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(30px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Animated Gradient Title */
    .main-title { 
        font-size: 3.8rem; 
        font-weight: 900; 
        background: linear-gradient(-45deg, #1E3A8A, #3b82f6, #0284c7, #1E3A8A); 
        background-size: 300% auto;
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        text-align: center; 
        margin-bottom: 0.5rem; 
        margin-top: -20px;
        letter-spacing: -1.5px;
        animation: gradientShift 6s ease infinite, fadeUp 0.8s ease-out;
    }
    
    /* Professional Subtitle */
    .sub-title { 
        font-size: 1.1rem; 
        text-align: center; 
        color: #64748b; 
        margin-bottom: 4rem; 
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 3px;
        animation: fadeUp 1s ease-out;
    }

    /* Elevated, Interactive Cards */
    .card {
        background: rgba(255, 255, 255, 0.7); 
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-top: 4px solid #bae6fd; /* Sleek top border accent */
        padding: 2.5rem 1.5rem;
        border-radius: 20px; 
        text-align: center; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 350px; 
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025);
        animation: fadeUp 1.2s ease-out;
    }
    
    /* Cursor Hover Dynamics for Cards */
    .card:hover { 
        transform: translateY(-15px); 
        box-shadow: 0 25px 50px -12px rgba(59, 130, 246, 0.25); 
        border-color: #3b82f6;
        border-top: 4px solid #3b82f6;
        background: #ffffff;
    }

    /* Circular Background for Icons */
    .icon { 
        width: 85px;
        height: 85px;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.04), 0 4px 8px rgba(59, 130, 246, 0.1);
        border: 2px solid #bae6fd;
        font-size: 38px; 
        transition: all 0.5s ease; /* Icon reacts to cursor */
    }

    /* Icon Animation when card is hovered */
    .card:hover .icon {
        transform: scale(1.15) rotate(5deg);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.04), 0 8px 16px rgba(59, 130, 246, 0.3);
        border-color: #60a5fa;
    }

    /* Card Text Alignment */
    .card h2 { 
        font-size: 1.6rem !important; 
        color: #0f172a; 
        font-weight: 800; 
        line-height: 1.3; 
        margin-bottom: 1rem; 
        margin-top: 0px; 
        transition: color 0.3s ease;
    }
    .card:hover h2 {
        color: #1E3A8A; /* Text darkens beautifully on hover */
    }
    
    .card p { 
        color: #475569; 
        font-size: 1.05rem; 
        line-height: 1.6;
        margin: 0;
    }

    /* Base Styling for the Suite "Launch" Buttons */
    div[data-testid="stButton"] > button {
        border-radius: 10px !important;
        font-weight: 700 !important;
        border: 2px solid #e2e8f0 !important;
        background-color: #ffffff !important;
        color: #334155 !important;
        transition: all 0.3s ease !important;
        animation: fadeUp 1.4s ease-out;
    }
    
    /* Button reacts to cursor */
    div[data-testid="stButton"] > button:hover {
        border-color: #3b82f6 !important;
        background-color: #f0f9ff !important;
        color: #2563eb !important;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
    }
    
    /* Sleek Horizontal Rule */
    hr { margin-top: 2rem; margin-bottom: 3rem; border-color: #cbd5e1; }
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
        if st.button("Enter Risk Suite", width="stretch"):
            navigate('Risk_Suite')

    with col2:
        st.markdown('<div class="card"><div class="icon">📊</div><h2>Student Profiling</h2><p>Member B: Grading Trends and Enrollment Analysis</p></div>', unsafe_allow_html=True)
        if st.button("Enter Profiling Suite", width="stretch"):
            navigate('Profiling_Suite') # Added navigation for Profiling

    with col3:
        st.markdown('<div class="card"><div class="icon">🤝</div><h2>Course Recommendation</h2><p>Member C: Student Engagement and Wellbeing Indices</p></div>', unsafe_allow_html=True)
        if st.button("Enter Course Rec Suite", width="stretch"):
            navigate('Course_Rec_Suite')

    # Adds a tiny bit of space between the button and the iframe
    st.write("")


# --- 4. LAYER 2: THE EMBEDDED IFRAMES ---

# Restore the Main Lobby button ONLY for Profiling and Course Rec suites
if st.session_state.current_view in ['Profiling_Suite', 'Course_Rec_Suite']:
    
    # Inject your custom CSS specifically for this "Master" Streamlit button
    st.markdown("""
        <style>
        div[data-testid="stButton"] > button {
            background-color: #3b82f6 !important; 
            color: white !important; 
            padding: 0.6rem 1.2rem !important; 
            border-radius: 8px !important; 
            font-weight: 600 !important; 
            border: none !important;
            box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2) !important;
            animation: none !important; /* Prevents double animation on inner pages */
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #2563eb !important; /* A slightly darker blue for the hover effect */
            color: white !important;
            border: none !important;
            box-shadow: 0 6px 10px rgba(59, 130, 246, 0.3) !important;
            transform: scale(1.02);
        }
        </style>
    """, unsafe_allow_html=True)

    # Note: Removed type="primary" because our CSS is now taking full control!
    if st.button("🏠 Main Lobby"):
        navigate('Lobby')
        
    st.write("") # Adds a tiny spacer below the button

if st.session_state.current_view == 'Risk_Suite':
    with st.spinner("Connecting to Risk Prediction Core..."):
        st.markdown("""
            <iframe src="http://localhost:8502/?embed=true" 
                    width="100%" 
                    height="850px" 
                    style="border:none; margin:0; padding:0; overflow:hidden;"
                    sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
            </iframe>
        """, unsafe_allow_html=True)

elif st.session_state.current_view == 'Profiling_Suite':
    with st.spinner("Connecting to Student Profiling Engine..."):
        st.markdown("""
            <iframe src="http://localhost:8504/?embed=true" 
                    width="100%" 
                    height="850px" 
                    style="border:none; margin:0; padding:0; overflow:hidden;"
                    sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
            </iframe>
        """, unsafe_allow_html=True)

elif st.session_state.current_view == 'Course_Rec_Suite':
    with st.spinner("Connecting to Course Recommendation Engine..."):
        st.markdown("""
            <iframe src="http://localhost:8503/?embed=true" 
                    width="100%" 
                    height="850px" 
                    style="border:none; margin:0; padding:0; overflow:hidden;"
                    sandbox="allow-scripts allow-same-origin allow-top-navigation allow-forms allow-popups">
            </iframe>
        """, unsafe_allow_html=True)