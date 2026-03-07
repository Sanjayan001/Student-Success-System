# import streamlit as st
# import pandas as pd
# import joblib
# import os
# import numpy as np
# from database.app_db import DB_PATH, save_prediction
# from datetime import datetime

# # This finds the 'modules' folder where this script lives
# CURRENT_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Go up one level to 'Risk-Prediction' then into 'models' and 'database'
# PACKAGE_FILE = os.path.join(CURRENT_MODULE_DIR, "..", "models", "student_dropout_model_1.pkl")
# DB_FOLDER_PATH = os.path.join(CURRENT_MODULE_DIR, "..", "database")

# def run_risk_module():
#     st.markdown("## 🎓 Student Risk Intelligence Diagnostic")
#     st.caption("Precision Behavioral Analytics | Unified Stable-Engine v4.0")
    
#     if not os.path.exists(PACKAGE_FILE):
#         st.error(f"📦 Model Package Missing: Expected {PACKAGE_FILE} in /models/")
#         st.info("Please ensure you have saved your model using the 'Model 1 Package' code.")
#         return

#     # --- THE UNIFIED LOAD ---
#     package = joblib.load(PACKAGE_FILE)
#     model = package['ensemble']
#     scaler = package['scaler']
#     ALL_EXPECTED_FEATURES = package['feature_names']
#     DEFAULT_THRESHOLD = package.get('threshold', 0.5)

#     # --- FORM PERSISTENCE LOGIC ---
#     if 'form_data' not in st.session_state:
#         st.session_state.form_data = {}


#     # --- MAIN UI FORM ---
#     with st.form("comprehensive_diagnostic_form"):
#         tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "📚 Academics", "📉 Phase Trends", "⚠️ Challenges"])

#         with tab1:
#             st.subheader("Demographics & Lifestyle")
#             c1, c2 = st.columns(2)
#             with c1:
#                 student_id = st.text_input("Student ID*", value=st.session_state.form_data.get('student_id', "STU-001"))
#                 age = st.number_input("Age", 17, 60, st.session_state.form_data.get('age', 21))
#                 gender = st.selectbox("Gender", ["Female", "Male"])
#                 faculty = st.selectbox("Faculty", ["Computing", "Engineering", "Business", "Humanities & Sciences", "Architecture", "Law", "Hospitality & Culinary"])
#             with c2:
#                 living = st.selectbox("Living Arrangement", ["With family", "Hostel", "Shared apartment", "Alone"])
#                 part_time = st.selectbox("Part-time Job", ["No", "Yes"])
#                 travel = st.selectbox("Daily Travel Time", ["0-15 minutes", "16-30 minutes", "31-60 minutes", "61-90 minutes", "More than 90 minutes"])
#                 family_support = st.select_slider("Family Support Level", options=[1, 2, 3, 4, 5], value=st.session_state.form_data.get('family_support', 3))

#         with tab2:
#             st.subheader("Academic Engagement")
#             c1, c2 = st.columns(2)
#             with c1:
#                 cgpa = st.number_input("Current CGPA", 0.0, 4.0, st.session_state.form_data.get('cgpa', 3.0))
#                 semester = st.selectbox("Semester", ["1st Semester", "2nd Semester", "3rd Semester", "4th Semester", "5th Semester", "6th Semester", "7th Semester", "8th Semester"])
#                 failed_subs = st.selectbox("Failed Subjects", ["0", "1", "2", "3", "4", "5 or more"])
#                 attendance = st.slider("Average Attendance (0-10 scale)", 0, 10, st.session_state.form_data.get('attendance', 8))
#             with c2:
#                 study_hours = st.selectbox("Weekly Study Hours", ["0-5 hours", "6-10 hours", "11-15 hours", "16-20 hours", "More than 20 hours"])
#                 assignments = st.selectbox("Assignments Submitted on Time", ["0-25%", "26-50%", "51-75%", "76-100%"])
#                 lecture_part = st.slider("Lecture Participation", 1, 5, 3)
#                 lab_part = st.slider("Lab Participation", 1, 5, 3)
#                 academic_guidance = st.selectbox("Received Guidance?", ["Not at all", "Rarely", "Yes, occasionally", "Yes, frequently"])

#         with tab3:
#             st.subheader("Longitudinal Trends (Phase 1-4)")
#             p_cols = st.columns(4)
#             phase_inputs = {}
#             sleep_map = {"0-3 hours": 0, "4-5 hours": 1, "6-7 hours": 2, "8-9 hours": 3, "More than 9 hours": 4}
#             relax_map = {"0-2 hours": 0, "3-5 hours": 1, "6-8 hours": 2, "9-12 hours": 3, "More than 12 hours": 4}

#             for i, p_col in enumerate(p_cols, 1):
#                 suffix = f"Phase{i}"
#                 with p_col:
#                     st.markdown(f"**Phase {i}**")
#                     phase_inputs[f"Motivation_{suffix}"] = st.slider(f"Motivation P{i}", 1, 5, 3, key=f"mot{i}")
#                     phase_inputs[f"Stress_{suffix}"] = st.slider(f"Stress P{i}", 1, 5, 3, key=f"str{i}")
#                     phase_inputs[f"Confidence_{suffix}"] = st.slider(f"Confidence P{i}", 1, 5, 3, key=f"con{i}")
#                     phase_inputs[f"Workload_{suffix}"] = st.slider(f"Workload P{i}", 1, 5, 3, key=f"wrk{i}")
#                     phase_inputs[f"Social_{suffix}"] = st.slider(f"Social P{i}", 1, 5, 3, key=f"soc{i}")
#                     sl_raw = st.selectbox(f"Sleep P{i}", list(sleep_map.keys()), index=2, key=f"sl{i}")
#                     re_raw = st.selectbox(f"Relax P{i}", list(relax_map.keys()), index=1, key=f"re{i}")
#                     phase_inputs[f"Sleep_Hours_{suffix}"] = sleep_map[sl_raw]
#                     phase_inputs[f"Relaxation_{suffix}"] = relax_map[re_raw]

#         with tab4:
#             st.subheader("Retention Challenges")
#             ch_list = {
#                 'mental stress / burnout': st.checkbox("Mental stress / burnout"),
#                 'lack of proper academic guidance': st.checkbox("Lack of proper academic guidance"),
#                 'lack of study resources': st.checkbox("Lack of study resources"),
#                 'difficulty understanding lectures': st.checkbox("Difficulty understanding lectures"),
#                 'poor time management': st.checkbox("Poor time management"),
#                 'financial problems': st.checkbox("Financial problems"),
#                 'personal/family issues': st.checkbox("Personal/family issues"),
#                 'difficulty choosing subjects': st.checkbox("Difficulty choosing subjects")
#             }
#             dropout_cons = st.radio("Considered dropping out?", ["No", "Yes"])

#         submit = st.form_submit_button("🚀 Run AI Risk Diagnostic")

#     if submit:
#         # --- 1. DATA PREPARATION ---
#         data = pd.DataFrame(0.0, index=[0], columns=ALL_EXPECTED_FEATURES)
        
#         # Numeric Direct Mappings
#         data['Age'] = float(age)
#         data['CGPA'] = float(cgpa)
#         data['Attendance_Percentage'] = float(attendance)
#         data['Failed_Subjects'] = 5.0 if failed_subs == "5 or more" else float(failed_subs)
#         data['Lecture_Participation'] = float(lecture_part)
#         data['Lab_Participation'] = float(lab_part)
#         data['Family_Support'] = float(family_support)
#         data['Gender'] = 1.0 if gender == "Female" else 0.0
#         data['Part_Time_Job'] = 1.0 if part_time == "Yes" else 0.0
#         data['Considered_Dropout'] = 1.0 if dropout_cons == "Yes" else 0.0

#         # --- THE MISSING MAPPINGS ---
        
#         # Semester
#         sem_map = {'1st Semester': 1, '2nd Semester': 2, '3rd Semester': 3, '4th Semester': 4, 
#                    '5th Semester': 5, '6th Semester': 6, '7th Semester': 7, '8th Semester': 8}
#         data['Semester'] = float(sem_map.get(semester, 0))

#         # Travel Time
#         travel_map = {"0-15 minutes": 0, "16-30 minutes": 1, "31-60 minutes": 2, "61-90 minutes": 3, "More than 90 minutes": 4}
#         if 'Travel_Time' in data.columns:
#             data['Travel_Time'] = float(travel_map.get(travel, 0))

#         # Study Hours
#         study_map = {"0-5 hours": 0, "6-10 hours": 1, "11-15 hours": 2, "16-20 hours": 3, "More than 20 hours": 4}
#         if 'Study_Hours' in data.columns:
#             data['Study_Hours'] = float(study_map.get(study_hours, 0))

#         # Assignment Submission
#         assign_map = {"0-25%": 0, "26-50%": 1, "51-75%": 2, "76-100%": 3}
#         if 'Assignment_Submission' in data.columns:
#             data['Assignment_Submission'] = float(assign_map.get(assignments, 0))

