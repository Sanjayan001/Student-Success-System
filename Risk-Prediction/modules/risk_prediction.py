import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np
from database.app_db import save_prediction

# --- ASSET PATHS ---
MODEL_DIR = "models"
MODEL_FILE = os.path.join(MODEL_DIR, 'final_ensemble_model.pkl')
SELECTOR_FILE = os.path.join(MODEL_DIR, 'feature_selector.pkl')
SCALER_FILE = os.path.join(MODEL_DIR, 'main_scaler.pkl')

def run_risk_module():
    st.markdown("## 🎓 Student Risk Intelligence Diagnostic")
    
    if not os.path.exists(MODEL_FILE):
        st.error("AI Model files missing. Please ensure /models/ contains your trained pkl files.")
        return

    # Load Research Brain
    model = joblib.load(MODEL_FILE)
    selector = joblib.load(SELECTOR_FILE)
    scaler = joblib.load(SCALER_FILE)
    ALL_EXPECTED_FEATURES = scaler.feature_names_in_

    # --- FORM PERSISTENCE LOGIC (Prevents data clearing) ---
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
                gender = st.selectbox("Gender", ["Female", "Male"], index=0 if st.session_state.form_data.get('gender') == "Female" else 1)
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
            st.write("Identify current barriers:")
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
        # Save current state to prevent clearing
        st.session_state.form_data = {'student_id': student_id, 'age': age, 'cgpa': cgpa, 'attendance': attendance, 'family_support': family_support}

        # --- 1. DATA PREPARATION ---
        data = pd.DataFrame(0.0, index=[0], columns=ALL_EXPECTED_FEATURES)
        data['Age'] = float(age); data['CGPA'] = float(cgpa); data['Attendance_Percentage'] = float(attendance)
        data['Failed_Subjects'] = 5.0 if failed_subs == "5 or more" else float(failed_subs)
        data['Lecture_Participation'] = float(lecture_part); data['Lab_Participation'] = float(lab_part)
        data['Family_Support'] = float(family_support)
        data['Gender'] = 1.0 if gender == "Female" else 0.0
        data['Part_Time_Job'] = 1.0 if part_time == "Yes" else 0.0
        data['Considered_Dropout'] = 1.0 if dropout_cons == "Yes" else 0.0

        sem_map = {'1st Semester': 1, '2nd Semester': 2, '3rd Semester': 3, '4th Semester': 4, '5th Semester': 5, '6th Semester': 6, '7th Semester': 7, '8th Semester': 8}
        data['Semester'] = float(sem_map.get(semester, 0))

        if f"Faculty_{faculty}" in data.columns: data[f"Faculty_{faculty}"] = 1.0
        if f"Living_{living}" in data.columns: data[f"Living_{living}"] = 1.0
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
        data_scaled = pd.DataFrame(scaler.transform(data), columns=ALL_EXPECTED_FEATURES)
        data_reduced = pd.DataFrame(selector.transform(data_scaled), columns=selector.get_feature_names_out())
        prob = model.predict_proba(data_reduced)[:, 1][0]
        status = "High Risk" if prob >= 0.2392 else "Low Risk"

        # --- SESSION HANDOVER (FIXED Key: risk_score) ---
        st.session_state['last_student_id'] = student_id
        st.session_state['last_run_data'] = {
            'status': status,
            'risk_score': prob, # Matches AI Counselor key
            'details': data.to_dict('records')[0]
        }

        # --- 4. MAIN ASSESSMENT HEADER ---
        st.divider()
        res_col1, res_col2 = st.columns([1, 1])
        with res_col1:
            if status == "High Risk":
                st.error(f"### Assessment: {status}")
            else:
                st.success(f"### Assessment: {status}")
            st.metric("Risk Probability", f"{prob:.4f}")
        
        with res_col2:
            st.write("📊 **AI Model Confidence**")
            st.progress(min(float(prob), 1.0))

        # --- 5. DEEP XAI REPORT ---
        st.write("---")
        st.subheader("🔍 AI Decision Intelligence Report")
        
        st.markdown(f"""
            <div style="background-color: {'#ff4b4b11' if status == 'High Risk' else '#28a74511'}; 
                        padding: 20px; border-radius: 10px; border-left: 5px solid {'#ff4b4b' if status == 'High Risk' else '#28a745'};">
                <h4 style="margin:0; color: {'#ff4b4b' if status == 'High Risk' else '#28a745'};">Diagnostic Profile: {status}</h4>
                <p style="margin:10px 0 0 0; font-size: 0.95rem; color: #555; line-height: 1.5;">
                    The AI Ensemble has cross-referenced this student's unique 4-phase trajectory against historical data. 
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.write("") 

        cv = data.iloc[0]
        top_features = selector.get_feature_names_out()
        xai_col1, xai_col2 = st.columns(2)

        with xai_col1:
            st.markdown("#### 📉 Behavioral Dynamics & Trajectories")
            vol = cv.get('Motivation_Volatility', 0)
            if vol > 1.0:
                st.warning("**Unstable Engagement Analysis**")
                st.write(f"**Score:** `{vol:.2f}` | High volatility indicates reactive study drive.")
            else:
                st.success("**Stable Engagement Strategy**")
                st.write(f"**Score:** `{vol:.2f}` | Consistent drive matches the resilient profile.")

            acc = cv.get('Confidence_Acceleration', 0)
            if acc < -0.5:
                st.error("**Negative Confidence Acceleration**")
                st.write(f"**Rate:** `{acc:.2f}` | Critical 'Confidence Spiral' detected.")
            elif acc > 0.5:
                st.success("**Positive Momentum Detected**")
                st.write(f"**Rate:** `+{acc:.2f}` | Accelerating mastery trajectory.")
            else:
                st.info("**Stable Self-Assurance Baseline**")

        with xai_col2:
            st.markdown("#### 📚 Academic & Lifestyle Metrics")
            att = cv.get('Attendance_Percentage', 0)
            if att < 7:
                st.warning("**Sub-optimal Participation**")
                st.write(f"**Presence:** `{att}/10` | Falling below classroom integration threshold.")
            else:
                st.success("**High-Presence Anchor**")
                st.write(f"**Presence:** `{att}/10` | Participation levels within the safe cluster.")

            slp = cv.get('Sleep_Hours_Slope', 0)
            if slp < -0.2:
                st.error("**Sleep Depletion Trajectory**")
                st.write(f"**Trend:** `Negative Slope` | Strong correlation with biological exhaustion.")
            else:
                st.success("**Sustainable Biological Load**")

        # --- TECHNICAL ARCHITECTURE ---
        with st.expander("🛠️ View Committee Decision Matrix"):
            table_df = pd.DataFrame({
                "Diagnostic Feature": [n.replace("_", " ").title() for n in top_features],
                "Current Value": [f"{cv[n]:.2f}" for n in top_features]
            })
            st.table(table_df)

        save_prediction(student_id, float(prob), status, data.to_dict('records')[0])























# import streamlit as st
# import pandas as pd
# import joblib
# import os
# import numpy as np
# from database.app_db import save_prediction

# # --- ASSET PATHS ---
# MODEL_DIR = "models"
# MODEL_FILE = os.path.join(MODEL_DIR, 'final_ensemble_model.pkl')
# SELECTOR_FILE = os.path.join(MODEL_DIR, 'feature_selector.pkl')
# SCALER_FILE = os.path.join(MODEL_DIR, 'main_scaler.pkl')

# def run_risk_module():
#     st.markdown("## 🎓 Student Risk Intelligence Diagnostic")
    
#     if not os.path.exists(MODEL_FILE):
#         st.error("AI Model files missing. Please ensure /models/ contains your trained pkl files.")
#         return

#     # Load Research Brain
#     model = joblib.load(MODEL_FILE)
#     selector = joblib.load(SELECTOR_FILE)
#     scaler = joblib.load(SCALER_FILE)
#     ALL_EXPECTED_FEATURES = scaler.feature_names_in_

#     with st.form("comprehensive_diagnostic_form"):
#         tab1, tab2, tab3, tab4 = st.tabs(["👤 Profile", "📚 Academics", "📉 Phase Trends", "⚠️ Challenges"])

#         with tab1:
#             st.subheader("Demographics & Lifestyle")
#             c1, c2 = st.columns(2)
#             with c1:
#                 student_id = st.text_input("Student ID*", value="STU-001")
#                 age = st.number_input("Age", 17, 60, 21)
#                 gender = st.selectbox("Gender", ["Female", "Male"])
#                 faculty = st.selectbox("Faculty", ["Computing", "Engineering", "Business", "Humanities & Sciences", "Architecture", "Law", "Hospitality & Culinary"])
#             with c2:
#                 living = st.selectbox("Living Arrangement", ["With family", "Hostel", "Shared apartment", "Alone"])
#                 part_time = st.selectbox("Part-time Job", ["No", "Yes"])
#                 travel = st.selectbox("Daily Travel Time", ["0-15 minutes", "16-30 minutes", "31-60 minutes", "61-90 minutes", "More than 90 minutes"])
#                 family_support = st.select_slider("Family Support Level", options=[1, 2, 3, 4, 5], value=3)

#         with tab2:
#             st.subheader("Academic Engagement")
#             c1, c2 = st.columns(2)
#             with c1:
#                 cgpa = st.number_input("Current CGPA", 0.0, 4.0, 3.0)
#                 semester = st.selectbox("Semester", ["1st Semester", "2nd Semester", "3rd Semester", "4th Semester", "5th Semester", "6th Semester", "7th Semester", "8th Semester"])
#                 failed_subs = st.selectbox("Failed Subjects", ["0", "1", "2", "3", "4", "5 or more"])
#                 attendance = st.slider("Average Attendance (0-10 scale)", 0, 10, 8)
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
#             st.write("Identify current barriers:")
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
#         data['Age'] = float(age); data['CGPA'] = float(cgpa); data['Attendance_Percentage'] = float(attendance)
#         data['Failed_Subjects'] = 5.0 if failed_subs == "5 or more" else float(failed_subs)
#         data['Lecture_Participation'] = float(lecture_part); data['Lab_Participation'] = float(lab_part)
#         data['Family_Support'] = float(family_support)
#         data['Gender'] = 1.0 if gender == "Female" else 0.0
#         data['Part_Time_Job'] = 1.0 if part_time == "Yes" else 0.0
#         data['Considered_Dropout'] = 1.0 if dropout_cons == "Yes" else 0.0

#         sem_map = {'1st Semester': 1, '2nd Semester': 2, '3rd Semester': 3, '4th Semester': 4, '5th Semester': 5, '6th Semester': 6, '7th Semester': 7, '8th Semester': 8}
#         data['Semester'] = float(sem_map.get(semester, 0))

#         if f"Faculty_{faculty}" in data.columns: data[f"Faculty_{faculty}"] = 1.0
#         if f"Living_{living}" in data.columns: data[f"Living_{living}"] = 1.0
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
#         data_scaled = pd.DataFrame(scaler.transform(data), columns=ALL_EXPECTED_FEATURES)
#         data_reduced = pd.DataFrame(selector.transform(data_scaled), columns=selector.get_feature_names_out())
#         prob = model.predict_proba(data_reduced)[:, 1][0]
#         status = "High Risk" if prob >= 0.2392 else "Low Risk"

#         # --- 4. MAIN ASSESSMENT HEADER ---
#         st.divider()
#         res_col1, res_col2 = st.columns([1, 1])
#         with res_col1:
#             if status == "High Risk":
#                 st.error(f"### Assessment: {status}")
#             else:
#                 st.success(f"### Assessment: {status}")
#             st.metric("Risk Probability", f"{prob:.4f}")
        
#         with res_col2:
#             st.write("📊 **AI Model Confidence**")
#             st.progress(min(float(prob), 1.0))
#             st.caption("Target Threshold: 0.2392 (F2-Optimized)")

#         # --- 5. ENHANCED AI DECISION INTELLIGENCE REPORT ---
#         st.write("---")
#         st.subheader("🔍 AI Decision Intelligence Report")
        
#         # summary banner
#         st.markdown(f"""
#             <div style="background-color: {'#ff4b4b11' if status == 'High Risk' else '#28a74511'}; 
#                         padding: 20px; border-radius: 10px; border-left: 5px solid {'#ff4b4b' if status == 'High Risk' else '#28a745'};">
#                 <h4 style="margin:0; color: {'#ff4b4b' if status == 'High Risk' else '#28a745'};">Diagnostic Profile: {status}</h4>
#                 <p style="margin:10px 0 0 0; font-size: 0.95rem; color: #555; line-height: 1.5;">
#                     The AI Ensemble has cross-referenced this student's unique 4-phase trajectory against historical data. 
#                     This prediction is primarily driven by how the student's internal behavior (Motivation/Confidence) 
#                     interacts with external academic pressures.
#                 </p>
#             </div>
#         """, unsafe_allow_html=True)

#         st.write("") 

#         cv = data.iloc[0]
#         top_features = selector.get_feature_names_out()
#         xai_col1, xai_col2 = st.columns(2)

#         with xai_col1:
#             st.markdown("#### 📉 Behavioral Dynamics & Trajectories")
            
#             # --- MOTIVATION VOLATILITY ---
#             vol = cv.get('Motivation_Volatility', 0)
#             if vol > 1.0:
#                 st.warning(f"**Unstable Engagement Analysis**")
#                 st.write(f"**Volatility Score:** `{vol:.2f}` | **Threshold Alert**")
#                 st.write("""
#                     High 'Motivation Volatility' suggests the student's drive is reactive rather than resilient. 
#                     Drastic swings in engagement across the semester are a signature of students who 
#                     eventually disengage when workload peaks.
#                 """)
#             else:
#                 st.success(f"**Stable Engagement Strategy**")
#                 st.write(f"**Volatility Score:** `{vol:.2f}` | **Consistent Profile**")
#                 st.write("""
#                     This stability matches the 'Resilient' student profile. Maintaining consistent motivation 
#                     from the baseline (Phase 1) through to the finals (Phase 4) indicates a strong internal 
#                     discipline and lower probability of burnout.
#                 """)

#             # --- CONFIDENCE ACCELERATION ---
#             acc = cv.get('Confidence_Acceleration', 0)
#             if acc < -0.5:
#                 st.error(f"**Negative Confidence Acceleration**")
#                 st.write(f"**Rate:** `{acc:.2f}` | **Critical Spiral**")
#                 st.write("""
#                     The model detected a 'Confidence Spiral'. This means self-belief is not just declining, 
#                     but the *rate* of decline is speeding up as the semester ends. This mathematical pattern 
#                     is a high-impact early warning for silent dropout decisions.
#                 """)
#             elif acc > 0.5:
#                 st.success(f"**Positive Momentum Detected**")
#                 st.write(f"**Rate:** `+{acc:.2f}` | **Growth Phase**")
#                 st.write("""
#                     The student is in a 'Growth Trajectory'. Accelerating confidence suggests a mastery of 
#                     course materials and positive social integration, which acts as a powerful buffer 
#                     against academic risk.
#                 """)
#             else:
#                 st.info(f"**Stable Self-Assurance Baseline**")
#                 st.write(f"**Rate:** `{acc:.2f}` | **Plateau**")
#                 st.write("""
#                     Confidence levels are holding steady. While we don't see accelerating growth, the 
#                     absence of a downward spiral suggests the student currently possesses the emotional 
#                     stamina required for the remaining semester phases.
#                 """)

#         with xai_col2:
#             st.markdown("#### 📚 Academic & Lifestyle Metrics")
            
#             # --- ATTENDANCE ---
#             att = cv.get('Attendance_Percentage', 0)
#             if att < 7:
#                 st.warning(f"**Sub-optimal Participation**")
#                 st.write(f"**Physical Presence:** `{att}/10` | **Risk Factor**")
#                 st.write("""
#                     Attendance is a primary 'Anchor' for success. Scores below 7/10 indicate a breakdown in 
#                     classroom integration. The AI weights this heavily because missing conceptual lectures 
#                     in Phase 2 often leads to failure in Phase 4.
#                 """)
#             else:
#                 st.success(f"**High-Presence Anchor**")
#                 st.write(f"**Physical Presence:** `{att}/10` | **Safe Cluster**")
#                 st.write("""
#                     A score of 8 or higher places the student in the 'Safe Participation' cluster. Consistent 
#                     presence ensures the student receives immediate academic feedback and remains socially 
#                     tethered to the learning environment.
#                 """)

#             # --- SLEEP SLOPE ---
#             slp = cv.get('Sleep_Hours_Slope', 0)
#             if slp < -0.2:
#                 st.error(f"**Sleep Depletion Trajectory**")
#                 st.write(f"**Trend:** `Negative Slope` | **Biological Risk**")
#                 st.write("""
#                     We detected 'Linear Exhaustion'. Trading sleep for study hours as the semester progresses 
#                     creates a negative biological load. Statistically, students with this trajectory show a 
#                     spike in mental stress scores during the final phase.
#                 """)
#             else:
#                 st.success(f"**Sustainable Biological Load**")
#                 st.write(f"**Trend:** `Stable/Positive` | **Protected**")
#                 st.write("""
#                     The student is maintaining healthy rest patterns despite academic pressure. By preserving 
#                     sleep quality in the final phases, they maintain the cognitive cognitive functioning 
#                     necessary for complex problem solving.
#                 """)

#         # --- TECHNICAL ARCHITECTURE ---
#         with st.expander("🛠️ View Committee Decision Matrix (Mathematical Weights)"):
#             st.write("Technical breakdown of the Top 15 variables used by the Voting Ensemble (SVM, KNN, Extra Trees).")
#             # Image tag for instruction purposes
            
            
#             table_df = pd.DataFrame({
#                 "Diagnostic Feature": [n.replace("_", " ").title() for n in top_features],
#                 "Current Value": [f"{cv[n]:.2f}" for n in top_features]
#             })
#             st.table(table_df)

#         save_prediction(student_id, float(prob), status, data.to_dict('records')[0])




