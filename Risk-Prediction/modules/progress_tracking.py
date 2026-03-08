import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# --- DYNAMIC PATH RESOLUTION (Root-Aware) ---
CURRENT_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CURRENT_MODULE_DIR, "..", "database", "student_success.db")

def run_progress_tracking():
    # =====================================================================
    # 🔙 LOCAL NAVIGATION BUTTON
    # =====================================================================
    st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
    if st.button("« Back to Suite Portal", key="risk_back_btn"):
        st.session_state.current_view = 'MySuite'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("# 📊 Advanced Student Intelligence Suite")
    st.caption("Deep Behavioral Diagnostics & Multidimensional Risk Mapping")

    if 'last_run_data' not in st.session_state:
        st.warning("⚠️ **System Awaiting Input:** Please execute a Diagnostic Scan in the Risk Intelligence module.")
        st.stop() # Prevents the rest of the code from crashing

    # --- 1. DATA INFRASTRUCTURE ---
    data = st.session_state['last_run_data']['details']
    prob = st.session_state['last_run_data']['risk_score']
    status = st.session_state['last_run_data']['status']
    student_id = st.session_state.get('last_student_id', "STU-001")

    # --- 2. THE EXECUTIVE HUD (Heads-Up Display) ---
    st.write(f"### 🧬 Diagnostic ID: {student_id}")
    h1, h2, h3, h4 = st.columns(4)
    
    # Calculate Velocity (Change between P3 and P4)
    p3_avg = np.mean([data.get(f'{m}_Phase3', 3) for m in ['Motivation', 'Confidence', 'Stress']])
    p4_avg = np.mean([data.get(f'{m}_Phase4', 3) for m in ['Motivation', 'Confidence', 'Stress']])
    velocity = p4_avg - p3_avg

    h1.metric("Risk Probability", f"{prob:.1%}", delta=f"{'CRITICAL' if prob > 0.7 else 'ELEVATED' if prob > 0.4 else 'STABLE'}", delta_color="inverse")
    h2.metric("Momentum Velocity", f"{velocity:+.2f}", delta="Recent Shift", delta_color="normal")
    h3.metric("Engagement Index", f"{data.get('Attendance_Percentage', 0)*10}%")
    h4.metric("Academic Load", f"Sem {int(data.get('Semester', 1))}")

    st.divider()

    # --- 3. DEEP BEHAVIORAL TRAJECTORY (Spline Analysis) ---
    st.subheader("📉 Longitudinal Behavioral Analysis")
    st.info("This chart maps the 'Psychological Drift' across 4 key phases of the academic cycle.")
    
    metrics = ['Motivation', 'Stress', 'Confidence', 'Workload', 'Social']
    trend_data = []
    for m in metrics:
        for p in range(1, 5):
            trend_data.append({"Metric": m, "Phase": p, "Score": data.get(f"{m}_Phase{p}", 3.0)})
    
    if PLOTLY_AVAILABLE:
        df_trends = pd.DataFrame(trend_data)
        fig_trends = px.line(df_trends, x="Phase", y="Score", color="Metric", 
                             line_shape="spline", markers=True, 
                             template="plotly_white", # Using white for a cleaner, modern look
                             color_discrete_sequence=px.colors.sequential.Agsunset)
        
        fig_trends.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1), yaxis_range=[0, 5.5])
        # 2026 Syntax Update: width="stretch"
        st.plotly_chart(fig_trends, width="stretch")

    # --- 4. THE BENTO ANALYTICS GRID (Multidimensional) ---
    st.write("### 🧩 Strategic Risk Clusters")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # A. RADAR BALANCE (Baseline vs Current)
        st.markdown("#### ⚖️ Holistic Resilience Balance")
        if PLOTLY_AVAILABLE:
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=[data.get(f"{m}_Phase1", 3) for m in metrics] + [data.get(f"{metrics[0]}_Phase1", 3)],
                theta=metrics + [metrics[0]], fill='toself', name='Baseline (P1)', line_color='#636EFA'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[data.get(f"{m}_Phase4", 3) for m in metrics] + [data.get(f"{metrics[0]}_Phase4", 3)],
                theta=metrics + [metrics[0]], fill='toself', name='Current (P4)', line_color='#EF553B'
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])), showlegend=True, margin=dict(t=20, b=20))
            st.plotly_chart(fig_radar, width="stretch")

    with col_right:
        # B. ACADEMIC ANCHOR POINTS (Bar Chart)
        st.markdown("#### ⚓ Academic Strength Anchors")
        anchors = {
            "GPA Performance": data.get('CGPA', 0) / 4.0 * 5, 
            "Attendance": data.get('Attendance_Percentage', 0) / 2, 
            "Lab Participation": data.get('Lab_Participation', 0),
            "Lecture Participation": data.get('Lecture_Participation', 0),
            "Guidance Level": data.get('Academic_Guidance', 0)
        }
        if PLOTLY_AVAILABLE:
            fig_anchors = px.bar(x=list(anchors.values()), y=list(anchors.keys()), 
                                 orientation='h', color=list(anchors.values()),
                                 color_continuous_scale='RdYlGn', labels={'x':'Strength (0-5)', 'y':''})
            fig_anchors.update_layout(showlegend=False, margin=dict(t=20, b=20))
            st.plotly_chart(fig_anchors, width="stretch")

    # --- 5. DETAILED FEATURE MATRIX (The "Deep Dive") ---
    st.divider()
    st.subheader("🔍 Full Feature Audit Matrix")
    st.write("Every variable processed by the AI is logged here for clinical audit.")
    
    categories = {
        "Demographics": ['Age', 'Gender', 'Faculty', 'Living_Arrangement'],
        "Academic Metrics": ['CGPA', 'Semester', 'Failed_Subjects', 'Attendance_Percentage'],
        "Longitudinal Trends": [c for c in data.keys() if 'Slope' in c or 'Volatility' in c],
        "External Challenges": [c for c in data.keys() if 'Challenge_' in c]
    }

    cat_tabs = st.tabs(list(categories.keys()))
    for i, (cat_name, cat_features) in enumerate(categories.items()):
        with cat_tabs[i]:
            cat_data = {k: v for k, v in data.items() if any(f in k for f in cat_features)}
            if cat_data:
                df_cat = pd.DataFrame(list(cat_data.items()), columns=['Signal', 'Value'])
                st.table(df_cat)
            else:
                st.write("No specific data found for this category.")

    # --- 6. PREDICTIVE LOGS (DB Integration) ---
    st.divider()
    st.subheader("📅 Historical Log & Prediction Dates")
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT prediction_date, risk_status, risk_score FROM risk_history WHERE student_id = ? ORDER BY prediction_date DESC"
        hist_df = pd.read_sql_query(query, conn, params=(student_id,))
        conn.close()

        if not hist_df.empty:
            # 2026 Syntax Update
            st.dataframe(hist_df, width="stretch")
            if PLOTLY_AVAILABLE:
                fig_area = px.area(hist_df, x='prediction_date', y='risk_score', title="Longitudinal Risk Exposure")
                st.plotly_chart(fig_area, width="stretch")
        else:
            st.info("No prior history found. This assessment is currently the Baseline.")
    except Exception as e:
        st.error(f"Database sync failed: {e}")

    # --- 7. ACTIONABLE INTELLIGENCE FOOTER ---
    st.divider()
    st.subheader("💡 Strategic Intervention Priority")
    
    drops = {}
    for m in metrics:
        drops[m] = data.get(f"{m}_Phase1", 3) - data.get(f"{m}_Phase4", 3)
    
    critical_drop = max(drops, key=drops.get)
    
    if drops[critical_drop] > 1.0:
        st.error(f"**PRIORITY 1:** Significant decline detected in `{critical_drop}`. This is the primary driver of the current Risk Score.")
    else:
        st.success("**PRIORITY 1:** Behavioral patterns are within normal variance. Focus on maintaining Academic GPA.")