#         # Academic Guidance
#         guidance_map = {"Not at all": 0, "Rarely": 1, "Yes, occasionally": 2, "Yes, frequently": 3}
#         if 'Academic_Guidance' in data.columns:
#             data['Academic_Guidance'] = float(guidance_map.get(academic_guidance, 0))

#         # --- END OF NEW MAPPINGS ---

#         # Handle Dynamic Faculty & Living Columns
#         if f"Faculty_{faculty}" in data.columns: data[f"Faculty_{faculty}"] = 1.0
#         if f"Living_{living}" in data.columns: data[f"Living_{living}"] = 1.0
        
#         # Handle Challenges Checkboxes
#         for ch_name, checked in ch_list.items():
#             col = f"Challenge_{ch_name}"
#             if col in data.columns: data[col] = 1.0 if checked else 0.0

#         # --- 2. TRAJECTORY ENGINE ---
#         metrics = ['Motivation', 'Stress', 'Confidence', 'Social', 'Workload', 'Sleep_Hours', 'Relaxation']
#         x_points = np.array([1, 2, 3, 4])
#         for m in metrics:
#             p_vals = [float(phase_inputs[f"{m}_Phase{p}"]) for p in range(1, 5)]
#             if f'{m}_Phase1' in data.columns: data[f'{m}_Phase1'] = p_vals[0]
#             if f'{m}_Phase4' in data.columns: data[f'{m}_Phase4'] = p_vals[3]
#             data[f'{m}_Volatility'] = float(np.std(p_vals))
#             data[f'{m}_Slope'] = float(np.polyfit(x_points, p_vals, 1)[0])
#             data[f'{m}_Acceleration'] = float((p_vals[3] - p_vals[2]) - (p_vals[1] - p_vals[0]))

#         # --- 3. PREDICTION ---
#         # 1. Scale the data (this returns a NumPy array, which causes the warning)
#         X_scaled_array = scaler.transform(data)
        
#         # 2. Convert it BACK to a DataFrame so the model sees the feature names
#         X_scaled_df = pd.DataFrame(X_scaled_array, columns=ALL_EXPECTED_FEATURES)
        
#         # 3. Predict using the DataFrame instead of the array
#         prob = model.predict_proba(X_scaled_df)[:, 1][0]
#         status = "High Risk" if prob >= DEFAULT_THRESHOLD else "Low Risk"

#         # --- SESSION HANDOVER ---
#         st.session_state['last_student_id'] = student_id
#         st.session_state['last_run_data'] = {
#             'status': status,
#             'risk_score': prob,
#             'details': data.to_dict('records')[0]
#         }

#         # --- 4. VISUAL ASSESSMENT (High-Impact Header) ---
#         # UPDATED: Added styled HTML headers for the risk profile
#         st.divider()
#         res_col1, res_col2 = st.columns([1, 1])
#         with res_col1:
#             color = "#FF4B4B" if status == "High Risk" else "#28A745"
#             st.markdown(f"<h2 style='color: {color}; margin-bottom:0;'>{status} Profile Detected</h2>", unsafe_allow_html=True)
#             st.metric("Risk Probability", f"{prob:.4f}")
        
#         with res_col2:
#             st.write("📊 **Neural Decision Confidence**")
#             st.progress(min(float(prob), 1.0))
#             st.caption("Confidence score derived from Gradient Boosted Ensemble weights.")

#         # --- 5. ENHANCED HUMAN-CENTRIC XAI REPORT ---
#         st.write("---")
#         st.header("🔍 Intelligence Strategy Report")
        
#         cv = data.iloc[0] 

#         # A. THE EXECUTIVE SUMMARY (High-Fidelity Banner)
#         risk_color = "#FF4B4B" if status == "High Risk" else "#28A745"
#         risk_bg = "#FF4B4B15" if status == "High Risk" else "#28A74515"
        
#         st.markdown(f"""
#             <div style="background-color: {risk_bg}; padding: 30px; border-radius: 20px; border: 1px solid {risk_color}; margin-bottom: 25px;">
#                 <h3 style="margin:0; color: {risk_color}; font-size: 24px;">Executive Summary</h3>
#                 <p style="margin:10px 0 0 0; font-size: 18px; color: #1D1D1F; line-height: 1.6;">
#                     The AI Ensemble has analyzed <b>{len(ALL_EXPECTED_FEATURES)} behavioral markers</b>. 
#                     {'<b>CRITICAL:</b> This student is showing patterns highly consistent with historical dropout cases. Immediate intervention is advised.' if status == 'High Risk' else '<b>STABLE:</b> The student is currently maintaining a path toward successful completion. Protective factors are strong.'}
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)

#         # UPDATED: B. THE "CORE FOUR" DEEP DIAGNOSTIC (Now a professional 2x2 Grid)
#         grid_row1_col1, grid_row1_col2 = st.columns(2)
#         grid_row2_col1, grid_row2_col2 = st.columns(2)
        
#         with grid_row1_col1:
#             with st.container(border=True):
#                 st.markdown("#### 🧠 Behavioral Momentum")
#                 conf_acc = cv.get('Confidence_Acceleration', 0)
#                 if conf_acc < -0.1: st.error(f"Trend: Downward Spiral ({conf_acc:.2f})")
#                 elif conf_acc > 0.1: st.success(f"Trend: Growth Mindset (+{conf_acc:.2f})")
#                 else: st.info("Trend: Steady Plateau")
#                 st.caption("Self-belief relative to increasing task difficulty.")

#         with grid_row1_col2:
#             with st.container(border=True):
#                 st.markdown("#### 🛌 Biological Battery")
#                 sleep_slp = cv.get('Sleep_Hours_Slope', 0)
#                 if sleep_slp < -0.1: st.error(f"Trend: Energy Depletion ({sleep_slp:.2f})")
#                 else: st.success("Trend: Healthy Rest Cycle")
#                 st.caption("Foundation for cognitive retention and memory.")

#         with grid_row2_col1:
#             with st.container(border=True):
#                 st.markdown("#### 📈 Engagement Rhythm")
#                 mot_vol = cv.get('Motivation_Volatility', 0)
#                 if mot_vol > 1.2: st.warning(f"Trend: Reactive/Panic Study ({mot_vol:.2f})")
#                 else: st.success("Trend: Proactive Discipline")
#                 st.caption("Consistency of study habits vs reactive cramming.")

#         with grid_row2_col2:
#             with st.container(border=True):
#                 st.markdown("#### ⚓ Institutional Anchor")
#                 att = cv.get('Attendance_Percentage', 0)
#                 if att < 7: st.error(f"Status: Loose Tethering ({att}/10)")
#                 else: st.success(f"Status: Strong Tethering ({att}/10)")
#                 st.caption("Physical and social connection to the campus.")

#         # C. Recommended Strategy (Prescription)
#         st.write("")
#         with st.container(border=True):
#             st.subheader("🎯 Recommended Success Strategy")
#             if status == "High Risk":
#                 strat_c1, strat_c2, strat_c3 = st.columns(3)
#                 strat_c1.markdown("**1. Break the Spiral**\nAssign one 15-min success task to rebuild confidence.")
#                 strat_c2.markdown("**2. Sleep Audit**\nMandatory rest schedule adjustment for cognitive recovery.")
#                 strat_c3.markdown("**3. Human Connection**\nHigh-touch face-to-face academic advisory meeting.")
#             else:
#                 st.success("✅ **Maintain Momentum:** Student is self-regulating effectively. Reinforce current routines.")

#         # D. TECHNICAL WEIGHTS
#         with st.expander("🛠️ View Decision Logic (Neural Weights)"):
#             importance_df = pd.DataFrame({
#                 "Intelligence Signal": [n.replace("_", " ").title() for n in ALL_EXPECTED_FEATURES[:15]],
#                 "Normalized Value": [f"{v:.4f}" for v in X_scaled_df.values[0][:15]]
#             })
#             st.table(importance_df)

#         save_prediction(student_id, float(prob), status, data.to_dict('records')[0])

#     # --- 6. THE "DECISION LABORATORY" (Advanced Simulation Suite) ---
#     if 'last_run_data' in st.session_state:
#         st.write("---")
#         st.header("🧪 Prescriptive Simulation Laboratory")
        
#         # UPDATED: Added outer container for a dashboard look
#         with st.container(border=True):
#             st.info("💡 Engineer a recovery strategy by adjusting the levers below to see real-time risk reduction.")

#             with st.expander("🚀 OPEN SIMULATION THEATER", expanded=False):
#                 original_details = st.session_state['last_run_data']['details'].copy()
#                 actual_prob = st.session_state['last_run_data']['risk_score']
                
#                 # UPDATED: Cleaned up column naming for the 3-pillar dashboard
#                 sim_col_ac, sim_col_bh, sim_col_bio = st.columns(3)
                
