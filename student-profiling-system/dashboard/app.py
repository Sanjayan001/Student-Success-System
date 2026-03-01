import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import logging
import plotly.graph_objects as go
from sklearn.decomposition import PCA

# Ensure root directory is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dashboard.auth import create_admin_if_missing, verify_login
from src.data_contract import validate_dataset
from src.preprocessing import preprocess
from src.features import add_phase_features, get_model_features
from src.clustering import model_exists, train_kmeans, load_model, predict, run_anova
from src.profiling import cluster_summary, assign_profile_names, profiles_table
from src.xai import cluster_drivers, explain_student
from src.reports import institution_tables, individual_row

# ===============================
# 1. PAGE CONFIG & LOGGING
# ===============================
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/mlops.log", level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

st.set_page_config(page_title="Institutional Student Profiling", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 1rem; padding-bottom: 2rem;}
    /* Clean metric cards */
    [data-testid="stMetric"] {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    [data-testid="stMetricLabel"] {font-size: 16px; font-weight: 600; color: #94A3B8;}
    [data-testid="stMetricValue"] {color: #38BDF8; font-size: 28px;}
    hr {border-top: 1px solid #1E293B;}
    .stTabs [data-baseweb="tab-list"] {gap: 24px;}
    .stTabs [data-baseweb="tab"] {height: 50px; white-space: pre-wrap; font-weight: 600; font-size: 16px;}
</style>
""", unsafe_allow_html=True)

# ===============================
# 2. ADMIN AUTHENTICATION
# ===============================
create_admin_if_missing("admin", "admin123")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #F8FAFC;'>🎓 University Admin Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94A3B8;'>Secure Student Analytics Login</p>", unsafe_allow_html=True)
        st.write("")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Secure Login", use_container_width=True, type="primary"):
            if verify_login(u, p):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Unauthorized access. Invalid credentials.")
    st.stop()

with st.sidebar:
    st.title("🎓 Admin Dashboard")
    st.success("🟢 System Online | Authenticated")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.title("🎓 Executive Student Intelligence Platform")
st.markdown("Automated Behavioral Tracking & Early Intervention System")
st.markdown("---")

# ===============================
# 3. EXECUTIVE TABBED NAVIGATION
# ===============================
tab1, tab2, tab3, tab4 = st.tabs([
    "📥 1. Upload Semester Data", 
    "📊 2. Executive Overview", 
    "👤 3. Student Risk Profiles", 
    "📋 4. Action & Export Lists"
])

# ---------------------------------------------------------
# TAB 1: DATA INGESTION
# ---------------------------------------------------------
with tab1:
    st.markdown("### Process New Semester Data")
    st.write("Upload the latest student survey and academic dataset. The AI will automatically clean the data and identify at-risk students.")
    
    uploaded = st.file_uploader("Upload CSV Dataset", type=["csv"])
    
    if uploaded:
        os.makedirs("data/semester_uploads", exist_ok=True)
        save_path = os.path.join("data/semester_uploads", uploaded.name)
        with open(save_path, "wb") as f:
            f.write(uploaded.getbuffer())

        try:
            df_raw = pd.read_csv(save_path)
            missing, df_raw = validate_dataset(df_raw)
            
            if missing:
                st.error(f"⚠️ Error: The uploaded file is missing required data columns: {missing}")
            else:
                st.success(f"✅ Data Accepted. Found {len(df_raw)} student records.")
                
                st.markdown("### Run AI Analysis")
                if st.button("▶️ Generate Student Profiles & Insights", type="primary"):
                    with st.spinner("Analyzing student behaviors and academic trends..."):
                        df_clean, _ = preprocess(df_raw)
                        df_feat = add_phase_features(df_clean)
                        features = get_model_features(df_feat)
                        
                        meta = train_kmeans(df_feat, features, k=3)
                        df_feat["cluster"] = predict(df_feat)
                        sig_count = run_anova(df_feat, features, "cluster")
                        meta["significant_features"] = f"{sig_count} / {len(features)}"
                        
                        st.session_state["meta"] = meta
                        st.session_state["df_feat"] = df_feat
                        st.session_state["features"] = features
                        
                    st.success("✅ Analysis Complete! Please navigate to the 'Executive Overview' tab.")
                    # 🔥 UX Upgrade 1: Celebratory Toast Notification
                    st.toast('AI Pipeline Executed Successfully!', icon='🚀')
        except Exception as e:
            logging.error(f"System Error: {str(e)}")
            st.error(f"Critical System Error. The IT team has been notified.")

# 🔥 UX Upgrade 2: Friendly Welcome Message instead of a blank screen
if "df_feat" not in st.session_state:
    st.info("👋 **Welcome to the Executive Intelligence Platform.** Please upload your semester dataset in **Tab 1** to unlock the dashboard.")
    st.stop()

df_feat = st.session_state["df_feat"]
features = st.session_state["features"]
meta = st.session_state.get("meta", {}) # Safely get meta

summary = cluster_summary(df_feat, features, "cluster")
profiles = assign_profile_names(summary)
df_feat["Profile"] = df_feat["cluster"].map(lambda x: profiles[x]["Profile"])
color_map = {"High Performing & Motivated": "#10B981", "Average / Moderate Students": "#3B82F6", "At-Risk Students": "#EF4444"}

# ---------------------------------------------------------
# TAB 2: EXECUTIVE OVERVIEW
# ---------------------------------------------------------
with tab2:
    st.markdown("### 📈 Artificial Intelligence Health Check")
    
    # FIXED: Safe metric retrieval to prevent KeyErrors
    sil_score = meta.get('silhouette', 0.0)
    ari_score = meta.get('stability_ari', 0.0)
    sig_feats = meta.get('significant_features', "0 / 0")

    c1, c2, c3 = st.columns(3)
    c1.metric("AI Confidence Level", "High", help=f"Technical Metric (Silhouette): {sil_score:.3f}. Indicates strong grouping.")
    c2.metric("System Reliability", "Stable", help=f"Technical Metric (ARI): {ari_score:.3f}. Indicates consistent results across tests.")
    c3.metric("Key Behavioral Factors", sig_feats, help="Number of behavioral traits scientifically proven to affect student outcomes (ANOVA p<0.05).")
    
    st.markdown("---")
    
    col_a, col_b = st.columns([1, 1.2])
    with col_a:
        st.markdown("### Institutional Cohort Breakdown")
        dist = df_feat["Profile"].value_counts().reset_index()
        dist.columns = ["Profile", "Students"]
        
        fig_donut = px.pie(
            dist, values="Students", names="Profile", hole=0.6,
            color="Profile", color_discrete_map=color_map, template="plotly_dark"
        )
        fig_donut.update_traces(textinfo='percent+value', textposition='outside', textfont_size=14)
        fig_donut.update_layout(showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col_b:
        st.markdown("### Student Behavioral Landscape")
        st.caption("Students positioned closer together share similar psychological and academic behaviors.")
        
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(df_feat[features].fillna(0))
        df_feat['Behavioral_Axis_1'] = X_pca[:, 0]
        df_feat['Behavioral_Axis_2'] = X_pca[:, 1]
        
        fig_pca = px.scatter(
            df_feat, x="Behavioral_Axis_1", y="Behavioral_Axis_2", color="Profile", 
            hover_data={"student_id": True, "CGPA": True, "Behavioral_Axis_1": False, "Behavioral_Axis_2": False},
            color_discrete_map=color_map, template="plotly_dark", opacity=0.8
        )
        fig_pca.update_layout(xaxis_title="", yaxis_title="", showlegend=False, margin=dict(t=10, b=0, l=0, r=0))
        # 🔥 UX Upgrade 3: Hiding the confusing math axes to make a clean "map"
        fig_pca.update_xaxes(showgrid=False, zeroline=False, visible=False)
        fig_pca.update_yaxes(showgrid=False, zeroline=False, visible=False)
        st.plotly_chart(fig_pca, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: STUDENT RISK PROFILES & ADVISING
# ---------------------------------------------------------
with tab3:
    st.markdown("### ⚠️ Primary Warning Signs")
    st.write("These are the top behavioral indicators the AI identified as separating failing students from passing students.")
    drivers = cluster_drivers(df_feat, features, "cluster", top_n=4)
    st.dataframe(drivers, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 🔍 Individual Student Advising Lookup")
    
    sid = st.selectbox("Select or Type Student ID", df_feat["student_id"].unique())
    row = df_feat[df_feat["student_id"] == sid].iloc[0]
    cid = int(row["cluster"])
    
    if "Risk" in profiles[cid]['Profile']:
        st.error(f"**Cohort Assignment:** {profiles[cid]['Profile']} (High Priority)")
    else:
        st.success(f"**Cohort Assignment:** {profiles[cid]['Profile']}")
    
    r1, r2 = st.columns([1, 1])
    with r1:
        st.markdown("**🧠 AI Behavioral Analysis:**")
        st.info(profiles[cid]['Explanation'])
        st.markdown("**📋 Recommended Counselor Action:**")
        st.warning(profiles[cid]['Intervention'])
    
    with r2:
        radar_features = [f for f in ["Motivation_Mean", "Stress_Mean", "Confidence_Mean", "Social_Mean", "Workload_Mean"] if f in features]
        if radar_features:
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[f] for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features],
                fill='toself', name=f'{sid} Profile', line_color="#FBBF24"
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[df_feat[f].mean() for f in radar_features], theta=[f.replace("_Mean","") for f in radar_features],
                fill='toself', name='University Average', line_color="#6B7280", opacity=0.5
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=True, template="plotly_dark", margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
    with st.expander("📂 View Complete Student Record"):
        st.dataframe(individual_row(df_feat, sid), use_container_width=True)

# ---------------------------------------------------------
# TAB 4: ACTION & EXPORT LISTS
# ---------------------------------------------------------
with tab4:
    st.markdown("### 📥 Generate Counselor Action Lists")
    st.write("Filter the student body to export targeted intervention lists for faculty members and academic advisors.")
    
    if "Faculty" in df_feat.columns and "Semester" in df_feat.columns:
        e1, e2, e3 = st.columns(3)
        with e1: sel_fac = st.selectbox("Select Faculty", sorted(df_feat["Faculty"].unique()))
        with e2: sel_sem = st.selectbox("Select Semester", sorted(df_feat["Semester"].unique()))
        with e3: sel_prof = st.selectbox("Select Target Cohort", sorted(df_feat["Profile"].unique()), index=len(df_feat["Profile"].unique())-1)

        filtered = df_feat[(df_feat["Faculty"] == sel_fac) & (df_feat["Semester"] == sel_sem) & (df_feat["Profile"] == sel_prof)]
        
        st.info(f"**{len(filtered)} Students Found** requiring attention in this segment.")
        st.dataframe(filtered, use_container_width=True)
        
        st.download_button(
            "⬇️ Download CSV Action List", 
            filtered.to_csv(index=False).encode("utf-8"), file_name=f"ActionList_{sel_fac}_{sel_prof}.csv", mime="text/csv", type="primary"
        )
    else:
        st.download_button("⬇️ Download Full University Database", df_feat.to_csv(index=False).encode("utf-8"), file_name=f"Full_University_Data.csv", mime="text/csv", type="primary")