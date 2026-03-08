import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import logging
import urllib.parse  
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score

# Ensure root directory is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.auth import create_admin_if_missing, verify_login
from src.data_contract import validate_dataset
from src.preprocessing import preprocess
from src.features import add_phase_features, get_model_features
from src.clustering import train_kmeans, predict, run_anova
from src.profiling import cluster_summary, assign_profile_names
from src.xai import cluster_drivers
from src.reports import individual_row

# ===============================
# 1. SYSTEM CONFIGURATION & LOGGING
# ===============================
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/system_operations.log", level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

st.set_page_config(page_title="Student Success Platform", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# ===============================
# 2. PREMIUM ENTERPRISE CSS
# ===============================
st.markdown("""
<style>
    /* Modern Typography & Spacing */
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; font-family: 'Inter', sans-serif; }
    
    /* Gradient Metric Cards */
    [data-testid="stMetric"] { 
        background: linear-gradient(145deg, var(--secondary-background-color), rgba(128,128,128,0.05)); 
        border: 1px solid rgba(128, 128, 128, 0.2); 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); 
        text-align: center; 
        transition: transform 0.2s ease, box-shadow 0.2s ease; 
        border-top: 4px solid #38BDF8; 
    }
    [data-testid="stMetric"]:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); }
    [data-testid="stMetricLabel"] { font-size: 13px; font-weight: 600; opacity: 0.7; text-transform: uppercase; letter-spacing: 0.8px; }
    [data-testid="stMetricValue"] { font-size: 32px; font-weight: 800; }
    
    /* Premium Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 40px; border-bottom: 1px solid rgba(128, 128, 128, 0.2); padding-bottom: 5px; }
    .stTabs [data-baseweb="tab"] { height: 50px; font-weight: 600; font-size: 15px; opacity: 0.5; transition: opacity 0.3s ease; }
    .stTabs [data-baseweb="tab"]:hover { opacity: 1; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { opacity: 1; border-bottom-color: #38BDF8 !important; border-bottom-width: 3px !important; }
    
    /* Sleek Information Boxes */
    .admin-guide { background-color: rgba(56, 189, 248, 0.05); padding: 18px; border-left: 4px solid #38BDF8; border-radius: 6px; margin-bottom: 24px; font-size: 14px; line-height: 1.6; }
    .mentor-card { background: rgba(16, 185, 129, 0.05); border-left: 4px solid #10B981; padding: 16px; border-radius: 8px; margin-bottom: 12px; border-top: 1px solid rgba(128,128,128,0.1); border-right: 1px solid rgba(128,128,128,0.1); border-bottom: 1px solid rgba(128,128,128,0.1); transition: transform 0.2s; }
    .mentor-card:hover { transform: translateX(5px); }
    
    /* Action Checklist Items */
    .action-item { padding: 14px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #EF4444; background: rgba(239, 68, 68, 0.05); font-weight: 500; font-size: 14px;}
    .action-item-warning { border-left-color: #F59E0B; background: rgba(245, 158, 11, 0.05); }
    .action-item-ok { border-left-color: #10B981; background: rgba(16, 185, 129, 0.05); }
</style>
""", unsafe_allow_html=True)

color_map = {
    "High Performing & Motivated": "#10B981", 
    "Average / Moderate Students": "#3B82F6", 
    "At-Risk Students": "#EF4444"             
}

# ===============================
# 3. SECURE AUTHENTICATION
# ===============================
create_admin_if_missing("admin", "admin123")
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-weight: 800;'>🎓 Institutional AI Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; opacity: 0.7; font-size: 18px;'>Secure Enterprise Analytics Login</p>", unsafe_allow_html=True)
        st.write("")
        with st.container(border=True):
            u = st.text_input("Administrator ID", placeholder="Enter your ID")
            p = st.text_input("Secure Password", type="password", placeholder="Enter your password")
            st.write("")
            if st.button("Authenticate Session", use_container_width=True, type="primary"):
                if verify_login(u, p):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Authentication Denied. Invalid credentials.")
    st.stop()

with st.sidebar:
    st.title("⚙️ System Controls")
    st.success("🟢 Security: Offline Core Active")
    st.markdown("---")
    st.caption("Logged in as System Administrator")
    if st.button("Secure Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.markdown("<h1 style='font-weight: 800; letter-spacing: -1px;'>🎓 Executive Student Intelligence Platform</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px; opacity: 0.8;'>Automated Behavioral Segmentation & Predictive Trajectory Analytics</p>", unsafe_allow_html=True)
st.write("")

# ===============================
# 4. EXECUTIVE NAVIGATION
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 01 Integration", 
    "📊 02 Macro Overview", 
    "🧠 03 Micro Advising", 
    "📋 04 Bulk Outreach"
])