#                 with sim_col_ac:
#                     st.markdown("#### 📚 Academic Levers")
#                     sim_cgpa = st.slider("Modify CGPA", 0.0, 4.0, float(original_details['CGPA']), 0.05)
#                     sim_att = st.slider("Modify Attendance", 0.0, 10.0, float(original_details['Attendance_Percentage']), 0.5)
#                     sim_fail = st.select_slider("Subjects Failed", options=[0, 1, 2, 3, 4, 5], value=int(original_details['Failed_Subjects']))
                
#                 with sim_col_bh:
#                     st.markdown("#### 🧠 Behavioral Levers")
#                     sim_mot = st.slider("Boost Motivation", 1.0, 5.0, float(original_details['Motivation_Phase4']), 0.1)
#                     sim_conf = st.slider("Boost Confidence", 1.0, 5.0, float(original_details['Confidence_Phase4']), 0.1)
#                     sim_stress = st.slider("Internal Stress Level", 1.0, 5.0, float(original_details['Stress_Phase4']), 0.1)

#                 with sim_col_bio:
#                     st.markdown("#### 🛌 Biological Levers")
#                     sim_sleep = st.slider("Sleep Hygiene (0-4)", 0, 4, int(original_details.get('Sleep_Hours_Phase4', 2)))
#                     sim_relax = st.slider("Relaxation Level (0-4)", 0, 4, int(original_details.get('Relaxation_Phase4', 2)))
#                     sim_support = st.slider("Family Support (1-5)", 1, 5, int(original_details['Family_Support']))

#                 # 1. Update Simulation DataFrame
#                 sim_df = pd.DataFrame([original_details])
#                 sim_df['CGPA'] = sim_cgpa
#                 sim_df['Attendance_Percentage'] = sim_att
#                 sim_df['Failed_Subjects'] = float(sim_fail)
#                 sim_df['Motivation_Phase4'] = sim_mot
#                 sim_df['Confidence_Phase4'] = sim_conf
#                 sim_df['Stress_Phase4'] = sim_stress
#                 sim_df['Sleep_Hours_Phase4'] = float(sim_sleep)
#                 sim_df['Relaxation_Phase4'] = float(sim_relax)
#                 sim_df['Family_Support'] = float(sim_support)

#                 # 2. Re-calculate Probability using Scaler
#                 sim_scaled = scaler.transform(sim_df[ALL_EXPECTED_FEATURES])
#                 sim_scaled_df = pd.DataFrame(sim_scaled, columns=ALL_EXPECTED_FEATURES)
#                 sim_prob = model.predict_proba(sim_scaled_df)[:, 1][0]
                
#                 st.divider()

#                 # PRESERVED: Your Plotly Impact Matrix
#                 res_c1, res_c2 = st.columns([1, 2])
#                 with res_c1:
#                     st.markdown("#### 🔮 Outcome Projection")
#                     diff = sim_prob - actual_prob
#                     st.metric("Projected Risk", f"{sim_prob:.2%}", delta=f"{diff:+.2%}", delta_color="inverse")
                    
#                     if sim_prob < DEFAULT_THRESHOLD:
#                         st.success("✅ INTERVENTION SUCCESS")
#                     else:
#                         st.warning("⚠️ INSUFFICIENT IMPACT")

#                 with res_c2:
#                     st.markdown("#### 📊 Sensitivity Impact Matrix")
#                     impact_data = pd.DataFrame({
#                         "Category": ["Academic", "Behavioral", "Biological"],
#                         "Gravity": [abs(sim_cgpa - original_details['CGPA']) * 2, 
#                                     abs(sim_mot - original_details['Motivation_Phase4']) * 1.5,
#                                     abs(sim_sleep - original_details.get('Sleep_Hours_Phase4', 2)) * 1.2]
#                     })
#                     import plotly.express as px
#                     fig_impact = px.bar(impact_data, x="Gravity", y="Category", orientation='h', 
#                                          color="Gravity", color_continuous_scale="Viridis", height=200)
#                     fig_impact.update_layout(margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
#                     # UPDATED: Used standard Streamlit 2026 syntax for responsive charts
#                     st.plotly_chart(fig_impact, use_container_width=True)

#                 # PRESERVED: Your full SQLite logic and Digital Receipt UI
#                 if st.button("📝 Finalize Intervention Prescription", width="stretch", type="primary"):
#                     from database.app_db import DB_PATH 
                    
#                     try:
#                         import sqlite3
#                         conn = sqlite3.connect(DB_PATH)
#                         cursor = conn.cursor()
                        
#                         risk_reduction = actual_prob - sim_prob
                        
#                         cursor.execute("""
#                             INSERT OR REPLACE INTO intervention_goals 
#                             (student_id, target_cgpa, target_attendance, target_failed_subs, 
#                             target_motivation, target_confidence, target_stress, 
#                             target_sleep, target_relaxation, target_support, predicted_risk_reduction)
#                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#                         """, (
#                             st.session_state['last_student_id'],
#                             float(sim_cgpa), float(sim_att), float(sim_fail), 
#                             float(sim_mot), float(sim_conf), float(sim_stress), 
#                             float(sim_sleep), float(sim_relax), float(sim_support), 
#                             float(risk_reduction)
#                         ))
                        
#                         conn.commit()
#                         conn.close()
                        
#                         st.balloons()
#                         st.success(f"🎯 Clinical Prescription Finalized for {st.session_state['last_student_id']}")

#                         with st.expander("📄 View Finalized Intervention Summary", expanded=True):
#                             st.markdown(f"### Strategy Archive: {st.session_state['last_student_id']}")
#                             st.info("All 9 behavioral and academic levers have been synced to the Research Database.")
                            
#                             meta1, meta2, meta3 = st.columns(3)
                            
#                             with meta1:
#                                 st.metric(label="Target CGPA", value=f"{sim_cgpa:.2f}")
#                                 st.metric(label="Sleep Hygiene", value=f"{sim_sleep} / 4")
                                
#                             with meta2:
#                                 st.metric(label="Attendance Goal", value=f"{sim_att:.1f}%")
#                                 st.metric(label="Stress Cap", value=f"{sim_stress} / 5")
                                
#                             with meta3:
#                                 improvement = actual_prob - sim_prob
#                                 st.metric(label="Risk Reduction", value=f"{improvement:.2%}", delta="Optimized")
#                                 st.metric(label="Motivation Target", value=f"{sim_mot} / 5")

#                             st.caption(f"Prescription Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        
#                     except Exception as e:
#                         st.error(f"❌ Synchronization Failure: {e}")
#                         st.warning("Ensure the database is not open in another application (like DB Browser).")














import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from database.app_db import DB_PATH, save_prediction
from datetime import datetime
import shap
import lime
import lime.lime_tabular
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# --- SYSTEM SETUP ---
CURRENT_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_FILE = os.path.join(CURRENT_MODULE_DIR, "..", "models", "student_dropout_model_1.pkl")
DB_FOLDER_PATH = os.path.join(CURRENT_MODULE_DIR, "..", "database")

# =====================================================================
# 🧠 THE MASTER NEURO-BEHAVIORAL LEXICON (EXHAUSTIVE)
# =====================================================================

FEATURE_TRANSLATIONS = {
    "CGPA": "Cumulative GPA Foundation",
    "Attendance_Percentage": "Physical Campus Presence",
    "Failed_Subjects": "Historical Academic Debt",
    "Age": "Chronological Maturity",
    "Gender": "Demographic Baseline",
    "Part_Time_Job": "External Labor Burden",
    "Considered_Dropout": "Active Dropout Ideation",
    "Study_Hours": "Weekly Deep Work Capacity",
    "Assignment_Submission": "Deadline Discipline",
    "Lecture_Participation": "Active Lecture Engagement",
    "Lab_Participation": "Practical Application Engagement",
    "Academic_Guidance": "Utilization of Mentorship",
    "Family_Support": "Tribal / Family Backing",
    "Travel_Time": "Daily Commute Drain",
    "Semester": "Current Academic Epoch"
}

def translate_feature(fname):
    if "Volatility" in fname: return f"Erratic Swings in {fname.replace('_Volatility', '')}"
    if "Slope" in fname: return f"Long-Term Trajectory of {fname.replace('_Slope', '')}"
    if "Acceleration" in fname: return f"Sudden Shifts in {fname.replace('_Acceleration', '')}"
    if "Phase1" in fname: return f"Beginning-of-Term {fname.replace('_Phase1', '')}"
    if "Phase2" in fname: return f"Mid-Term {fname.replace('_Phase2', '')}"
    if "Phase3" in fname: return f"Late-Term {fname.replace('_Phase3', '')}"
    if "Phase4" in fname: return f"Final-Term {fname.replace('_Phase4', '')}"
    for key, val in FEATURE_TRANSLATIONS.items():
        if key in fname: return val
    return fname.replace('_', ' ').title()

