import os

def export_all(df_feat, prof_tbl, drivers, summary):
    # ✅ ensure folders exist
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    df_feat.to_csv("data/processed/clustered_students.csv", index=False)
    prof_tbl.to_csv("reports/cluster_profiles.csv", index=False)
    drivers.to_csv("reports/cluster_explanations.csv", index=False)
    summary.to_csv("reports/cluster_summary_means.csv", index=True)