# ---------------------------------------------------------
# TAB 1: DATA INGESTION
# ---------------------------------------------------------
with tab1:
    st.markdown("""<div class='admin-guide'><b>System Moderator Guide:</b> Upload the pre-exam survey CSV below. The AI pipeline will automatically clean the data, validate schemas, engineer temporal features, and cluster the cohorts.</div>""", unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("1. Secure Data Upload")
        uploaded = st.file_uploader("Select Pre-Exam Survey File", type=["csv"], label_visibility="collapsed")
    
    if uploaded:
        os.makedirs("data/semester_uploads", exist_ok=True)
        save_path = os.path.join("data/semester_uploads", uploaded.name)
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())

        try:
            df_raw = pd.read_csv(save_path)
            missing, df_raw = validate_dataset(df_raw)
            
            if missing:
                st.error(f"Validation Failed: Missing required architecture columns: {missing}")
            else:
                with st.container(border=True):
                    st.subheader("2. Data Schema Validation")
                    c_rows, c_cols = st.columns(2)
                    c_rows.metric("Total Student Records", f"{len(df_raw):,}")
                    c_cols.metric("Total Features Detected", f"{len(df_raw.columns)}")
                    
                    with st.expander("🔎 Preview Raw Uploaded Data"):
                        st.dataframe(df_raw.head(), use_container_width=True)
                
                st.write("")
                if st.button("🚀 Initialize AI Processing Pipeline", type="primary", use_container_width=True):
                    with st.spinner("Compiling statistical behavioral models & calculating multidimensional trajectories..."):
                        df_clean, _ = preprocess(df_raw)
                        df_feat = add_phase_features(df_clean)
                        
                        if 'Challenges' in df_raw.columns: df_feat['Challenges'] = df_raw['Challenges']
                        
                        for phase in range(1, 5):
                            mot_col = f"Motivation_Phase{phase}"
                            str_col = f"Stress_Phase{phase}"
                            if mot_col in df_raw.columns: df_feat[mot_col] = pd.to_numeric(df_raw[mot_col], errors='coerce').fillna(0)
                            if str_col in df_raw.columns: df_feat[str_col] = pd.to_numeric(df_raw[str_col], errors='coerce').fillna(0)
                            
                        features = get_model_features(df_feat)
                        meta = train_kmeans(df_feat, features, k=3)
                        labels = predict(df_feat)
                        df_feat["cluster"] = labels
                        
                        if "student_id" in df_feat.columns:
                            df_feat["Institutional_Email"] = df_feat["student_id"].astype(str).str.lower() + "@my.sliit.lk"
                        
                        X = df_feat[features].fillna(0)
                        meta['silhouette'] = silhouette_score(X, labels)
                        meta['calinski'] = calinski_harabasz_score(X, labels)
                        sig_count = run_anova(df_feat, features, "cluster")
                        meta["significant_features"] = f"{sig_count} / {len(features)}"
                        
                        st.session_state["meta"] = meta
                        st.session_state["df_feat"] = df_feat
                        st.session_state["features"] = features
                        
                    st.toast("Intelligence Pipeline Execution Successful!", icon="✅")
                    st.success("Mathematical Pipeline Complete. Please navigate to the Macro Overview tab.")
        except Exception as e:
            st.error(f"⚠️ A critical framework error occurred. Technical Details: {str(e)}")

if "df_feat" not in st.session_state:
    st.info("👋 **System Offline.** Please upload your pre-exam semester dataset in **01 Integration** to unlock the platform features.")
    st.stop()

df_feat = st.session_state["df_feat"]
features = st.session_state["features"]
meta = st.session_state.get("meta", {}) 

summary = cluster_summary(df_feat, features, "cluster")
profiles = assign_profile_names(summary)
df_feat["Profile"] = df_feat["cluster"].map(lambda x: profiles[x]["Profile"])