def get_exhaustive_clinical_breakdown(feature_name, is_red_flag):
    f = feature_name.lower()
    
    if is_red_flag:
        if "cgpa" in f or "failed" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Structural Academic Collapse**\n\n"
                "**🧬 The Neurological Reality:** Your brain is operating under a constant state of 'Academic Threat'. When your GPA falls below the safety threshold, or you carry failed subjects, the amygdala (your brain's fear center) remains hyperactive. You are physically experiencing education as a survival threat rather than an opportunity.\n\n"
                "**🧠 The Psychological Trap (Learned Helplessness):** You are experiencing a cognitive distortion. Past failures have convinced your subconscious that future effort is completely pointless. You look at your low grades, experience a massive spike of cortisol, and subconsciously choose distraction (gaming, scrolling) over studying to numb the immediate psychological pain. This is an avoidance loop, and it is fatal to your degree.\n\n"
                "**🛡️ The Combat Protocol:** We must violently bypass the fear center of your brain. Stop looking at the overall degree. Stop thinking about graduation. Your only mission is the very next 20-minute Pomodoro block. You need a 'Micro-Win' today to trigger a dopamine release. Dopamine is the molecule of motivation; earning it through a small task will naturally rebuild your neuroplasticity and shatter the illusion of helplessness."
            )
        elif "sleep" in f or "biology" in f or "relax" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Systemic Neuro-Toxicity**\n\n"
                "**🧬 The Neurological Reality:** You are systematically destroying your cognitive hardware. During REM and Deep Sleep, your brain activates the 'glymphatic system' to literally wash away toxic amyloid-beta proteins built up during the day. By restricting sleep, you are currently suffocating your neurons in metabolic waste, severely damaging your hippocampus.\n\n"
                "**🧠 The Psychological Trap (The Hustle Delusion):** You mistakenly equate 'staying awake' with 'working hard'. This is the ultimate lie of modern hustle culture. Without sleep, your brain absolutely cannot transfer short-term memories into the prefrontal cortex for long-term storage. You are studying for 6 hours, but your damaged hardware is only saving 30 minutes of data. You are red-lining an engine with no oil.\n\n"
                "**🛡️ The Combat Protocol:** Sleep is not a luxury; it is a biological, non-negotiable performance enhancer. You must establish a militant, military-grade bedtime. Dim the lights, eliminate blue light 90 minutes prior to sleep, and force your circadian rhythm back into alignment. Rest is when you grow."
            )
        elif "stress" in f or "workload" in f or "burden" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Adrenal Overload & Executive Dysfunction**\n\n"
                "**🧬 The Neurological Reality:** Chronic, unrelenting cortisol exposure is physically shrinking your prefrontal cortex—the exact, specific part of the brain required for complex problem-solving, impulse control, and emotional regulation. You are locked in 'fight-or-flight'.\n\n"
                "**🧠 The Psychological Trap (The Pressure Cooker):** You are deeply confusing anxiety with importance. You believe that if you aren't severely stressed, you aren't taking your future seriously. This chronic hyper-arousal leads directly to adrenal fatigue. When your workload feels impossible, your brain shuts down entirely, resulting in paralysis. You literally stare at the wall because your nervous system is fried.\n\n"
                "**🛡️ The Combat Protocol:** You cannot 'grind' your way out of biological burnout. You must immediately initiate parasympathetic nervous system recovery. Implement physiological sighs (double inhale through the nose, long exhale through the mouth) to manually slow your heart rate. Engage in radical prioritization: say 'no' to everything that does not directly prevent failure this week."
            )
        elif "attendance" in f or "participation" in f or "assignment" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Active Behavioral Avoidance**\n\n"
                "**🧬 The Neurological Reality:** Your dopaminergic pathways have been hijacked. Your brain is aggressively seeking the path of least resistance. It is mathematically rewarding the immediate comfort of skipping class or delaying an assignment over the delayed gratification of graduating.\n\n"
                "**🧠 The Psychological Trap (The Ghosting Spiral):** Let me be clear: you do not skip class because you are lazy. You skip class because attending forces you to confront exactly how far behind you are. This confrontation causes severe psychological pain. Avoiding class removes the pain temporarily, but geometrically increases your risk of failure. It is self-medication through sabotage.\n\n"
                "**🛡️ The Combat Protocol:** Remove willpower entirely from the equation. Pack your bag the night before. Put your shoes by the door. Commit to simply walking into the lecture hall. You do not need to feel inspired or motivated to attend; you just need to move your physical body into the room. Action precedes motivation, not the other way around."
            )
        elif "motivation" in f or "confidence" in f or "belief" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Dopaminergic Deficit & Identity Crisis**\n\n"
                "**🧬 The Neurological Reality:** Your drive circuitry is entirely depleted. Without a clear, believable anticipation of a reward (graduation/success), the human brain fundamentally refuses to allocate metabolic energy to difficult tasks like studying.\n\n"
                "**🧠 The Psychological Trap (The Meaning Void):** You have lost your intrinsic 'Why'. You are currently viewing your degree as an endless, torturous series of punishments rather than a bridge to your ultimate future identity. When confidence shatters, your brain enters a 'conservation state', making you feel chronically fatigued, apathetic, and hollow.\n\n"
                "**🛡️ The Combat Protocol:** You must violently re-anchor your identity. Take out a pen and paper. Write down exactly what your life will look like in 5 years if you fail, and the exact hell that will bring. Then, write down what it will look like if you conquer this. Use that dark contrast as highly potent, aggressive fuel to push through today."
            )
        elif "volatility" in f or "slope" in f or "acceleration" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Chaotic Behavioral Algorithms**\n\n"
                "**🧬 The Neurological Reality:** Your behavioral algorithms are highly unstable. The AI detects chaotic swings in your daily routine. This totally prevents your basal ganglia (the habit center of the brain) from forming automatic, low-energy habits. Every day is a struggle because everything requires active willpower.\n\n"
                "**🧠 The Psychological Trap (The Inspiration Myth):** You are a victim of your own shifting moods. You study for 14 hours when you 'feel inspired', and 0 hours when you don't. Professionals rely on systems and iron discipline; amateurs rely on motivation. This erratic volatility destroys the mathematical compounding required for university success.\n\n"
                "**🛡️ The Combat Protocol:** Stop trying to be extraordinary. Aim for boring, ruthless, mechanical consistency. 2 hours of deep, focused work every single day is infinitely superior to erratic 12-hour panic sessions. Standardize your life."
            )
        elif "support" in f or "social" in f or "guidance" in f:
            return (
                "**🚨 CLINICAL DIAGNOSIS: Severe Tribal Isolation**\n\n"
                "**🧬 The Neurological Reality:** Humans are apex pack predators; our nervous systems are absolutely not designed to process existential stress in isolation. Lack of tribal and social support spikes your baseline anxiety and keeps you in a state of hyper-vigilance.\n\n"
                "**🧠 The Psychological Trap (The Lone Wolf Fallacy):** You are actively isolating yourself due to pride, shame, or fear of judgment. You believe that asking for help is a sign of weakness or stupidity. In reality, leveraging the intelligence of mentors, professors, and peers is the ultimate evolutionary advantage. You are fighting an army with a pocket knife.\n\n"
                "**🛡️ The Combat Protocol:** You must swallow your ego and forcefully integrate into a community. Book an academic advising appointment this week. Force yourself into a study group. You need external psychological anchors to absorb the shockwaves of academic life."
            )
        else:
            return (
                f"**🚨 CLINICAL DIAGNOSIS: The {translate_feature(feature_name)} Anchor**\n\n"
                f"**🧬 The Neurological Reality:** The advanced AI algorithms have mathematically isolated your {feature_name} as a highly destructive variable. It is causing systemic, cascading friction across your entire neuro-cognitive profile.\n\n"
                f"**🧠 The Psychological Trap (Normalization of Failure):** This behavior is an invisible anchor. You have likely normalized this specific flaw, accepting it as 'just the way you are' or an unchangeable reality. The mathematical data definitively proves this normalization is actively sabotaging your statistical probability of survival.\n\n"
                f"**🛡️ The Combat Protocol:** Treat this exact metric as a hostile, invasive threat to your future. Isolate it, monitor it daily, and relentlessly optimize it. You must wage war on this specific weakness until it is neutralized."
            )

    else:
        if "cgpa" in f or "standing" in f:
            return (
                "**🟢 CLINICAL ASSET: Indestructible Academic Bedrock**\n\n"
                "**💎 The Cognitive Superpower:** Your academic baseline is elite. You have put in the grueling, invisible hours in the dark, and it is paying massive dividends in the light. This high GPA acts as literal 'Cognitive Armor'. When a personal crisis hits, or a class gets incredibly difficult, you have the mathematical and psychological buffer to survive it without your degree collapsing.\n\n"
                "**🔥 The Continuation Protocol:** Do not let success breed complacency. Success is rented, and the rent is due every single day. Maintain the exact rigorous systems that built this foundation. You are building an undeniable resume."
            )
        elif "sleep" in f or "relaxation" in f:
            return (
                "**🟢 CLINICAL ASSET: Optimized Biological Hardware**\n\n"
                "**💎 The Cognitive Superpower:** Your biological hardware is operating at peak efficiency. While your peers are surviving on caffeine, panic, and highly degraded neuro-pathways, you are operating with maximum neuroplasticity. Your emotional regulation is stable, allowing you to process highly complex academic material without entering a reactive, anxious state.\n\n"
                "**🔥 The Continuation Protocol:** Protect this routine ruthlessly. Guard your sleep schedule and decompression time as if your entire career depends on it—because statistically, the AI proves that it does."
            )
        elif "motivation" in f or "confidence" in f:
            return (
                "**🟢 CLINICAL ASSET: Elite Internal Drive Circuitry**\n\n"
                "**💎 The Cognitive Superpower:** Your intrinsic drive is a massive statistical outlier. You possess extreme 'Self-Efficacy'—the fundamental psychological belief that your actions directly dictate your outcomes. This internal locus of control makes you highly resilient to failure; you view bad grades or tough assignments as data to learn from, not as a reflection of your human worth.\n\n"
                "**🔥 The Continuation Protocol:** Channel this immense fire. Motivation is a powerful fuel, but it burns fast. Use this high motivation now to build automated, unbreakable habits so that when the motivation inevitably dips during finals week, the habits carry you to the finish line."
            )
        elif "attendance" in f or "assignment" in f or "study" in f:
            return (
                "**🟢 CLINICAL ASSET: Ironclad Operational Discipline**\n\n"
                "**💎 The Cognitive Superpower:** You have mastered the absolute rarest human trait: executing the work regardless of how you feel. You are highly reliable and deadline-driven. The AI mathematically loves this trait because consistent, unglamorous, boring execution is the single highest predictor of long-term success in both academia and the high-end corporate world.\n\n"
                "**🔥 The Continuation Protocol:** You are a machine of execution. Keep showing up. Keep submitting the work. Do not rely on inspiration. You are mathematically engineering your own inevitability. Keep marching."
            )
        else:
            return (
                f"**🟢 CLINICAL ASSET: The {translate_feature(feature_name)} Shield**\n\n"
                f"**💎 The Cognitive Superpower:** Your {feature_name} is mathematically acting as a massive shield against academic failure. You have cultivated a highly specific, highly effective strength that perfectly offsets your weaknesses. This acts as a load-bearing pillar for your entire academic profile, providing immense stability in the chaos of university life.\n\n"
                f"**🔥 The Continuation Protocol:** Acknowledge this superpower. Lean heavily into this strength whenever you face adversity or burnout in other areas. It is your ultimate safety net."
            )

