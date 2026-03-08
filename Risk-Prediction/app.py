# import streamlit as st
# import os
# import sys

# # 1. PAGE CONFIG
# st.set_page_config(page_title="Risk Suite", page_icon="🎯", layout="wide")

# # --- 2. HIGH-END INTERACTIVE CSS ---
# st.markdown("""
#     <style>
#         /* Hide default Streamlit headers and footers */
#         header[data-testid="stHeader"] { 
#             background: transparent !important;
#         }
#         footer { display: none !important; }
        
#         /* Clean up container padding for the iframe */
#         .block-container { 
#             padding-top: 1.5rem !important; 
#             max-width: 1200px;
#         }

#         /* App Background */
#         .stApp {
#             background: radial-gradient(circle at top, #ffffff, #f8fafc 80%);
#         }

#         /* Animations */
#         @keyframes fadeUp {
#             0% { opacity: 0; transform: translateY(20px); }
#             100% { opacity: 1; transform: translateY(0); }
#         }
#         @keyframes fadeDown {
#             0% { opacity: 0; transform: translateY(-15px); }
#             100% { opacity: 1; transform: translateY(0); }
#         }

#         /* Breakout Button (Main Lobby) */
#         .breakout-btn {
#             background: linear-gradient(135deg, #3b82f6, #2563eb);
#             color: white !important;
#             padding: 0.5rem 1.2rem;
#             border-radius: 8px;
#             text-decoration: none;
#             font-weight: 600;
#             display: inline-flex;
#             align-items: center;
#             margin-bottom: 1.5rem;
#             box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
#             transition: all 0.3s ease;
#             animation: fadeDown 0.6s ease-out;
#             font-size: 0.95rem;
#         }
#         .breakout-btn:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 6px 15px rgba(37, 99, 235, 0.35);
#             background: linear-gradient(135deg, #2563eb, #1d4ed8);
#         }

#         /* Suite Title area */
#         .suite-header {
#             animation: fadeUp 0.8s ease-out;
#         }

#         /* High-End Suite Cards */
#         .suite-card {
#             background: rgba(255, 255, 255, 0.8);
#             backdrop-filter: blur(10px);
#             border: 1px solid #e2e8f0;
#             border-top: 4px solid #3b82f6;
#             padding: 1.5rem;
#             border-radius: 16px;
#             height: 180px; 
#             box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
#             transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
#             display: flex;
#             flex-direction: column;
#             justify-content: center;
#             align-items: center;
#             text-align: center;
#             animation: fadeUp 1s ease-out;
#         }
#         .suite-card:hover {
#             transform: translateY(-8px);
#             box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.15);
#             border-color: #93c5fd;
#         }
        
#         /* Interactive Icons */
#         .card-icon {
#             font-size: 2.5rem;
#             margin-bottom: 0.5rem;
#             transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
#         }
#         .suite-card:hover .card-icon {
#             transform: scale(1.2) rotate(8deg);
#         }

#         .suite-card h3 { 
#             margin-top: 0px; 
#             margin-bottom: 8px; 
#             color: #0f172a; 
#             font-size: 20px;
#             font-weight: 700;
#         }
#         .suite-card p { 
#             color: #475569; 
#             font-size: 14px; 
#             line-height: 1.5; 
#             margin-bottom: 0px;
#         }

#         /* Streamlit Button Styling (Launch & Back buttons) */
#         div[data-testid="stButton"] > button {
#             border-radius: 8px !important;
#             font-weight: 600 !important;
#             border: 1px solid #cbd5e1 !important;
#             background-color: #ffffff !important;
#             color: #334155 !important;
#             transition: all 0.3s ease !important;
#             animation: fadeUp 1.2s ease-out;
#         }
#         div[data-testid="stButton"] > button:hover {
#             border-color: #3b82f6 !important;
#             background-color: #f0f9ff !important;
#             color: #2563eb !important;
#             box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
#             transform: translateY(-2px) !important;
#         }
        
#         hr { border-color: #e2e8f0; animation: fadeUp 0.8s ease-out; }
#     </style>
# """, unsafe_allow_html=True)