# ---------------------------------------------------------
# TAB 2: INSTITUTIONAL OVERVIEW
# ---------------------------------------------------------
with tab2:
    st.markdown("### System Health & Topography")
    
    with st.container(border=True):
        sil_score = meta.get('silhouette', 0.0)
        cal_score = meta.get('calinski', 0.0)
        sig_feats = meta.get('significant_features', "0 / 0")

        c1, c2, c3 = st.columns(3)
        c1.metric("Cluster Cohesion (Silhouette)", f"{sil_score:.4f}", help="Measures boundary separation.")
        c2.metric("Cluster Density (Calinski)", f"{cal_score:.2f}", help="Measures variance ratio.")
        c3.metric("Key Predictive Variables", sig_feats, help="Number of parameters with ANOVA p < 0.05.")
    
    st.write("")
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        with st.container(border=True):
            st.markdown("#### Cohort Distribution")
            dist = df_feat["Profile"].value_counts().reset_index()
            dist.columns = ["Profile", "Students"]
            fig_donut = px.pie(dist, values="Students", names="Profile", hole=0.65, color="Profile", color_discrete_map=color_map)
            fig_donut.update_traces(textinfo='percent+value')
            fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5), margin=dict(t=10, b=0, l=0, r=0))
            st.plotly_chart(fig_donut, use_container_width=True, theme="streamlit")
        
    with col_b:
        with st.container(border=True):
            st.markdown("#### Root Cause Analytics (NLP)")
            st.caption("Algorithmic extraction of qualitative text anomalies for High-Risk cohorts.")
            risk_df = df_feat[df_feat["Profile"].str.contains("Risk")]
            if "Challenges" in risk_df.columns and not risk_df["Challenges"].dropna().empty:
                challenges = risk_df["Challenges"].dropna().str.replace('"', '').str.split(",").explode().str.strip()
                top_challenges = challenges.value_counts().head(5).reset_index()
                top_challenges.columns = ["Reported Challenge", "Frequency"]
                fig_bar = px.bar(top_challenges, x="Frequency", y="Reported Challenge", orientation='h', color_discrete_sequence=["#EF4444"])
                fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=10, b=0, l=0, r=0))
                st.plotly_chart(fig_bar, use_container_width=True, theme="streamlit")

    with st.container(border=True):
        st.markdown("#### Departmental Risk Topography")
        if "Faculty" in df_feat.columns:
            heat_df = pd.crosstab(df_feat['Faculty'], df_feat['Profile'], normalize='index') * 100
            fig_heat = px.imshow(heat_df, text_auto=".1f", aspect="auto", color_continuous_scale="Reds", title="Percentage of Risk per Faculty")
            fig_heat.update_layout(margin=dict(t=30, b=0, l=0, r=0), coloraxis_showscale=False)
            st.plotly_chart(fig_heat, use_container_width=True, theme="streamlit")