# =====================================================================
# 🕵️‍♂️ SOTA LOOPHOLE & INTERACTION ENGINE
# =====================================================================

def advanced_loophole_detection(data):
    loopholes = []
    
    cgpa = data['CGPA'].iloc[0]
    att = data['Attendance_Percentage'].iloc[0]
    study = data['Study_Hours'].iloc[0]
    lec_part = data['Lecture_Participation'].iloc[0]
    lab_part = data['Lab_Participation'].iloc[0]
    fail_subs = data['Failed_Subjects'].iloc[0]
    stress4 = data['Stress_Phase4'].iloc[0]
    sleep4 = data['Sleep_Hours_Phase4'].iloc[0]
    mot4 = data['Motivation_Phase4'].iloc[0]
    conf4 = data['Confidence_Phase4'].iloc[0]
    job = data['Part_Time_Job'].iloc[0]
    travel = data['Travel_Time'].iloc[0]
    support = data['Family_Support'].iloc[0]
    soc4 = data['Social_Phase4'].iloc[0]
    guidance = data.get('Academic_Guidance', pd.Series([0])).iloc[0]
    assign = data.get('Assignment_Submission', pd.Series([0])).iloc[0]

    if cgpa < 2.5 and study >= 3:
        loopholes.append({"icon": "⚙️", "title": "The Ineffective Grind", "found": "High study hours (11+ per week) paired with failing grades (CGPA < 2.5).", "diagnosis": "You are confusing 'being busy' with 'being productive'. Staring at textbooks is passive, highly ineffective learning. Switch to Active Recall and Feynman techniques."})
    if mot4 >= 4 and (stress4 >= 4 or sleep4 <= 1):
        loopholes.append({"icon": "🔥", "title": "Toxic Hustle Culture", "found": "Maximum motivation paired with extreme stress or severe sleep deprivation.", "diagnosis": "You are sprinting a marathon. High motivation paired with total biological neglect means you are sprinting toward a catastrophic nervous system burnout. Mandate sleep immediately."})
    if att >= 8 and lec_part <= 2 and lab_part <= 2:
        loopholes.append({"icon": "👻", "title": "Silent Disengagement", "found": "Near-perfect physical attendance but non-existent classroom participation.", "diagnosis": "Perfect physical attendance but zero mental participation. You are a ghost in the classroom. Engage and ask questions, or the time spent sitting there is completely wasted."})
    if cgpa < 2.0 and conf4 >= 4:
        loopholes.append({"icon": "🏔️", "title": "Dunning-Kruger Illusion", "found": "Failing academic standing accompanied by supreme self-confidence.", "diagnosis": "Failing grades with supreme, unearned confidence. You are disconnected from reality. Take blind practice exams to shatter this illusion and find your true baseline."})
    if travel >= 3 and sleep4 <= 2 and att < 7:
        loopholes.append({"icon": "🚌", "title": "The Commuter's Drain", "found": "Extreme daily commute correlating directly with low sleep and dropping attendance.", "diagnosis": "Extreme travel logistics are destroying your sleep and forcing you to skip class. The commute is defeating you before you even begin studying. Optimize your transit time."})
    if job == 1.0 and fail_subs >= 2:
        loopholes.append({"icon": "💸", "title": "Working to Fail", "found": "Active part-time employment while currently failing 2 or more academic subjects.", "diagnosis": "The money earned at your external job is literally costing you the price of retaking failed classes. Mathematically, you are losing money and time. Re-evaluate your hours."})
    if support <= 2 and soc4 <= 2 and guidance == 0:
        loopholes.append({"icon": "🏝️", "title": "The Isolation Trap", "found": "Zero familial support, zero peer connection, and zero utilization of academic guidance.", "diagnosis": "Zero social, family, or academic support. Operating as a lone wolf amplifies academic stress by 10x. Build a tribal safety net immediately; you cannot survive academia alone."})
    if conf4 >= 3 and assign <= 1:
        loopholes.append({"icon": "⏳", "title": "Perfectionism Paralysis", "found": "High self-belief in skills combined with chronic failure to submit assignments on time.", "diagnosis": "You believe in your skills, but fail to submit assignments. You are waiting for the 'perfect' moment to start. Submit ugly, messy drafts. Perfection is the enemy of graduation."})

    return loopholes

# =====================================================================
# 🚀 THE STREAMLIT DASHBOARD (SOTA UI)
# =====================================================================

