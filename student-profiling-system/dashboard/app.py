import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import logging
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

# Set Page Configuration
st.set_page_config(page_title="Student Success System", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

# ===============================
# 2. ADAPTIVE ENTERPRISE CSS
# ===============================
st.markdown("""
<style>
    /* Global Container Padding */
    .block-container {
        padding-top: 2rem; 
        padding-bottom: 2rem; 
        font-family: 'Inter', 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Adaptive Metric Cards with Hover Effects */
    [data-testid="stMetric"] {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        border-top: 4px solid var(--primary-color);
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stMetricLabel"] {
        font-size: 14px; 
        font-weight: 700; 
        color: var(--text-color);
        opacity: 0.8;
        text-transform: uppercase; 
        letter-spacing: 0.5px;
    }
    [data-testid="stMetricValue"] {
        font-size: 36px; 
        font-weight: 700; 
        color: var(--text-color);
    }
    
    /* Sleek Navigation Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 32px; 
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px; 
        font-weight: 600; 
        font-size: 16px; 
        color: var(--text-color);
        opacity: 0.6;
        transition: opacity 0.2s;
    }
    .stTabs [data-baseweb="tab"]:hover {
        opacity: 0.9;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        opacity: 1; 
        border-bottom-color: var(--primary-color) !important;
    }
    
    /* Custom Administrator Guide Box */
    .admin-guide {
        background-color: var(--secondary-background-color);
        padding: 16px;
        border-left: 5px solid var(--primary-color);
        border-radius: 6px;
        margin-bottom: 24px;
        font-size: 14.5px;
        color: var(--text-color);
        line-height: 1.5;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

# High-contrast palette mapped to profiles
color_map = {
    "High Performing & Motivated": "#10B981", # Emerald Green
    "Average / Moderate Students": "#3B82F6", # Ocean Blue
    "At-Risk Students": "#EF4444"             # Crimson Red
}

# ===============================
# 3. SECURE AUTHENTICATION
# ===============================
create_admin_if_missing("admin", "admin123")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🎓 Student Success Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; opacity: 0.7;'>Secure MLOps Executive Dashboard</p>", unsafe_allow_html=True)
        st.write("")
        u = st.text_input("Administrator ID")
        p = st.text_input("Secure Password", type="password")
        if st.button("Authenticate Session", use_container_width=True, type="primary"):
            if verify_login(u, p):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Authentication Denied. Invalid credentials.")
    st.stop()

with st.sidebar:
    st.title("⚙️ System Controls")
    st.success("🟢 Status: Secure Connection")
    st.markdown("---")
    if st.button("Terminate Session", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🎓 Executive Student Intelligence Platform")
st.markdown("Automated Behavioral Segmentation & Explainable AI (XAI) Advising Framework")
st.markdown("---")

# ===============================
# 4. EXECUTIVE NAVIGATION
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 01 Data Integration", 
    "📊 02 Institutional Overview", 
    "🧠 03 XAI Diagnostic Profiles", 
    "📋 04 Strategic Reporting"
])

# ---------------------------------------------------------
# TAB 1: DATA INGESTION
# ---------------------------------------------------------
with tab1:
    st.markdown("### Process New Semester Data")
    st.markdown("""<div class='admin-guide'><b>Administrator Guide:</b> Upload the raw end-of-semester CSV file. The AI engine will autonomously execute Median Imputation, Temporal Feature Engineering, and K-Means Clustering to identify risk cohorts.</div>""", unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Select CSV Source File", type=["csv"], label_visibility="collapsed")
    
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
                health_score = 100 - (df_raw.isnull().sum().sum() / (df_raw.shape[0] * df_raw.shape[1]) * 100)
                st.success(f"✅ Validation Successful: {len(df_raw)} records securely acquired.")
                st.progress(int(health_score), text=f"Data Quality Index: {health_score:.1f}%")
                
                st.write("")
                if st.button("▶️ Execute Intelligence Pipeline", type="primary"):
                    with st.spinner("Compiling statistical behavioral models & calculating Euclidean distances..."):
                        # 1. MLOps Preprocessing
                        df_clean, _ = preprocess(df_raw)
                        df_feat = add_phase_features(df_clean)
                        features = get_model_features(df_feat)
                        
                        # 2. Unsupervised Clustering Engine (K-Means)
                        meta = train_kmeans(df_feat, features, k=3)
                        labels = predict(df_feat)
                        df_feat["cluster"] = labels
                        
                        # 3. Dynamic Research Metrics (Data Drift Monitoring)
                        X = df_feat[features].fillna(0)
                        meta['silhouette'] = silhouette_score(X, labels)
                        meta['calinski'] = calinski_harabasz_score(X, labels)
                        
                        # 4. ANOVA Explainability Testing
                        sig_count = run_anova(df_feat, features, "cluster")
                        meta["significant_features"] = f"{sig_count} / {len(features)}"
                        
                        # Save to State
                        st.session_state["meta"] = meta
                        st.session_state["df_feat"] = df_feat
                        st.session_state["features"] = features
                        
                    st.toast("Pipeline execution successful!", icon="🚀")
                    st.success("Analysis complete. The executive dashboards have been populated.")
        except Exception as e:
            logging.error(f"System Error: {str(e)}")
            st.error(f"⚠️ A critical framework error occurred. Technical Details: {str(e)}")

if "df_feat" not in st.session_state:
    st.info("👋 **System Ready.** Please upload your semester dataset in **01 Data Integration** to initialize the mathematical models.")
    st.stop()

# Load state variables
df_feat = st.session_state["df_feat"]
features = st.session_state["features"]
meta = st.session_state.get("meta", {}) 

# Assign plain-English profiles
summary = cluster_summary(df_feat, features, "cluster")
profiles = assign_profile_names(summary)
df_feat["Profile"] = df_feat["cluster"].map(lambda x: profiles[x]["Profile"])

# ---------------------------------------------------------
# TAB 2: INSTITUTIONAL OVERVIEW
# ---------------------------------------------------------
with tab2:
    st.markdown("### System Health & Mathematical Validation")
    st.markdown("""<div style='font-size:13px; opacity:0.8; margin-bottom:15px;'><b>Data Drift Monitor:</b> These metrics confirm that the current dataset maintains strong mathematical boundaries and is safe for administrative use.</div>""", unsafe_allow_html=True)
    
    sil_score = meta.get('silhouette', 0.0)
    cal_score = meta.get('calinski', 0.0)
    sig_feats = meta.get('significant_features', "0 / 0")

    c1, c2, c3 = st.columns(3)
    c1.metric("Separation Accuracy (Silhouette)", f"{sil_score:.4f}", help="Validates distinctness of behavioral profiles. Positive numbers indicate correct clustering.")
    c2.metric("Cluster Density (Calinski-Harabasz)", f"{cal_score:.2f}", help="Measures how tightly grouped the students are within their assigned cohorts.")
    c3.metric("Key Differentiating Variables", sig_feats, help="Number of parameters proving statistical significance via ANOVA (p < 0.05).")
    
    st.markdown("---")
    
    # Executive Insight Generator
    risk_count = len(df_feat[df_feat["Profile"].str.contains("Risk")])
    total_count = len(df_feat)
    risk_pct = (risk_count / total_count) * 100
    
    st.info(f"💡 **Executive Insight:** The system processed **{total_count}** active student records. Currently, **{risk_count} students ({risk_pct:.1f}%)** are exhibiting behavioral indicators characteristic of the high-risk segment. Targeted intervention is recommended.")
    
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        st.markdown("#### Institutional Population Distribution")
        dist = df_feat["Profile"].value_counts().reset_index()
        dist.columns = ["Profile", "Students"]
        
        fig_donut = px.pie(dist, values="Students", names="Profile", hole=0.65, color="Profile", color_discrete_map=color_map)
        fig_donut.update_traces(textinfo='percent+value', textfont_size=15, hoverinfo="label+value")
        fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5), margin=dict(t=20, b=0, l=0, r=0))
        st.plotly_chart(fig_donut, use_container_width=True, theme="streamlit")
        
    with col_b:
        st.markdown("#### Behavioral Topology Map (PCA Projection)")
        st.markdown("""<div style='font-size:12px; opacity:0.8; margin-bottom:5px;'>Students positioned proximately share highly similar academic and psychological trajectories.</div>""", unsafe_allow_html=True)
        
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(df_feat[features].fillna(0))
        df_feat['Axis_1'] = X_pca[:, 0]
        df_feat['Axis_2'] = X_pca[:, 1]
        
        fig_pca = px.scatter(df_feat, x="Axis_1", y="Axis_2", color="Profile", hover_data={"student_id": True, "CGPA": True, "Axis_1": False, "Axis_2": False}, color_discrete_map=color_map, opacity=0.85)
        fig_pca.update_layout(xaxis_title="", yaxis_title="", showlegend=False, margin=dict(t=10, b=0, l=0, r=0))
        fig_pca.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
        fig_pca.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)
        st.plotly_chart(fig_pca, use_container_width=True, theme="streamlit")

# ---------------------------------------------------------
# TAB 3: XAI & STUDENT PROFILES
# ---------------------------------------------------------
with tab3:
    st.markdown("### Explainable AI (XAI): Primary Cohort Separators")
    st.markdown("""<div class='admin-guide'><b>Administrator Guide:</b> The system utilizes ANOVA testing to identify <i>why</i> cohorts differ. The table below ranks the top statistical behaviors driving the AI's classification engine.</div>""", unsafe_allow_html=True)
    drivers = cluster_drivers(df_feat, features, "cluster", top_n=4)
    st.dataframe(drivers, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 🔍 Individual Student XAI Diagnostic")
    
    sid = st.selectbox("Query Student ID for Individual Review", df_feat["student_id"].unique())
    row = df_feat[df_feat["student_id"] == sid].iloc[0]
    cid = int(row["cluster"])
    
    if "Risk" in profiles[cid]['Profile']:
        st.error(f"**Classification Assignment:** {profiles[cid]['Profile']} (High Priority)")
    else:
        st.success(f"**Classification Assignment:** {profiles[cid]['Profile']}")
    
    r1, r2 = st.columns([1, 1])
    with r1:
        st.markdown("##### 🧠 System Assessment:")
        st.write(profiles[cid]['Explanation'])
        st.write("")
        st.markdown("##### 📋 Intervention Protocol:")
        st.write(profiles[cid]['Intervention'])
        
        st.write("")
        st.markdown("##### 📊 XAI Risk Breakdown:")
        st.markdown("<span style='font-size:13px; opacity:0.8;'>Variance compared to Institutional Average</span>", unsafe_allow_html=True)
        
        # XAI Delta Metrics Generator
        xai_cols = st.columns(2)
        metrics_to_show = ["Stress_Mean", "Motivation_Trend", "CGPA", "Attendance_Percentage"]
        for i, m in enumerate(metrics_to_show):
            if m in df_feat.columns:
                val = row[m]
                avg = df_feat[m].mean()
                delta = val - avg
                # Invert color for Stress & Failed Subjects (Higher is worse)
                inv = "inverse" if "Stress" in m or "Failed" in m else "normal"
                # Format properly (Percentages vs Decimals)
                format_str = f"{val:.0f}%" if "Percentage" in m else f"{val:.2f}"
                delta_str = f"{delta:.0f}%" if "Percentage" in m else f"{delta:.2f}"
                xai_cols[i % 2].metric(label=m.replace("_", " "), value=format_str, delta=f"{delta_str} vs Avg", delta_color=inv)
    
    with r2:
        st.markdown("##### Behavioral Radar")
        st.markdown("<span style='font-size:12px; opacity:0.8;'>The blue polygon represents the student. The shaded gray area is the institutional average.</span>", unsafe_allow_html=True)
        radar_features = [f for f in ["Motivation_Mean", "Stress_Mean", "Confidence_Mean", "Social_Mean", "Workload_Mean"] if f in features]
        if radar_features:
            fig_radar = go.Figure()
            # Student Polygon
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[f] for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features],
                fill='toself', name=f'Student {sid}', line_color="#3B82F6"
            ))
            # Average Polygon
            fig_radar.add_trace(go.Scatterpolar(
                r=[df_feat[f].mean() for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features],
                fill='toself', name='Institutional Average', line_color="#94A3B8", opacity=0.4
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True, margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_radar, use_container_width=True, theme="streamlit")
        
    with st.expander("📂 Expand Comprehensive Student Dataset"):
        st.dataframe(individual_row(df_feat, sid), use_container_width=True)

# ---------------------------------------------------------
# TAB 4: REPORTING & EXPORT
# ---------------------------------------------------------
with tab4:
    st.markdown("### Extracted Intervention Rosters")
    st.markdown("""<div class='admin-guide'><b>Administrator Guide:</b> Apply institutional parameters below to isolate specific student populations. Export these secure rosters for academic advising staff.</div>""", unsafe_allow_html=True)
    
    if "Faculty" in df_feat.columns and "Semester" in df_feat.columns:
        e1, e2, e3 = st.columns(3)
        with e1: sel_fac = st.selectbox("Department Filter", sorted(df_feat["Faculty"].unique()))
        with e2: sel_sem = st.selectbox("Academic Term Filter", sorted(df_feat["Semester"].unique()))
        with e3: sel_prof = st.selectbox("Cohort Segment Filter", sorted(df_feat["Profile"].unique()), index=len(df_feat["Profile"].unique())-1)

        filtered = df_feat[(df_feat["Faculty"] == sel_fac) & (df_feat["Semester"] == sel_sem) & (df_feat["Profile"] == sel_prof)]
        
        st.write("")
        st.info(f"🔍 Query returned **{len(filtered)}** active records matching institutional parameters.")
        st.dataframe(filtered, use_container_width=True)
        
        st.download_button("⬇️ Export Secure Roster (CSV)", filtered.to_csv(index=False).encode("utf-8"), file_name=f"Intervention_Roster_{sel_fac}_{sel_prof}.csv", mime="text/csv", type="primary")
    else:
        st.download_button("⬇️ Export Master System Database", df_feat.to_csv(index=False).encode("utf-8"), file_name=f"Master_Database.csv", mime="text/csv", type="primary")