# # 3. LOCAL IMPORTS
# try:
#     from modules.risk_prediction import run_risk_module
#     from modules.ai_counselor import run_ai_counselor
#     from modules.progress_tracking import run_progress_tracking 
# except Exception as e:
#     st.error(f"Import Error: {e}")
#     st.stop()

# # 4. NAVIGATION STATE
# if 'current_view' not in st.session_state:
#     st.session_state.current_view = 'MySuite'

# def navigate(view_name):
#     st.session_state.current_view = view_name
#     st.rerun()

# # --- 5. YOUR SUB-PORTAL ---
# if st.session_state.current_view == 'MySuite':
    
#     # 🚀 THE BREAKOUT BUTTON: Beautifully styled for the iframe escape
#     st.markdown("""
#         <a href="http://localhost:8501" target="_top" class="breakout-btn">
#             🏠 Main Lobby
#         </a>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="suite-header"><h2 style="color: #1E3A8A; font-weight: 800; margin-bottom: 0;">🎯 Risk Prediction & Intervention Suite</h2>', unsafe_allow_html=True)
#     st.markdown('<p style="color: #64748b; font-size: 1.1rem; margin-top: 5px;">Welcome to the specialized lab for student dropout prevention and clinical goal setting.</p></div>', unsafe_allow_html=True)
#     st.divider()
    
#     card1, card2, card3 = st.columns(3)
    
#     with card1: 
#         st.markdown("""
#             <div class="suite-card">
#                 <div class="card-icon">🔍</div>
#                 <h3>Risk Diagnostic</h3>
#                 <p>Analyze 73 behavioral variables and simulate recovery paths.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#     with card2: 
#         st.markdown("""
#             <div class="suite-card">
#                 <div class="card-icon">🤖</div>
#                 <h3>AI Counselor</h3>
#                 <p>Consult the LLM Clinical assistant for intervention advice.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#     with card3: 
#         st.markdown("""
#             <div class="suite-card">
#                 <div class="card-icon">📈</div>
#                 <h3>Progress Tracking</h3>
#                 <p>Analyze the gap between actual performance and locked goals.</p>
#             </div>
#         """, unsafe_allow_html=True)
        
#     st.write("") 
#     btn1, btn2, btn3 = st.columns(3)
    
#     # Updated to width="stretch" to remove 2026 warnings!
#     with btn1:
#         if st.button("Launch Diagnostic", width="stretch"):
#             st.session_state.active_tool = 'Risk'
#             navigate('Tool')
#     with btn2:
#         if st.button("Launch AI Bot", width="stretch"):
#             st.session_state.active_tool = 'Counselor'
#             navigate('Tool')
#     with btn3:
#         if st.button("Launch Tracker", width="stretch"):
#             st.session_state.active_tool = 'Tracking'
#             navigate('Tool')

# # --- 6. YOUR TOOLS ---
# elif st.session_state.current_view == 'Tool':
    
#     # # Native Streamlit button to go back ONE step to your Suite Portal
#     # # The CSS styling automatically applies a beautiful hover effect to this!
#     # if st.button("« Back to Suite Portal", help="Return to the Risk Suite menu"): 
#     #     navigate('MySuite')
        
#     # st.divider()
    
#     if st.session_state.active_tool == 'Risk':
#         run_risk_module()
#     elif st.session_state.active_tool == 'Counselor':
#         run_ai_counselor()
#     elif st.session_state.active_tool == 'Tracking':
#         run_progress_tracking()



import streamlit as st
import os
import sys

# 1. PAGE CONFIG
st.set_page_config(page_title="Risk Suite", page_icon="🎯", layout="wide")