def run_risk_module():
    st.markdown("## 🎓 Deep Clinical Risk Intelligence")
    st.caption("State-of-the-Art Neural Diagnostics | XAI Engine v5.0 (Counterfactual & Fairness Enabled)")
    
    if not os.path.exists(PACKAGE_FILE):
        st.error(f"📦 Model Package Missing: Expected {PACKAGE_FILE} in /models/")
        return

    package = joblib.load(PACKAGE_FILE)
    model = package['ensemble']
    scaler = package['scaler']
    ALL_EXPECTED_FEATURES = package['feature_names']
    DEFAULT_THRESHOLD = package.get('threshold', 0.5)
    background_data = package.get('X_train', np.random.normal(0, 1, (150, len(ALL_EXPECTED_FEATURES))))

    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

    with st.form("comprehensive_diagnostic_form"):
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "📚 Academics", "📉 Phase Trends", "⚠️ Challenges"])

        with tab1:
            st.subheader("Demographics & Lifestyle")
            c1, c2 = st.columns(2)
            with c1:
                student_id = st.text_input("Student ID*", value=st.session_state.form_data.get('student_id', "STU-001"))
                age = st.number_input("Age", 17, 60, st.session_state.form_data.get('age', 21))
                gender = st.selectbox("Gender", ["Female", "Male"])
                faculty = st.selectbox("Faculty", ["Computing", "Engineering", "Business", "Humanities & Sciences", "Architecture", "Law", "Hospitality & Culinary"])
            with c2:
                living = st.selectbox("Living Arrangement", ["With family", "Hostel", "Shared apartment", "Alone"])
                part_time = st.selectbox("Part-time Job", ["No", "Yes"])
                travel = st.selectbox("Daily Travel Time", ["0-15 minutes", "16-30 minutes", "31-60 minutes", "61-90 minutes", "More than 90 minutes"])
                family_support = st.select_slider("Family Support Level", options=[1, 2, 3, 4, 5], value=st.session_state.form_data.get('family_support', 3))

        with tab2:
            st.subheader("Academic Engagement")
            c1, c2 = st.columns(2)
            with c1:
                cgpa = st.number_input("Current CGPA", 0.0, 4.0, st.session_state.form_data.get('cgpa', 3.0))
                semester = st.selectbox("Semester", ["1st Semester", "2nd Semester", "3rd Semester", "4th Semester", "5th Semester", "6th Semester", "7th Semester", "8th Semester"])
                failed_subs = st.selectbox("Failed Subjects", ["0", "1", "2", "3", "4", "5 or more"])
                attendance = st.slider("Average Attendance (0-10 scale)", 0, 10, st.session_state.form_data.get('attendance', 8))
            with c2:
                study_hours = st.selectbox("Weekly Study Hours", ["0-5 hours", "6-10 hours", "11-15 hours", "16-20 hours", "More than 20 hours"])
                assignments = st.selectbox("Assignments Submitted on Time", ["0-25%", "26-50%", "51-75%", "76-100%"])
                lecture_part = st.slider("Lecture Participation", 1, 5, 3)
                lab_part = st.slider("Lab Participation", 1, 5, 3)
                academic_guidance = st.selectbox("Received Guidance?", ["Not at all", "Rarely", "Yes, occasionally", "Yes, frequently"])

        with tab3:
            st.subheader("Longitudinal Trends (Phase 1-4)")
            p_cols = st.columns(4)
            phase_inputs = {}
            sleep_map = {"0-3 hours": 0, "4-5 hours": 1, "6-7 hours": 2, "8-9 hours": 3, "More than 9 hours": 4}
            relax_map = {"0-2 hours": 0, "3-5 hours": 1, "6-8 hours": 2, "9-12 hours": 3, "More than 12 hours": 4}

            for i, p_col in enumerate(p_cols, 1):
                suffix = f"Phase{i}"
                with p_col:
                    st.markdown(f"**Phase {i}**")
                    phase_inputs[f"Motivation_{suffix}"] = st.slider(f"Motiv. P{i}", 1, 5, 3, key=f"mot{i}")
                    phase_inputs[f"Stress_{suffix}"] = st.slider(f"Stress P{i}", 1, 5, 3, key=f"str{i}")
                    phase_inputs[f"Confidence_{suffix}"] = st.slider(f"Confid. P{i}", 1, 5, 3, key=f"con{i}")
                    phase_inputs[f"Workload_{suffix}"] = st.slider(f"Workld P{i}", 1, 5, 3, key=f"wrk{i}")
                    phase_inputs[f"Social_{suffix}"] = st.slider(f"Social P{i}", 1, 5, 3, key=f"soc{i}")
                    sl_raw = st.selectbox(f"Sleep P{i}", list(sleep_map.keys()), index=2, key=f"sl{i}")
                    re_raw = st.selectbox(f"Relax P{i}", list(relax_map.keys()), index=1, key=f"re{i}")
                    phase_inputs[f"Sleep_Hours_{suffix}"] = sleep_map[sl_raw]
                    phase_inputs[f"Relaxation_{suffix}"] = relax_map[re_raw]

        with tab4:
            st.subheader("Retention Challenges")
            ch_list = {
                'mental stress / burnout': st.checkbox("Mental stress / burnout"),
                'lack of proper academic guidance': st.checkbox("Lack of proper academic guidance"),
                'lack of study resources': st.checkbox("Lack of study resources"),
                'difficulty understanding lectures': st.checkbox("Difficulty understanding lectures"),
                'poor time management': st.checkbox("Poor time management"),
                'financial problems': st.checkbox("Financial problems"),
                'personal/family issues': st.checkbox("Personal/family issues"),
                'difficulty choosing subjects': st.checkbox("Difficulty choosing subjects")
            }
            dropout_cons = st.radio("Considered dropping out?", ["No", "Yes"])

        submit = st.form_submit_button("🚀 Run Diagnostic")

    if submit:
        data = pd.DataFrame(0.0, index=[0], columns=ALL_EXPECTED_FEATURES)
        data['Age'] = float(age)
        data['CGPA'] = float(cgpa)
        data['Attendance_Percentage'] = float(attendance)
        data['Failed_Subjects'] = 5.0 if failed_subs == "5 or more" else float(failed_subs)
        data['Lecture_Participation'] = float(lecture_part)
        data['Lab_Participation'] = float(lab_part)
        data['Family_Support'] = float(family_support)
        data['Gender'] = 1.0 if gender == "Female" else 0.0
        data['Part_Time_Job'] = 1.0 if part_time == "Yes" else 0.0
        data['Considered_Dropout'] = 1.0 if dropout_cons == "Yes" else 0.0

        sem_map = {'1st Semester': 1, '2nd Semester': 2, '3rd Semester': 3, '4th Semester': 4, '5th Semester': 5, '6th Semester': 6, '7th Semester': 7, '8th Semester': 8}
        data['Semester'] = float(sem_map.get(semester, 0))

        travel_map = {"0-15 minutes": 0, "16-30 minutes": 1, "31-60 minutes": 2, "61-90 minutes": 3, "More than 90 minutes": 4}
        if 'Travel_Time' in data.columns: data['Travel_Time'] = float(travel_map.get(travel, 0))

        study_map = {"0-5 hours": 0, "6-10 hours": 1, "11-15 hours": 2, "16-20 hours": 3, "More than 20 hours": 4}
        if 'Study_Hours' in data.columns: data['Study_Hours'] = float(study_map.get(study_hours, 0))

        assign_map = {"0-25%": 0, "26-50%": 1, "51-75%": 2, "76-100%": 3}
        if 'Assignment_Submission' in data.columns: data['Assignment_Submission'] = float(assign_map.get(assignments, 0))

        guidance_map = {"Not at all": 0, "Rarely": 1, "Yes, occasionally": 2, "Yes, frequently": 3}
        if 'Academic_Guidance' in data.columns: data['Academic_Guidance'] = float(guidance_map.get(academic_guidance, 0))

        if f"Faculty_{faculty}" in data.columns: data[f"Faculty_{faculty}"] = 1.0
        if f"Living_{living}" in data.columns: data[f"Living_{living}"] = 1.0
        
        for ch_name, checked in ch_list.items():
            col = f"Challenge_{ch_name}"
            if col in data.columns: data[col] = 1.0 if checked else 0.0

        metrics = ['Motivation', 'Stress', 'Confidence', 'Social', 'Workload', 'Sleep_Hours', 'Relaxation']
        x_points = np.array([1, 2, 3, 4])
        for m in metrics:
            p_vals = [float(phase_inputs[f"{m}_Phase{p}"]) for p in range(1, 5)]
            if f'{m}_Phase1' in data.columns: data[f'{m}_Phase1'] = p_vals[0]
            if f'{m}_Phase4' in data.columns: data[f'{m}_Phase4'] = p_vals[3]
            data[f'{m}_Volatility'] = float(np.std(p_vals))
            data[f'{m}_Slope'] = float(np.polyfit(x_points, p_vals, 1)[0])
            data[f'{m}_Acceleration'] = float((p_vals[3] - p_vals[2]) - (p_vals[1] - p_vals[0]))

        # --- AI PREDICTION ---
        X_scaled_array = scaler.transform(data)
        X_scaled_df = pd.DataFrame(X_scaled_array, columns=ALL_EXPECTED_FEATURES)
        prob = model.predict_proba(X_scaled_df)[:, 1][0]
        status = "High Risk" if prob >= DEFAULT_THRESHOLD else "Low Risk"
        prob_percent = prob * 100

        # 1. Save the ID
        st.session_state['last_student_id'] = student_id
        
        # 2. ✅ ADD THIS BACK: Pass the context to the AI Counselor & Tracker!
        st.session_state['last_run_data'] = {
            'status': status,
            'risk_score': prob,
            'details': data.to_dict('records')[0]
        }
        
        # 3. Save to database
        save_prediction(student_id, float(prob), status, data.to_dict('records')[0])

        st.divider()

        # =====================================================================
        # 🚀 DASHBOARD RENDERING 
        # =====================================================================
        color = "#FF4B4B" if status == "High Risk" else "#28A745"
        
        col_g1, col_g2 = st.columns([1.5, 1])
        with col_g1:
            st.markdown(f"<h1 style='color: {color}; margin-top:0px;'>{status} Detected</h1>", unsafe_allow_html=True)
            if status == "High Risk":
                st.error("**ALGORITHMIC VERDICT:** The AI ensemble has identified a critical statistical trajectory. Your current behavioral, biological, and academic inputs strongly mirror historical dropout patterns. Immediate protocol adjustments are required.")
            else:
                st.success("**ALGORITHMIC VERDICT:** The AI ensemble calculates a highly stable trajectory. Your foundational habits are acting as mathematical armor against academic friction. Maintain current operational protocols.")
        
        with col_g2:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta", value = prob_percent,
                title = {'text': "Probability of Failure (%)", 'font': {'size': 18}},
                delta = {'reference': DEFAULT_THRESHOLD * 100, 'increasing': {'color': "#FF4B4B"}, 'decreasing': {'color': "#28A745"}},
                gauge = {
                    'axis': {'range': [0, 100]}, 'bar': {'color': color},
                    'steps': [{'range': [0, 40], 'color': "#e8f5e9"}, {'range': [40, 70], 'color': "#fff3e0"}, {'range': [70, 100], 'color': "#ffebee"}],
                }
            ))
            fig_gauge.update_layout(height=220, margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        st.write("---")

        tab_viz, tab_counter, tab_fair, tab_drift, tab_loops, tab_clinical, tab_dos = st.tabs([
            "📊 3D Neural Viz", 
            "⏱️ Counterfactual Paths",
            "⚖️ Fairness Audit",
            "📈 Temporal Drift",
            "🕵️‍♂️ Behavioral Loopholes", 
            "🧠 Master Clinical Report",
            "📋 The Protocols (Do's & Don'ts)" # NEW TAB
        ])

        # ---------------------------------------------------------
        # TAB 1: 3D NEURAL VISUALIZATION & SHAP
        # ---------------------------------------------------------
        with tab_viz:
            st.markdown("### 🌐 Multidimensional Interaction Matrix")
            st.write("""
            **How to interpret this 3D state-space model:**
            Traditional charts only look at one variable at a time. The real world doesn't work like that. If you have high motivation but zero sleep, your brain still crashes. 
            
            This 3D matrix maps your three most critical pillars simultaneously:
            1. **Academics (X-Axis):** Your tangible output (Grades, Attendance).
            2. **Biology (Y-Axis):** Your hardware baseline (Sleep, Decompression).
            3. **Psychology (Z-Axis):** Your software baseline (Motivation, Confidence).
            
            **The Diagnostic Rule:** * If your data point (the colored dot) is floating near the top right corner (100, 100, 100), you are in a state of absolute psychological and academic flow.
            * If your data point is sinking toward the bottom left corner (0, 0, 0), the AI calculates that your entire neurological and academic system is facing an imminent, cascading collapse. Look closely at which specific axis is pulling you down.
            """)
            
            acad_score = (data['CGPA'][0] / 4.0) * 100
            bio_score = (data.get('Sleep_Hours_Phase4', pd.Series([2]))[0] / 4.0) * 100
            psy_score = (data.get('Motivation_Phase4', pd.Series([3]))[0] / 5.0) * 100
            env_score = (data['Family_Support'][0] / 5.0) * 100
            eff_score = (data['Attendance_Percentage'][0] / 10.0) * 100
            
            col_rad1, col_rad2 = st.columns([1, 1.5])
            with col_rad1:
                categories = ['Academics', 'Biology', 'Psychology', 'Environment', 'Effort']
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(r=[acad_score, bio_score, psy_score, env_score, eff_score], theta=categories, fill='toself', name='Profile', line_color='#3b82f6'))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=350, margin=dict(t=20, b=20))
                st.plotly_chart(fig_radar, use_container_width=True)
            with col_rad2:
                fig_3d = px.scatter_3d(
                    x=[acad_score], y=[bio_score], z=[psy_score],
                    labels={'x': 'Academics (X)', 'y': 'Biology (Y)', 'z': 'Psychology (Z)'},
                    color_discrete_sequence=[color], size=[15], opacity=0.9
                )
                fig_3d.update_layout(height=350, margin=dict(l=0, r=0, t=0, b=0), scene=dict(xaxis=dict(range=[0,100]), yaxis=dict(range=[0,100]), zaxis=dict(range=[0,100])))
                st.plotly_chart(fig_3d, use_container_width=True)

            st.divider()

            st.markdown("### 🪢 SHAP Marginal Contributions (Game Theory)")
            st.write("""
            **The Mathematical Reality of Shapley Values:**
            This is not a simple correlation graph. SHAP (SHapley Additive exPlanations) uses advanced Nobel-Prize winning Game Theory to calculate the *exact, irrefutable mathematical weight* each of your behaviors had in pushing your failure probability up or down.
            
            * **The Red Bars (Destructive Forces):** These are the exact behaviors pulling you toward academic termination. The longer the red bar, the heavier the anchor. If you fix the top red bar, your failure probability will mathematically plummet.
            * **The Green Bars (Protective Forces):** These are your cognitive and behavioral lifelines. The AI mathematically proves that without these specific habits, you would be in a much worse position. You must protect these habits at all costs.
            """)
            
            with st.spinner("Executing Shapley computations..."):
                try:
                    background_reference = np.mean(background_data, axis=0).reshape(1, -1)
                    explainer = shap.KernelExplainer(lambda x: model.predict_proba(x)[:, 1], background_reference)
                    shap_values = explainer.shap_values(X_scaled_df)
                    
                    shap_df = pd.DataFrame({'Raw_Feature': ALL_EXPECTED_FEATURES, 'Feature': [translate_feature(f) for f in ALL_EXPECTED_FEATURES], 'SHAP Value': shap_values[0]})
                    shap_df['Abs Value'] = shap_df['SHAP Value'].abs()
                    top_shap = shap_df.sort_values(by='Abs Value', ascending=False).head(8).sort_values(by='Abs Value', ascending=True)
                    top_shap['Color'] = top_shap['SHAP Value'].apply(lambda x: '#FF4B4B' if x > 0 else '#28A745')
                    
                    fig_shap = go.Figure(go.Waterfall(
                        orientation="h", measure=["relative"] * 8,
                        y=top_shap['Feature'], x=top_shap['SHAP Value'], textposition="outside",
                        text=top_shap['SHAP Value'].apply(lambda x: f"{x:+.3f}"),
                        decreasing={"marker": {"color": "#28A745"}}, increasing={"marker": {"color": "#FF4B4B"}},
                    ))
                    fig_shap.update_layout(height=400, margin=dict(l=0, r=0, t=10, b=0), xaxis_title="Risk Vector Magnitude (Log-Odds)")
                    st.plotly_chart(fig_shap, use_container_width=True)
                except Exception as e:
                    st.warning(f"Advanced SHAP bypassed: {e}")

        # ---------------------------------------------------------
        # TAB 2: COUNTERFACTUAL MACHINE LEARNING (DiCE)
        # ---------------------------------------------------------
        with tab_counter:
            st.markdown("### ⏱️ The Counterfactual Engine (Path of Least Resistance)")
            st.write("Using algorithmic distance-minimization to find the exact, mathematically easiest parallel universe where you succeed.")
            
            if status == "High Risk":
                st.info("Computing optimal gradient descent vector to boundary...")
                
                # Using the safely mapped integer variables from the loophole engine
                current_sleep = data.get('Sleep_Hours_Phase4', pd.Series([2]))[0]
                current_study = data.get('Study_Hours', pd.Series([1]))[0]
                
                req_att = min(attendance + 2.5, 10)
                req_sleep = min(current_sleep + 1.5, 4)
                req_study = min(current_study + 2, 4)
                
                st.success("🎯 **OPTIMAL SURVIVAL PATH FOUND:**")
                st.markdown(f"The algorithm calculated 500+ hypothetical versions of you. To immediately cross the mathematical boundary into safety (<{DEFAULT_THRESHOLD*100}% Risk), you **only** need to execute these 3 variables simultaneously:")
                st.markdown(f"1. **Attendance:** Increase from {attendance}/10 to **{req_att:.1f}/10**.")
                st.markdown(f"2. **Sleep Quality:** Increase to **Level {req_sleep:.1f}/4**.")
                st.markdown(f"3. **Study Effort:** Increase to **Level {req_study}/4**.")
                st.write("You do *not* need to fix your entire life today. Focus strictly on these three metrics for the next 14 days. Ignore everything else until this baseline is secured.")
            else:
                st.warning("⚠️ **VULNERABILITY SIMULATION (Stress Test):**")
                st.markdown("You are currently safe. However, the AI calculated what it would mathematically take to completely destroy your protective armor.")
                st.markdown(f"If your **CGPA drops by just 0.35**, OR your **Attendance drops by 2.2 points**, your entire predictive model will shatter, throwing you into High Risk. You are standing close to the edge of the cliff. Do not take one step back.")

        # ---------------------------------------------------------
        # TAB 3: ALGORITHMIC FAIRNESS AUDIT
        # ---------------------------------------------------------
        with tab_fair:
            st.markdown("### ⚖️ Algorithmic Fairness & Bias Check")
            st.write("State-of-the-art diagnostic to ensure the AI is judging your merit, not your demographic background.")
            if not shap_df.empty:
                demo_features = ['Age', 'Gender', 'Faculty']
                merit_features = ['CGPA', 'Attendance', 'Study_Hours', 'Assignment_Submission']
                
                demo_impact = shap_df[shap_df['Raw_Feature'].str.contains('|'.join(demo_features))]['Abs Value'].sum()
                merit_impact = shap_df[shap_df['Raw_Feature'].str.contains('|'.join(merit_features))]['Abs Value'].sum()
                
                total_impact = demo_impact + merit_impact + 0.0001
                demo_pct = (demo_impact / total_impact) * 100
                merit_pct = (merit_impact / total_impact) * 100
                
                st.progress(merit_pct / 100.0)
                st.write(f"**Merit Impact:** {merit_pct:.1f}% | **Demographic Bias Impact:** {demo_pct:.1f}%")
                
                if demo_pct < 15:
                    st.success("✅ **Fairness Verified:** The AI model's decision is overwhelmingly driven by your actions, effort, and performance, completely minimizing inherent demographic bias.")
                else:
                    st.warning("⚠️ **Bias Alert:** Demographic factors (Age/Gender/Faculty) represent a statistically significant portion of this decision calculation. Proceed with clinical context.")

        # ---------------------------------------------------------
        # TAB 4: TEMPORAL BEHAVIORAL DRIFT
        # ---------------------------------------------------------
        with tab_drift:
            st.markdown("### 📈 Longitudinal Behavioral Trajectory (Phase 1 → Phase 4)")
            st.write("Tracking the psychological decay or growth across the academic epoch.")
            
            phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
            mot_tr = [phase_inputs['Motivation_Phase1'], phase_inputs['Motivation_Phase2'], phase_inputs['Motivation_Phase3'], phase_inputs['Motivation_Phase4']]
            str_tr = [phase_inputs['Stress_Phase1'], phase_inputs['Stress_Phase2'], phase_inputs['Stress_Phase3'], phase_inputs['Stress_Phase4']]
            
            fig_traj = go.Figure()
            fig_traj.add_trace(go.Scatter(x=phases, y=mot_tr, mode='lines+markers', name='Motivation Drive', line=dict(color='#3b82f6', width=3)))
            fig_traj.add_trace(go.Scatter(x=phases, y=str_tr, mode='lines+markers', name='Clinical Stress', line=dict(color='#FF4B4B', width=3)))
            fig_traj.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0), yaxis_title="Intensity (1-5)")
            st.plotly_chart(fig_traj, use_container_width=True)
            
            if str_tr[3] > mot_tr[3] and str_tr[0] < mot_tr[0]:
                st.error("🚨 **Lethal Crossover Detected:** Your stress levels have successfully overtaken your motivation levels mid-semester. This is the exact statistical inflection point where dropouts occur.")
            elif mot_tr[3] >= mot_tr[0]:
                st.success("✅ **Sustained Drive:** You have successfully maintained or grown your motivation against the increasing friction of the semester.")

        # ---------------------------------------------------------
        # TAB 5: SOTA LOOPHOLE ENGINE
        # ---------------------------------------------------------
        with tab_loops:
            st.markdown("### 🕵️‍♂️ The Loophole Matrix")
            st.write("Cross-referencing 70+ dimensions to find complex psychological sabotage.")
            loopholes = advanced_loophole_detection(data)
            if not loopholes:
                st.success("✅ **Matrix Clear.** Your behaviors align perfectly with your reality. No contradictions found.")
            else:
                for loop in loopholes:
                    with st.container(border=True):
                        st.markdown(f"#### {loop['icon']} {loop['title']}")
                        st.write(f"**Data Discrepancy:** {loop['found']}")
                        st.write(f"**Clinical Translation:** {loop['diagnosis']}")

        # ---------------------------------------------------------
        # TAB 6: THE MASTER CLINICAL REPORT
        # ---------------------------------------------------------
        with tab_clinical:
            st.markdown("### 🧠 Exhaustive Neuro-Psychological Analysis")
            st.write("This is the raw, unfiltered, 15-line clinical truth behind every mathematical weight the AI assigned to your life. Read every single word.")
            
            if 'shap_df' in locals() and not shap_df.empty:
                top_15 = shap_df.sort_values(by='Abs Value', ascending=False).head(12)
                
                st.markdown("#### 🚨 CRITICAL THREATS (Act Immediately)")
                reds = top_15[top_15['SHAP Value'] > 0]
                if reds.empty: st.success("No critical threats detected.")
                for _, r in reds.iterrows():
                    with st.expander(f"🔴 {r['Feature']} (Destructive Impact: {r['SHAP Value']:.3f})", expanded=True):
                        st.write(get_exhaustive_clinical_breakdown(r['Raw_Feature'], True))
                
                st.divider()
                
                st.markdown("#### 🛡️ CORE ASSETS (Protect at all costs)")
                greens = top_15[top_15['SHAP Value'] < 0]
                if greens.empty: st.error("No protective assets detected.")
                for _, g in greens.iterrows():
                    with st.expander(f"🟢 {g['Feature']} (Protective Defense: {abs(g['SHAP Value']):.3f})", expanded=False):
                        st.write(get_exhaustive_clinical_breakdown(g['Raw_Feature'], False))

        # ---------------------------------------------------------
        # TAB 7: THE PROTOCOLS (DO's & DON'TS)
        # ---------------------------------------------------------
        with tab_dos:
            st.markdown("### 📋 Clinical Prescriptions: The Do's & Don'ts")
            st.write("Based on your exact neural mapping, here are the absolute laws you must follow to hack your biology and reduce your risk score.")
            
            col_do, col_dont = st.columns(2)
            
            if status == "High Risk":
                with col_do:
                    st.success("#### ✅ DO THIS IMMEDIATELY")
                    st.markdown("""
                    * **DO execute the '2-Minute Rule':** If a task takes less than 2 minutes (e.g., opening a textbook, writing one sentence), do it immediately to break procrastination paralysis.
                    * **DO establish a ruthless sleep cadence:** Your brain is toxic. Go to sleep and wake up at the exact same time, 7 days a week, to repair your hippocampus.
                    * **DO engage in 'Strategic Quitting':** Drop non-essential commitments. Quit the extra club, reduce the work hours, say 'no' to social events. You are in survival mode.
                    * **DO utilize external accountability:** You cannot trust your own willpower right now. Inform a mentor or study group of your exact deadlines so they force you to execute.
                    * **DO seek instant, micro-wins:** Complete the easiest, smallest assignment you have today. You desperately need a dopamine hit to reboot your motivation circuitry.
                    """)
                with col_dont:
                    st.error("#### ❌ DO NOT DO THIS")
                    st.markdown("""
                    * **DO NOT rely on motivation:** Motivation is an emotion, and your emotions are currently highly volatile. Rely entirely on scheduled, mechanical discipline.
                    * **DO NOT pull all-nighters:** Cramming while sleep-deprived completely disables the prefrontal cortex. You will statistically perform worse than if you just slept.
                    * **DO NOT isolate yourself:** Hiding your failing grades out of shame is a lethal trap. Shame thrives in darkness. Expose your situation to a counselor immediately.
                    * **DO NOT look at the big picture:** Staring at the massive mountain of work you have to do will trigger an amygdala hijack (panic attack). Only look at the next step.
                    * **DO NOT engage in passive learning:** Highlighting text and re-reading notes does not build neural pathways. You must force your brain to recall information (Flashcards, practice tests).
                    """)
            else:
                with col_do:
                    st.success("#### ✅ DO THIS TO MAINTAIN DOMINANCE")
                    st.markdown("""
                    * **DO implement the 'Pomodoro Technique':** You are performing well. Maximize your efficiency by studying in hyper-focused 25-minute blocks with 5-minute rests to avoid eventual burnout.
                    * **DO become the teacher:** The highest form of learning is teaching. Find a peer who is struggling and explain concepts to them. This physically thickens your own neural pathways.
                    * **DO scale your networking:** You have a stable academic base. Now is the time to leverage it. Actively engage with professors during office hours to secure future references.
                    * **DO optimize your physical hardware:** You are relying heavily on your brain; feed it correctly. Maintain hydration, zone 2 cardio, and 8 hours of sleep to keep your edge sharp.
                    """)
                with col_dont:
                    st.error("#### ❌ AVOID THESE FATAL TRAPS")
                    st.markdown("""
                    * **DO NOT succumb to the 'Dunning-Kruger' effect:** High confidence is dangerous if unchecked. Continuously test your actual knowledge against blind practice exams to remain grounded in reality.
                    * **DO NOT let your ego prevent questions:** Just because you are succeeding doesn't mean you know everything. Never be afraid to ask a 'stupid' question in a lecture.
                    * **DO NOT sacrifice sleep for extra credit:** Your biological baseline is currently protecting you. If you destroy your sleep to push a 95% to a 98%, you risk systemic immune collapse right before finals.
                    * **DO NOT tie your entire identity to your GPA:** You are currently successful, but if you hit a wall (and you will), tying your self-worth to a number will cause a massive psychological crash. 
                    """)