import streamlit as st
import pandas as pd
import numpy as np

try:
    import plotly.express as px
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

def run_progress_tracking():
    st.markdown("# 📈 Longitudinal Student Trajectory")
    st.caption("Predictive Trend Analysis & Behavioral Mapping")

    if not PLOTLY_AVAILABLE:
        st.error("📊 **Visualization Engine Offline**")
        st.info("To enable these charts, please run `pip install plotly` in your terminal and restart the app.")
        return

    # --- 1. DATA RETRIEVAL ---
    if 'last_run_data' not in st.session_state:
        st.warning("⚠️ **Awaiting Diagnostic Data:** Please run the 'Risk Intelligence' module first.")
        return

    data = st.session_state['last_run_data']['details']
    student_id = st.session_state.get('last_student_id', "STU-001")

    # --- 2. TRAJECTORY VISUALIZATION (Line Chart) ---
    st.subheader(f"🔍 Behavioral Trends: {student_id}")
    
    metrics = ['Motivation', 'Stress', 'Confidence', 'Workload', 'Social']
    trend_list = []
    for m in metrics:
        for p in range(1, 5):
            trend_list.append({
                "Metric": m, 
                "Phase": f"Phase {p}", 
                "Score": data.get(f"{m}_Phase{p}", 3.0)
            })
    
    df_trends = pd.DataFrame(trend_list)

    fig_line = px.line(df_trends, x="Phase", y="Score", color="Metric", 
                       markers=True, line_shape="spline", 
                       template="plotly_white",
                       color_discrete_sequence=px.colors.qualitative.Prism)
    
    fig_line.update_layout(yaxis_range=[0, 5.5], hovermode="x unified")
    st.plotly_chart(fig_line, use_container_width=True)

    # --- 3. HOLISTIC RADAR (Baseline vs Current) ---
    st.divider()
    st.subheader("📌 4-Phase Holistic Balance")
    
    fig_radar = go.Figure()

    # Baseline (Phase 1)
    fig_radar.add_trace(go.Scatterpolar(
        r=[data.get(f"{m}_Phase1", 3) for m in metrics],
        theta=metrics, fill='toself', name='P1 Baseline'
    ))

    # Current (Phase 4)
    fig_radar.add_trace(go.Scatterpolar(
        r=[data.get(f"{m}_Phase4", 3) for m in metrics],
        theta=metrics, fill='toself', name='P4 Current',
        line_color='red'
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
        showlegend=True
    )
    st.plotly_chart(fig_radar, use_container_width=True)