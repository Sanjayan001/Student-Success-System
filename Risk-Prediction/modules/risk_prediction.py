import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from database.app_db import DB_PATH, save_prediction
from datetime import datetime

# This finds the 'modules' folder where this script lives
CURRENT_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to 'Risk-Prediction' then into 'models' and 'database'
PACKAGE_FILE = os.path.join(CURRENT_MODULE_DIR, "..", "models", "student_dropout_model_1.pkl")
DB_FOLDER_PATH = os.path.join(CURRENT_MODULE_DIR, "..", "database")

def run_risk_module():
    st.markdown("## 🎓 Student Risk Intelligence Diagnostic")
    st.caption("Precision Behavioral Analytics | Unified Stable-Engine v4.0")
    
    if not os.path.exists(PACKAGE_FILE):
        st.error(f"📦 Model Package Missing: Expected {PACKAGE_FILE} in /models/")
        st.info("Please ensure you have saved your model using the 'Model 1 Package' code.")
        return

    # --- THE UNIFIED LOAD ---
    package = joblib.load(PACKAGE_FILE)
    model = package['ensemble']
    scaler = package['scaler']
    ALL_EXPECTED_FEATURES = package['feature_names']
    DEFAULT_THRESHOLD = package.get('threshold', 0.5)

    # --- FORM PERSISTENCE LOGIC ---
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}


    # --- MAIN UI FORM ---
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
                    phase_inputs[f"Motivation_{suffix}"] = st.slider(f"Motivation P{i}", 1, 5, 3, key=f"mot{i}")
                    phase_inputs[f"Stress_{suffix}"] = st.slider(f"Stress P{i}", 1, 5, 3, key=f"str{i}")
                    phase_inputs[f"Confidence_{suffix}"] = st.slider(f"Confidence P{i}", 1, 5, 3, key=f"con{i}")
                    phase_inputs[f"Workload_{suffix}"] = st.slider(f"Workload P{i}", 1, 5, 3, key=f"wrk{i}")
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

        submit = st.form_submit_button("🚀 Run AI Risk Diagnostic")

    if submit:
        # --- 1. DATA PREPARATION ---
        data = pd.DataFrame(0.0, index=[0], columns=ALL_EXPECTED_FEATURES)
        
        # Numeric Direct Mappings
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

        # --- THE MISSING MAPPINGS ---
        
        # Semester
        sem_map = {'1st Semester': 1, '2nd Semester': 2, '3rd Semester': 3, '4th Semester': 4, 
                   '5th Semester': 5, '6th Semester': 6, '7th Semester': 7, '8th Semester': 8}
        data['Semester'] = float(sem_map.get(semester, 0))

        # Travel Time
        travel_map = {"0-15 minutes": 0, "16-30 minutes": 1, "31-60 minutes": 2, "61-90 minutes": 3, "More than 90 minutes": 4}
        if 'Travel_Time' in data.columns:
            data['Travel_Time'] = float(travel_map.get(travel, 0))

        # Study Hours
        study_map = {"0-5 hours": 0, "6-10 hours": 1, "11-15 hours": 2, "16-20 hours": 3, "More than 20 hours": 4}
        if 'Study_Hours' in data.columns:
            data['Study_Hours'] = float(study_map.get(study_hours, 0))

        # Assignment Submission
        assign_map = {"0-25%": 0, "26-50%": 1, "51-75%": 2, "76-100%": 3}
        if 'Assignment_Submission' in data.columns:
            data['Assignment_Submission'] = float(assign_map.get(assignments, 0))

        # Academic Guidance
        guidance_map = {"Not at all": 0, "Rarely": 1, "Yes, occasionally": 2, "Yes, frequently": 3}
        if 'Academic_Guidance' in data.columns:
            data['Academic_Guidance'] = float(guidance_map.get(academic_guidance, 0))

        # --- END OF NEW MAPPINGS ---

        # Handle Dynamic Faculty & Living Columns
        if f"Faculty_{faculty}" in data.columns: data[f"Faculty_{faculty}"] = 1.0
        if f"Living_{living}" in data.columns: data[f"Living_{living}"] = 1.0
        
        # Handle Challenges Checkboxes
        for ch_name, checked in ch_list.items():
            col = f"Challenge_{ch_name}"
            if col in data.columns: data[col] = 1.0 if checked else 0.0

        # --- 2. TRAJECTORY ENGINE ---
        metrics = ['Motivation', 'Stress', 'Confidence', 'Social', 'Workload', 'Sleep_Hours', 'Relaxation']
        x_points = np.array([1, 2, 3, 4])
        for m in metrics:
            p_vals = [float(phase_inputs[f"{m}_Phase{p}"]) for p in range(1, 5)]
            if f'{m}_Phase1' in data.columns: data[f'{m}_Phase1'] = p_vals[0]
            if f'{m}_Phase4' in data.columns: data[f'{m}_Phase4'] = p_vals[3]
            data[f'{m}_Volatility'] = float(np.std(p_vals))
            data[f'{m}_Slope'] = float(np.polyfit(x_points, p_vals, 1)[0])
            data[f'{m}_Acceleration'] = float((p_vals[3] - p_vals[2]) - (p_vals[1] - p_vals[0]))

        # --- 3. PREDICTION ---
        # 1. Scale the data (this returns a NumPy array, which causes the warning)
        X_scaled_array = scaler.transform(data)
        
        # 2. Convert it BACK to a DataFrame so the model sees the feature names
        X_scaled_df = pd.DataFrame(X_scaled_array, columns=ALL_EXPECTED_FEATURES)
        
        # 3. Predict using the DataFrame instead of the array
        prob = model.predict_proba(X_scaled_df)[:, 1][0]
        status = "High Risk" if prob >= DEFAULT_THRESHOLD else "Low Risk"

        # --- SESSION HANDOVER ---
        st.session_state['last_student_id'] = student_id
        st.session_state['last_run_data'] = {
            'status': status,
            'risk_score': prob,
            'details': data.to_dict('records')[0]
        }

        # --- 4. VISUAL ASSESSMENT (High-Impact Header) ---
        # UPDATED: Added styled HTML headers for the risk profile
        st.divider()
        res_col1, res_col2 = st.columns([1, 1])
        with res_col1:
            color = "#FF4B4B" if status == "High Risk" else "#28A745"
            st.markdown(f"<h2 style='color: {color}; margin-bottom:0;'>{status} Profile Detected</h2>", unsafe_allow_html=True)
            st.metric("Risk Probability", f"{prob:.4f}")
        
        with res_col2:
            st.write("📊 **Neural Decision Confidence**")
            st.progress(min(float(prob), 1.0))
            st.caption("Confidence score derived from Gradient Boosted Ensemble weights.")

        # --- 5. ENHANCED HUMAN-CENTRIC XAI REPORT ---
        st.write("---")
        st.header("🔍 Intelligence Strategy Report")
        
        cv = data.iloc[0] 

        # A. THE EXECUTIVE SUMMARY (High-Fidelity Banner)
        risk_color = "#FF4B4B" if status == "High Risk" else "#28A745"
        risk_bg = "#FF4B4B15" if status == "High Risk" else "#28A74515"
        
        st.markdown(f"""
            <div style="background-color: {risk_bg}; padding: 30px; border-radius: 20px; border: 1px solid {risk_color}; margin-bottom: 25px;">
                <h3 style="margin:0; color: {risk_color}; font-size: 24px;">Executive Summary</h3>
                <p style="margin:10px 0 0 0; font-size: 18px; color: #1D1D1F; line-height: 1.6;">
                    The AI Ensemble has analyzed <b>{len(ALL_EXPECTED_FEATURES)} behavioral markers</b>. 
                    {'<b>CRITICAL:</b> This student is showing patterns highly consistent with historical dropout cases. Immediate intervention is advised.' if status == 'High Risk' else '<b>STABLE:</b> The student is currently maintaining a path toward successful completion. Protective factors are strong.'}
                </p>
            </div>
        """, unsafe_allow_html=True)

        # UPDATED: B. THE "CORE FOUR" DEEP DIAGNOSTIC (Now a professional 2x2 Grid)
        grid_row1_col1, grid_row1_col2 = st.columns(2)
        grid_row2_col1, grid_row2_col2 = st.columns(2)
        
        with grid_row1_col1:
            with st.container(border=True):
                st.markdown("#### 🧠 Behavioral Momentum")
                conf_acc = cv.get('Confidence_Acceleration', 0)
                if conf_acc < -0.1: st.error(f"Trend: Downward Spiral ({conf_acc:.2f})")
                elif conf_acc > 0.1: st.success(f"Trend: Growth Mindset (+{conf_acc:.2f})")
                else: st.info("Trend: Steady Plateau")
                st.caption("Self-belief relative to increasing task difficulty.")

        with grid_row1_col2:
            with st.container(border=True):
                st.markdown("#### 🛌 Biological Battery")
                sleep_slp = cv.get('Sleep_Hours_Slope', 0)
                if sleep_slp < -0.1: st.error(f"Trend: Energy Depletion ({sleep_slp:.2f})")
                else: st.success("Trend: Healthy Rest Cycle")
                st.caption("Foundation for cognitive retention and memory.")

        with grid_row2_col1:
            with st.container(border=True):
                st.markdown("#### 📈 Engagement Rhythm")
                mot_vol = cv.get('Motivation_Volatility', 0)
                if mot_vol > 1.2: st.warning(f"Trend: Reactive/Panic Study ({mot_vol:.2f})")
                else: st.success("Trend: Proactive Discipline")
                st.caption("Consistency of study habits vs reactive cramming.")

        with grid_row2_col2:
            with st.container(border=True):
                st.markdown("#### ⚓ Institutional Anchor")
                att = cv.get('Attendance_Percentage', 0)
                if att < 7: st.error(f"Status: Loose Tethering ({att}/10)")
                else: st.success(f"Status: Strong Tethering ({att}/10)")
                st.caption("Physical and social connection to the campus.")

        # C. Recommended Strategy (Prescription)
        st.write("")
        with st.container(border=True):
            st.subheader("🎯 Recommended Success Strategy")
            if status == "High Risk":
                strat_c1, strat_c2, strat_c3 = st.columns(3)
                strat_c1.markdown("**1. Break the Spiral**\nAssign one 15-min success task to rebuild confidence.")
                strat_c2.markdown("**2. Sleep Audit**\nMandatory rest schedule adjustment for cognitive recovery.")
                strat_c3.markdown("**3. Human Connection**\nHigh-touch face-to-face academic advisory meeting.")
            else:
                st.success("✅ **Maintain Momentum:** Student is self-regulating effectively. Reinforce current routines.")

        # D. TECHNICAL WEIGHTS
        with st.expander("🛠️ View Decision Logic (Neural Weights)"):
            importance_df = pd.DataFrame({
                "Intelligence Signal": [n.replace("_", " ").title() for n in ALL_EXPECTED_FEATURES[:15]],
                "Normalized Value": [f"{v:.4f}" for v in X_scaled_df.values[0][:15]]
            })
            st.table(importance_df)

        save_prediction(student_id, float(prob), status, data.to_dict('records')[0])

    # --- 6. THE "DECISION LABORATORY" (Advanced Simulation Suite) ---
    if 'last_run_data' in st.session_state:
        st.write("---")
        st.header("🧪 Prescriptive Simulation Laboratory")
        
        # UPDATED: Added outer container for a dashboard look
        with st.container(border=True):
            st.info("💡 Engineer a recovery strategy by adjusting the levers below to see real-time risk reduction.")

            with st.expander("🚀 OPEN SIMULATION THEATER", expanded=False):
                original_details = st.session_state['last_run_data']['details'].copy()
                actual_prob = st.session_state['last_run_data']['risk_score']
                
                # UPDATED: Cleaned up column naming for the 3-pillar dashboard
                sim_col_ac, sim_col_bh, sim_col_bio = st.columns(3)
                
                with sim_col_ac:
                    st.markdown("#### 📚 Academic Levers")
                    sim_cgpa = st.slider("Modify CGPA", 0.0, 4.0, float(original_details['CGPA']), 0.05)
                    sim_att = st.slider("Modify Attendance", 0.0, 10.0, float(original_details['Attendance_Percentage']), 0.5)
                    sim_fail = st.select_slider("Subjects Failed", options=[0, 1, 2, 3, 4, 5], value=int(original_details['Failed_Subjects']))
                
                with sim_col_bh:
                    st.markdown("#### 🧠 Behavioral Levers")
                    sim_mot = st.slider("Boost Motivation", 1.0, 5.0, float(original_details['Motivation_Phase4']), 0.1)
                    sim_conf = st.slider("Boost Confidence", 1.0, 5.0, float(original_details['Confidence_Phase4']), 0.1)
                    sim_stress = st.slider("Internal Stress Level", 1.0, 5.0, float(original_details['Stress_Phase4']), 0.1)

                with sim_col_bio:
                    st.markdown("#### 🛌 Biological Levers")
                    sim_sleep = st.slider("Sleep Hygiene (0-4)", 0, 4, int(original_details.get('Sleep_Hours_Phase4', 2)))
                    sim_relax = st.slider("Relaxation Level (0-4)", 0, 4, int(original_details.get('Relaxation_Phase4', 2)))
                    sim_support = st.slider("Family Support (1-5)", 1, 5, int(original_details['Family_Support']))

                # 1. Update Simulation DataFrame
                sim_df = pd.DataFrame([original_details])
                sim_df['CGPA'] = sim_cgpa
                sim_df['Attendance_Percentage'] = sim_att
                sim_df['Failed_Subjects'] = float(sim_fail)
                sim_df['Motivation_Phase4'] = sim_mot
                sim_df['Confidence_Phase4'] = sim_conf
                sim_df['Stress_Phase4'] = sim_stress
                sim_df['Sleep_Hours_Phase4'] = float(sim_sleep)
                sim_df['Relaxation_Phase4'] = float(sim_relax)
                sim_df['Family_Support'] = float(sim_support)

                # 2. Re-calculate Probability using Scaler
                sim_scaled = scaler.transform(sim_df[ALL_EXPECTED_FEATURES])
                sim_scaled_df = pd.DataFrame(sim_scaled, columns=ALL_EXPECTED_FEATURES)
                sim_prob = model.predict_proba(sim_scaled_df)[:, 1][0]
                
                st.divider()

                # PRESERVED: Your Plotly Impact Matrix
                res_c1, res_c2 = st.columns([1, 2])
                with res_c1:
                    st.markdown("#### 🔮 Outcome Projection")
                    diff = sim_prob - actual_prob
                    st.metric("Projected Risk", f"{sim_prob:.2%}", delta=f"{diff:+.2%}", delta_color="inverse")
                    
                    if sim_prob < DEFAULT_THRESHOLD:
                        st.success("✅ INTERVENTION SUCCESS")
                    else:
                        st.warning("⚠️ INSUFFICIENT IMPACT")

                with res_c2:
                    st.markdown("#### 📊 Sensitivity Impact Matrix")
                    impact_data = pd.DataFrame({
                        "Category": ["Academic", "Behavioral", "Biological"],
                        "Gravity": [abs(sim_cgpa - original_details['CGPA']) * 2, 
                                    abs(sim_mot - original_details['Motivation_Phase4']) * 1.5,
                                    abs(sim_sleep - original_details.get('Sleep_Hours_Phase4', 2)) * 1.2]
                    })
                    import plotly.express as px
                    fig_impact = px.bar(impact_data, x="Gravity", y="Category", orientation='h', 
                                         color="Gravity", color_continuous_scale="Viridis", height=200)
                    fig_impact.update_layout(margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
                    # UPDATED: Used standard Streamlit 2026 syntax for responsive charts
                    st.plotly_chart(fig_impact, use_container_width=True)

                # PRESERVED: Your full SQLite logic and Digital Receipt UI
                if st.button("📝 Finalize Intervention Prescription", width="stretch", type="primary"):
                    from database.app_db import DB_PATH 
                    
                    try:
                        import sqlite3
                        conn = sqlite3.connect(DB_PATH)
                        cursor = conn.cursor()
                        
                        risk_reduction = actual_prob - sim_prob
                        
                        cursor.execute("""
                            INSERT OR REPLACE INTO intervention_goals 
                            (student_id, target_cgpa, target_attendance, target_failed_subs, 
                            target_motivation, target_confidence, target_stress, 
                            target_sleep, target_relaxation, target_support, predicted_risk_reduction)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            st.session_state['last_student_id'],
                            float(sim_cgpa), float(sim_att), float(sim_fail), 
                            float(sim_mot), float(sim_conf), float(sim_stress), 
                            float(sim_sleep), float(sim_relax), float(sim_support), 
                            float(risk_reduction)
                        ))
                        
                        conn.commit()
                        conn.close()
                        
                        st.balloons()
                        st.success(f"🎯 Clinical Prescription Finalized for {st.session_state['last_student_id']}")

                        with st.expander("📄 View Finalized Intervention Summary", expanded=True):
                            st.markdown(f"### Strategy Archive: {st.session_state['last_student_id']}")
                            st.info("All 9 behavioral and academic levers have been synced to the Research Database.")
                            
                            meta1, meta2, meta3 = st.columns(3)
                            
                            with meta1:
                                st.metric(label="Target CGPA", value=f"{sim_cgpa:.2f}")
                                st.metric(label="Sleep Hygiene", value=f"{sim_sleep} / 4")
                                
                            with meta2:
                                st.metric(label="Attendance Goal", value=f"{sim_att:.1f}%")
                                st.metric(label="Stress Cap", value=f"{sim_stress} / 5")
                                
                            with meta3:
                                improvement = actual_prob - sim_prob
                                st.metric(label="Risk Reduction", value=f"{improvement:.2%}", delta="Optimized")
                                st.metric(label="Motivation Target", value=f"{sim_mot} / 5")

                            st.caption(f"Prescription Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                        
                    except Exception as e:
                        st.error(f"❌ Synchronization Failure: {e}")
                        st.warning("Ensure the database is not open in another application (like DB Browser).")