# ---------------------------------------------------------
# TAB 3: 1-ON-1 ADVISING ENGINE
# ---------------------------------------------------------
with tab3:
    st.markdown("### 🔍 Advanced Diagnostic Suite")
    st.markdown("""<div class='admin-guide'><b>Moderator Guide:</b> Input a Student ID below to instantly generate their personalized Risk Gauge, XAI Radar, and Time-Series Forecast before their counseling session.</div>""", unsafe_allow_html=True)
    
    with st.container(border=True):
        sid = st.selectbox("Search Student ID for Deep Scan", df_feat["student_id"].unique())
        row = df_feat[df_feat["student_id"] == sid].iloc[0]
        cid = int(row["cluster"])
        
        # Mathematical Risk Severity Index (0-100%)
        stress = float(row.get('Stress_Mean', 3))
        cgpa = float(row.get('CGPA', 2.0))
        att = float(row.get('Attendance_Percentage', 50))
        risk_score = min(100, max(0, ((stress / 5) * 35) + (((4.0 - cgpa) / 4.0) * 40) + (((100 - att) / 100) * 25)))
        
        if "Risk" in profiles[cid]['Profile']: st.error(f"**Classification:** {profiles[cid]['Profile']} | **Failure Probability:** {risk_score:.0f}%")
        elif "Average" in profiles[cid]['Profile']: st.warning(f"**Classification:** {profiles[cid]['Profile']} | **Failure Probability:** {risk_score:.0f}%")
        else: st.success(f"**Classification:** {profiles[cid]['Profile']} | **Failure Probability:** {risk_score:.0f}%")
    
    t_diag, t_ts, t_mentor, t_sim = st.tabs(["📊 Diagnostics & Action", "🔮 Exam Forecast", "🤝 Mentor Matcher", "🎛️ AI Simulator"])
    
    # --- 1. Diagnostic XAI & Action Plan ---
    with t_diag:
        with st.container(border=True):
            r1, r2, r3 = st.columns([1, 1.2, 1])
            with r1:
                st.markdown("##### 🧮 Failure Index")
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number", value = risk_score, number={'suffix': "%"},
                    gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "white"},
                             'steps': [{'range': [0, 35], 'color': "#10B981"}, {'range': [35, 65], 'color': "#F59E0B"}, {'range': [65, 100], 'color': "#EF4444"}]}
                ))
                fig_gauge.update_layout(margin=dict(t=20, b=10, l=10, r=10), height=200)
                st.plotly_chart(fig_gauge, use_container_width=True, theme="streamlit")
                
            with r2:
                st.markdown("##### 📊 Metric Variance")
                xai_cols = st.columns(2)
                metrics_to_show = ["Stress_Mean", "Motivation_Mean", "CGPA", "Attendance_Percentage"]
                for i, m in enumerate(metrics_to_show):
                    if m in df_feat.columns:
                        val = row[m]
                        avg = df_feat[m].mean()
                        inv = "inverse" if "Stress" in m or "Failed" in m else "normal"
                        fmt = f"{val:.0f}%" if "Percentage" in m else f"{val:.2f}"
                        d_fmt = f"{val-avg:.0f}%" if "Percentage" in m else f"{val-avg:.2f}"
                        xai_cols[i % 2].metric(label=m.replace("_Mean", "").replace("_Percentage", ""), value=fmt, delta=f"{d_fmt} vs Baseline", delta_color=inv)

            with r3:
                st.markdown("##### ✅ Priority Action Plan")
                st.caption("AI-generated intervention checklist:")
                if row.get('Stress_Mean', 0) > df_feat['Stress_Mean'].mean():
                    st.markdown("<div class='action-item'>🚨 Immediate Wellness Referral</div>", unsafe_allow_html=True)
                if row.get('Attendance_Percentage', 100) < 75:
                    st.markdown("<div class='action-item'>🚨 Issue Attendance Warning</div>", unsafe_allow_html=True)
                if row.get('CGPA', 4.0) < 3.0:
                    st.markdown("<div class='action-item action-item-warning'>⚠️ Enroll in Peer Tutoring</div>", unsafe_allow_html=True)
                st.markdown("<div class='action-item action-item-ok'>✅ Schedule Follow-Up</div>", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("##### Multidimensional Behavioral Geometry")
            st.caption("Visualizing the student against the Institutional Average and the Top 10% 'Gold Standard' benchmark.")
            radar_features = [f for f in ["Motivation_Mean", "Stress_Mean", "Confidence_Mean", "Social_Mean", "Workload_Mean"] if f in features]
            if radar_features:
                gold_standard = df_feat[df_feat['Profile'] == 'High Performing & Motivated'][radar_features].mean()
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(r=[row[f] for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features], fill='toself', name=f'Student {sid}', line_color="#3B82F6"))
                fig_radar.add_trace(go.Scatterpolar(r=gold_standard.tolist(), theta=[f.replace("_Mean","") for f in radar_features], fill='toself', name='Gold Standard', line_color="#F59E0B", opacity=0.6))
                fig_radar.add_trace(go.Scatterpolar(r=[df_feat[f].mean() for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features], fill='toself', name='Average', line_color="#000000", opacity=0.2))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
                st.plotly_chart(fig_radar, use_container_width=True, theme="streamlit")
    
    # --- 2. Predictive Burnout Tracker ---
    with t_ts:
        with st.container(border=True):
            st.markdown("##### 🔮 Pre-Exam Trajectory (Polynomial Regression)")
            st.write("Utilizes historical Phase 1-4 data to mathematically forecast where the student's psychology will be during Final Exams.")
            phases = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4']
            try:
                mot_vals = [float(row.get(f'Motivation_Phase{i}', 0)) for i in range(1, 5)]
                str_vals = [float(row.get(f'Stress_Phase{i}', 0)) for i in range(1, 5)]
                x = np.array([1, 2, 3, 4])
                p_mot = np.poly1d(np.polyfit(x, mot_vals, 1))
                p_str = np.poly1d(np.polyfit(x, str_vals, 1))
                forecast_mot, forecast_str = min(5, max(0, p_mot(5))), min(5, max(0, p_str(5)))
                
                fig_ts = go.Figure()
                fig_ts.add_trace(go.Scatter(x=phases, y=mot_vals, mode='lines+markers', name='Motivation', line=dict(color='#10B981', width=3), marker=dict(size=10)))
                fig_ts.add_trace(go.Scatter(x=phases, y=str_vals, mode='lines+markers', name='Stress', line=dict(color='#EF4444', width=3), marker=dict(size=10)))
                fig_ts.add_trace(go.Scatter(x=['Phase 4', 'Exam Forecast'], y=[mot_vals[-1], forecast_mot], mode='lines+markers', line=dict(color='#10B981', width=3, dash='dash'), name='Predicted Motivation'))
                fig_ts.add_trace(go.Scatter(x=['Phase 4', 'Exam Forecast'], y=[str_vals[-1], forecast_str], mode='lines+markers', line=dict(color='#EF4444', width=3, dash='dash'), name='Predicted Stress'))
                fig_ts.update_layout(yaxis=dict(range=[0, 5], title="Score (1-5)"), margin=dict(t=30, b=20, l=20, r=20), hovermode="x unified")
                st.plotly_chart(fig_ts, use_container_width=True, theme="streamlit")
            except Exception as e:
                st.info("Insufficient Phase data to render the Predictive Time-Series.")

    # --- 3. Peer Mentor Matcher ---
    with t_mentor:
        with st.container(border=True):
            st.markdown("##### 🤝 Peer Recommendation Engine")
            st.write(f"Automatically queries the **{row.get('Faculty', 'University')}** faculty to identify the top 3 'High Performing' peers to act as mentors.")
            if row['Profile'] == "High Performing & Motivated":
                st.success("🌟 This student is currently classified as High Performing. They are eligible to be a Peer Mentor for others!")
            else:
                student_faculty = row.get("Faculty", None)
                mentor_pool = df_feat[(df_feat['Profile'] == "High Performing & Motivated") & (df_feat['Faculty'] == student_faculty)]
                if not mentor_pool.empty:
                    top_mentors = mentor_pool.sort_values(by=['CGPA', 'Motivation_Mean'], ascending=[False, False]).head(3)
                    for index, mentor_row in top_mentors.iterrows():
                        st.markdown(f"""
                        <div class="mentor-card">
                            <b style="color: #38BDF8; font-size: 18px;">Highest Match: {mentor_row['student_id']}</b><br>
                            <span style="opacity: 0.9;"><b>CGPA:</b> {mentor_row['CGPA']:.2f} | <b>Motivation:</b> {mentor_row.get('Motivation_Mean', 5):.1f}/5 | <b>Workload:</b> {mentor_row.get('Workload_Mean', 3):.1f}/5</span>
                            <br><span style="font-size: 14px; color: #94A3B8;">Contact: {mentor_row.get('Institutional_Email', 'N/A')}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(f"No available High Performing mentors found in the {student_faculty} department.")

    # --- 4. What-If Simulator ---
    with t_sim:
        with st.container(border=True):
            st.markdown("##### 🎛️ Intervention Sandbox")
            st.write("Use the interactive sliders to mathematically prove how modifying behaviors reshapes the student's profile.")
            sim_cols = st.columns([1, 1.5])
            with sim_cols[0]:
                st.write("")
                sim_stress = st.slider("Simulate Counseling (Reduce Stress)", 1.0, 5.0, float(row.get("Stress_Mean", 3.0)), 0.1)
                sim_mot = st.slider("Simulate Mentoring (Increase Motivation)", 1.0, 5.0, float(row.get("Motivation_Mean", 3.0)), 0.1)
                sim_work = st.slider("Simulate Timetabling (Adjust Workload)", 1.0, 5.0, float(row.get("Workload_Mean", 3.0)), 0.1)
            with sim_cols[1]:
                if radar_features:
                    sim_radar = go.Figure()
                    sim_radar.add_trace(go.Scatterpolar(r=[row[f] for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features], fill='toself', name='Current State', line_color="#EF4444", opacity=0.3))
                    sim_vals = [sim_stress if f == "Stress_Mean" else sim_mot if f == "Motivation_Mean" else sim_work if f == "Workload_Mean" else row[f] for f in radar_features]
                    sim_radar.add_trace(go.Scatterpolar(r=sim_vals, theta=[f.replace("_Mean","") for f in radar_features], fill='toself', name='Simulated Target', line_color="#10B981"))
                    sim_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), margin=dict(t=20, b=20, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
                    st.plotly_chart(sim_radar, use_container_width=True, theme="streamlit")

# ---------------------------------------------------------
# TAB 4: BULK ACTION & REPORTING
# ---------------------------------------------------------
with tab4:
    st.markdown("### 📥 Mass Outreach & Roster Generation")
    st.markdown("""<div class='admin-guide'><b>Moderator Guide:</b> Filter specific cohorts to instantly generate bulk email communication and downloadable pre-exam intervention rosters.</div>""", unsafe_allow_html=True)
    
    with st.container(border=True):
        if "Faculty" in df_feat.columns and "Semester" in df_feat.columns:
            e1, e2, e3 = st.columns(3)
            with e1: sel_fac = st.selectbox("Department Filter", sorted(df_feat["Faculty"].unique()))
            with e2: sel_sem = st.selectbox("Academic Term Filter", sorted(df_feat["Semester"].unique()))
            with e3: sel_prof = st.selectbox("Cohort Segment Filter", sorted(df_feat["Profile"].unique()), index=len(df_feat["Profile"].unique())-1)

            filtered = df_feat[(df_feat["Faculty"] == sel_fac) & (df_feat["Semester"] == sel_sem) & (df_feat["Profile"] == sel_prof)]
            
            st.write("")
            st.info(f"🔍 Pipeline retrieved **{len(filtered)}** high-priority student records matching institutional query parameters.")
            st.dataframe(filtered, use_container_width=True)
            
            st.markdown("---")
            st.markdown("#### ✉️ Automated Bulk Communication Engine")
            
            if not filtered.empty and "Institutional_Email" in filtered.columns:
                email_list = ",".join(filtered["Institutional_Email"].tolist())
                subject = f"URGENT: Pre-Exam Support & Check-in for {sel_fac} Students"
                body = f"""Dear Student,

I am reaching out from the {sel_fac} Academic Advising Department. As we approach the final exam period, our system has flagged that you may benefit from additional academic resources to ensure you finish the semester strong.

We have immediate support systems available, including rapid academic peer-tutoring and wellness counseling to help manage exam stress and workload. We highly encourage you to schedule a brief 10-minute check-in with our office this week.

Please reply directly to this email to secure a time slot. We are here to help you succeed.

Best regards,
Department of Academic Advising"""

                encoded_subject = urllib.parse.quote(subject)
                encoded_body = urllib.parse.quote(body)
                mailto_link = f"mailto:?bcc={email_list}&subject={encoded_subject}&body={encoded_body}"
                
                col_email1, col_email2 = st.columns([1, 1])
                with col_email1:
                    st.write("###### Priority: 1-Click Secure Mailing")
                    st.write("Click below to securely open your native mail client. All identified students are automatically BCC'd to protect privacy.")
                    st.write("")
                    st.link_button("🚀 Execute Bulk Email Campaign", mailto_link, type="primary", use_container_width=True)
                
                with col_email2:
                    st.write("###### Fallback: Webmail Execution")
                    st.write("If using a web-based mail client, copy this encoded string to your BCC line:")
                    st.code(email_list.replace(",", "; "), language="text")
                    
                st.text_area("Review System-Generated Template:", value=body, height=220)
            else:
                st.warning("No students found in this specific segment to generate an outreach campaign.")
            
            st.write("")
            st.download_button("⬇️ Download Secure Action List (CSV)", filtered.to_csv(index=False).encode("utf-8"), file_name=f"Intervention_Roster_{sel_fac}_{sel_prof}.csv", mime="text/csv", type="primary", use_container_width=True)
        else:
            st.download_button("⬇️ Export Master System Database", df_feat.to_csv(index=False).encode("utf-8"), file_name=f"Master_Database.csv", mime="text/csv", type="primary", use_container_width=True)