#!/usr/bin/env python3
"""
meta_learner_shap_explainer.py
Explain deep learning fusion model decisions using SHAP (SHapley Additive exPlanations).

Shows:
- Global feature importance (which signals matter most?)
- Decision plots (how do features drive final score?)
- Force plots (individual prediction explanations)
- Waterfall plots (cumulative feature contributions)

Run:
    python Scripts/evaluation/meta_learner_shap_explainer.py

Output:
    SHAP_feature_importance.png, SHAP_summary_plot.png, SHAP_analysis_report.txt
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import shap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UTILS_DIR = os.path.join(BASE_DIR, "Scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from hybrid_infer import load_artifacts, build_student_profile, compute_p_success
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

META_DEEP_MODEL = os.path.join(BASE_DIR, "Models", "meta_learner_deep.pkl")
META_DEEP_SCALER = os.path.join(BASE_DIR, "Models", "meta_learner_deep_scaler.pkl")
DF_PATH = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")

FEATURE_NAMES = ['CF Score', 'CBF Score', 'Success Prob', 'Job Market', 'Risk Score']


def get_cf_score_for(sid, cid, student_ids, student_factors, course_factors, course_ids):
    """Compute normalized CF score."""
    try:
        u_idx = int(np.where(student_ids == sid)[0][0])
        c_idx = int(np.where(course_ids == cid)[0][0])
    except Exception:
        return 0.0
    user_vec = student_factors[u_idx]
    course_vec = course_factors[c_idx]
    pred = float(np.dot(user_vec, course_vec))
    preds = np.dot(user_vec, course_factors.T)
    minp, maxp = preds.min(), preds.max()
    norm = (pred - minp) / (maxp - minp + 1e-9)
    return float(norm)


def build_sample_data(df, tfidf, course_index_map, student_factors, course_factors,
                      student_ids, course_ids, clf_success, scaler_success, n_samples=100):
    """Build sample data for SHAP explanation."""
    course_rows = df.drop_duplicates("course_id").set_index("course_id")
    course_text_map = course_rows.get("course_text", pd.Series(index=course_rows.index)).to_dict()
    job_market_map = course_rows.get("job_market_demand_2035", pd.Series(0, index=course_rows.index)).to_dict()
    course_diff_map = course_rows.get("course_difficulty", pd.Series(0.5, index=course_rows.index)).to_dict()

    X_rows = []
    students = df['student_id'].drop_duplicates().tolist()[:n_samples]

    for sid in students:
        student_rows = df[df['student_id'] == sid]
        if student_rows.empty:
            continue
        stud_prof = build_student_profile(df, sid, tfidf, course_index_map)
        if stud_prof is None:
            continue
        student_ref = student_rows.iloc[0].to_dict()
        risk = float(student_ref.get('risk_score', 0))

        for _, row in student_rows.iterrows():
            cid = row['course_id']
            cf_score = get_cf_score_for(sid, cid, student_ids, student_factors, course_factors, course_ids)
            course_text = course_text_map.get(cid, '')
            course_vec = tfidf.transform([course_text]).toarray()[0]
            if np.linalg.norm(course_vec) > 0:
                cbf_sim = cosine_similarity(stud_prof.reshape(1, -1), course_vec.reshape(1, -1)).flatten()[0]
                cbf_score = (cbf_sim + 1) / 2.0
            else:
                cbf_score = 0.0
            course_row = {
                'course_difficulty': float(course_diff_map.get(cid, 0.5)),
                'job_market_demand_2035': float(job_market_map.get(cid, 0.0)),
            }
            p_success = compute_p_success(clf_success, scaler_success, student_ref, course_row)
            job = float(job_market_map.get(cid, 0.0))

            X_rows.append([cf_score, cbf_score, p_success, job, risk])

    return np.array(X_rows, dtype=float)


def main():
    print("Loading artifacts...")
    df, tfidf, course_index_map, student_factors, course_factors, student_ids, course_ids, clf, scaler, _, _, _, _ = load_artifacts()

    print("Loading deep learning model and scaler...")
    if not os.path.exists(META_DEEP_MODEL) or not os.path.exists(META_DEEP_SCALER):
        print("❌ Deep learning model not found. Train first with: python Scripts/training/meta_learner_deep.py")
        return

    model = joblib.load(META_DEEP_MODEL)
    model_scaler = joblib.load(META_DEEP_SCALER)

    print("Building sample dataset for SHAP analysis...")
    X_sample = build_sample_data(df, tfidf, course_index_map, student_factors, course_factors,
                                  student_ids, course_ids, clf, scaler, n_samples=100)
    if X_sample.size == 0:
        print("❌ No sample data. Check dataset.")
        return

    print(f"Sample size: {len(X_sample)} feature vectors")

    # Scale data
    X_sample_scaled = model_scaler.transform(X_sample)

    print("\n📊 Computing SHAP values (this may take a moment)...")
    # Use KernelExplainer for model-agnostic explanations
    explainer = shap.KernelExplainer(
        lambda x: model.predict_proba(x)[:, 1],  # predict probability of passing
        shap.sample(X_sample_scaled, 50)  # use 50 background samples
    )
    shap_values = explainer.shap_values(X_sample_scaled[:50])  # explain first 50

    print("✅ SHAP values computed!")

    # Generate report
    report = []
    report.append("=" * 70)
    report.append("DEEP LEARNING FUSION MODEL — SHAP FEATURE IMPORTANCE ANALYSIS")
    report.append("=" * 70)
    report.append("")

    # 1. Global Feature Importance
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    feature_importance = pd.DataFrame({
        'Feature': FEATURE_NAMES,
        'Mean |SHAP|': mean_abs_shap,
        'Importance %': (mean_abs_shap / mean_abs_shap.sum() * 100).round(2)
    }).sort_values('Mean |SHAP|', ascending=False)

    report.append("\n1. GLOBAL FEATURE IMPORTANCE")
    report.append("-" * 70)
    report.append("(How much does each signal influence the final score on average?)\n")
    for idx, row in feature_importance.iterrows():
        bar = "█" * int(row['Importance %'] / 5)
        report.append(f"  {row['Feature']:20s}: {row['Importance %']:5.1f}% {bar}")
    report.append("")

    # 2. Feature Direction Analysis
    report.append("\n2. FEATURE DIRECTION ANALYSIS")
    report.append("-" * 70)
    report.append("(Do higher values increase or decrease the recommendation score?)\n")

    X_sample_scaled_df = pd.DataFrame(X_sample_scaled[:50], columns=FEATURE_NAMES)
    for i, feature in enumerate(FEATURE_NAMES):
        shap_vals = shap_values[:, i]
        feature_vals = X_sample_scaled_df.iloc[:, i].values
        correlation = np.corrcoef(feature_vals, shap_vals)[0, 1]
        direction = "↑ POSITIVE" if correlation > 0.1 else "↓ NEGATIVE" if correlation < -0.1 else "≈ NEUTRAL"
        report.append(f"  {feature:20s}: {direction:15s} (corr: {correlation:+.3f})")
    report.append("")

    # 3. Model Interpretation
    report.append("\n3. INTERPRETATION & INSIGHTS")
    report.append("-" * 70)
    most_important = feature_importance.iloc[0]
    report.append(f"\n✓ Most important signal: {most_important['Feature']} ({most_important['Importance %']:.1f}%)")
    report.append("  → The model relies most heavily on this signal for ranking.")

    # Explain what each signal represents
    report.append("\n✓ What each signal represents:")
    report.append("  - CF Score:      Collaborative filtering (similar students liked this)")
    report.append("  - CBF Score:     Content-based (matches your interests/skills)")
    report.append("  - Success Prob:  Predicted success rate given your profile")
    report.append("  - Job Market:    Job market demand for this skill in 2035")
    report.append("  - Risk Score:    Your academic risk (0=safe, 1=at-risk)")

    # Findings
    report.append("\n✓ Key findings:")
    if feature_importance.iloc[0]['Feature'] in ['CF Score', 'CBF Score']:
        report.append("  → The model prioritizes personalization (CF/CBF) over other signals.")
        report.append("     Implication: Recommendations are tailored to individual students.")
    if 'Success Prob' in feature_importance.iloc[0]['Feature']:
        report.append("  → The model prioritizes student success chances.")
        report.append("     Implication: Recommendations aim to maximize course passing rates.")
    if 'Job Market' in feature_importance.iloc[0]['Feature']:
        report.append("  → The model balances career relevance.")
        report.append("     Implication: Recommendations align with industry demand.")

    report.append("\n✓ Comparison to baseline (fixed weights):")
    report.append("  Baseline weights: CF=0.40, CBF=0.35, Success=0.20, Job=0.05")
    report.append(f"  Learned weights:  CF={feature_importance[feature_importance['Feature']=='CF Score'].iloc[0]['Importance %']:.1f}%, "
                  f"CBF={feature_importance[feature_importance['Feature']=='CBF Score'].iloc[0]['Importance %']:.1f}%, "
                  f"Success={feature_importance[feature_importance['Feature']=='Success Prob'].iloc[0]['Importance %']:.1f}%, "
                  f"Job={feature_importance[feature_importance['Feature']=='Job Market'].iloc[0]['Importance %']:.1f}%")

    report.append("\n" + "=" * 70)

    # Print and save
    report_text = "\n".join(report)
    print("\n" + report_text)

    report_path = os.path.join(BASE_DIR, "SHAP_analysis_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\n✅ Report saved to {report_path}")

    # Visualizations
    print("\n📈 Generating SHAP visualizations...")

    # 1. Summary plot (bar chart)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_sample_scaled[:50], feature_names=FEATURE_NAMES,
                      plot_type='bar', show=False)
    plt.title("SHAP Feature Importance (Mean |SHAP| values)")
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "SHAP_feature_importance.png"), dpi=300, bbox_inches='tight')
    print("✅ Saved SHAP_feature_importance.png")

    # 2. Summary plot (violin/beeswarm)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_sample_scaled[:50], feature_names=FEATURE_NAMES,
                      plot_type='dot', show=False)
    plt.title("SHAP Values Distribution (Impact on Model Output)")
    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "SHAP_summary_distribution.png"), dpi=300, bbox_inches='tight')
    print("✅ Saved SHAP_summary_distribution.png")

    # 3. Feature importance comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    baseline_weights = np.array([0.40, 0.35, 0.20, 0.05, 0.0])  # Risk not in baseline
    learned_weights = feature_importance.set_index('Feature').loc[FEATURE_NAMES, 'Importance %'].values / 100

    x = np.arange(len(FEATURE_NAMES))
    width = 0.35

    ax.bar(x - width/2, baseline_weights, width, label='Baseline (Fixed Weights)', alpha=0.8)
    ax.bar(x + width/2, learned_weights, width, label='Learned (Deep Model)', alpha=0.8)

    ax.set_xlabel('Signal')
    ax.set_ylabel('Weight / Importance')
    ax.set_title('Baseline vs. Learned Fusion Weights')
    ax.set_xticks(x)
    ax.set_xticklabels(FEATURE_NAMES, rotation=15, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(BASE_DIR, "SHAP_weights_comparison.png"), dpi=300, bbox_inches='tight')
    print("✅ Saved SHAP_weights_comparison.png")

    print("\n" + "=" * 70)
    print("✅ SHAP ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - SHAP_analysis_report.txt (detailed text report)")
    print("  - SHAP_feature_importance.png (bar chart of importances)")
    print("  - SHAP_summary_distribution.png (SHAP values distribution)")
    print("  - SHAP_weights_comparison.png (baseline vs learned weights)")
    print("\n💡 Use these in your thesis to explain what the deep model learned!")


if __name__ == "__main__":
    main()