# --- 2. HIGH-END INTERACTIVE CSS ---
st.markdown("""
    <style>
        /* 🚀 FIX: Do NOT hide the whole header. Only hide the Deploy/GitHub buttons. This keeps the Sidebar Toggle visible! */
        header[data-testid="stHeader"] { background: transparent !important; }
        .stAppDeployButton, [data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; }
        
        /* Clean up container padding for the iframe */
        .block-container { 
            padding-top: 1.5rem !important; 
            max-width: 1200px;
        }

        /* App Background */
        .stApp {
            background: radial-gradient(circle at top, #ffffff, #f8fafc 80%);
        }

        /* Animations */
        @keyframes fadeUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeDown {
            0% { opacity: 0; transform: translateY(-15px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Breakout Button (Main Lobby) */
        .breakout-btn {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white !important;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
            transition: all 0.3s ease;
            animation: fadeDown 0.6s ease-out;
            font-size: 0.95rem;
        }
        .breakout-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(37, 99, 235, 0.35);
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
        }

        /* Suite Title area */
        .suite-header {
            animation: fadeUp 0.8s ease-out;
        }

        /* High-End Suite Cards */
        .suite-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid #e2e8f0;
            border-top: 4px solid #3b82f6;
            padding: 1.5rem;
            border-radius: 16px;
            height: 180px; 
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            animation: fadeUp 1s ease-out;
        }
        .suite-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.15);
            border-color: #93c5fd;
        }
        
        /* Interactive Icons */
        .card-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .suite-card:hover .card-icon {
            transform: scale(1.2) rotate(8deg);
        }

        .suite-card h3 { 
            margin-top: 0px; 
            margin-bottom: 8px; 
            color: #0f172a; 
            font-size: 20px;
            font-weight: 700;
        }
        .suite-card p { 
            color: #475569; 
            font-size: 14px; 
            line-height: 1.5; 
            margin-bottom: 0px;
        }

        /* Streamlit Button Styling */
        div[data-testid="stButton"] > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: 1px solid #cbd5e1 !important;
            background-color: #ffffff !important;
            color: #334155 !important;
            transition: all 0.3s ease !important;
            animation: fadeUp 1.2s ease-out;
        }
        div[data-testid="stButton"] > button:hover {
            border-color: #3b82f6 !important;
            background-color: #f0f9ff !important;
            color: #2563eb !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
            transform: translateY(-2px) !important;
        }
        
        hr { border-color: #e2e8f0; animation: fadeUp 0.8s ease-out; }
    </style>
""", unsafe_allow_html=True)

# 3. LOCAL IMPORTS
try:
    from modules.risk_prediction import run_risk_module
    from modules.ai_counselor import run_ai_counselor
    from modules.progress_tracking import run_progress_tracking 
except Exception as e:
    st.error(f"Import Error: {e}")
    st.stop()

# 4. NAVIGATION STATE
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'MySuite'

def navigate(view_name):
    st.session_state.current_view = view_name
    st.rerun()

# --- 5. YOUR SUB-PORTAL ---
if st.session_state.current_view == 'MySuite':
    
    # 🚀 THE BREAKOUT BUTTON: Beautifully styled for the iframe escape
    st.markdown("""
        <a href="http://localhost:8501" target="_top" class="breakout-btn">
            🏠 Main Lobby
        </a>
    """, unsafe_allow_html=True)

    st.markdown('<div class="suite-header"><h2 style="color: #1E3A8A; font-weight: 800; margin-bottom: 0;">🎯 Risk Prediction & Intervention Suite</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #64748b; font-size: 1.1rem; margin-top: 5px;">Welcome to the specialized lab for student dropout prevention and clinical goal setting.</p></div>', unsafe_allow_html=True)
    st.divider()
    
    card1, card2, card3 = st.columns(3)
    
    with card1: 
        st.markdown("""
            <div class="suite-card">
                <div class="card-icon">🔍</div>
                <h3>Risk Diagnostic</h3>
                <p>Analyze 73 behavioral variables and simulate recovery paths.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with card2: 
        st.markdown("""
            <div class="suite-card">
                <div class="card-icon">🤖</div>
                <h3>AI Counselor</h3>
                <p>Consult the LLM Clinical assistant for intervention advice.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with card3: 
        st.markdown("""
            <div class="suite-card">
                <div class="card-icon">📈</div>
                <h3>Progress Tracking</h3>
                <p>Analyze the gap between actual performance and locked goals.</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("") 
    btn1, btn2, btn3 = st.columns(3)
    
    # Using use_container_width=True to stretch buttons beautifully
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

# --- 6. YOUR TOOLS ---
elif st.session_state.current_view == 'Tool':
    
    # ❌ The global Back button is GONE.
    # The tools will now display their own local Back buttons!
    
    if st.session_state.active_tool == 'Risk':
        run_risk_module()
    elif st.session_state.active_tool == 'Counselor':
        run_ai_counselor()
    elif st.session_state.active_tool == 'Tracking':
        run_progress_tracking()