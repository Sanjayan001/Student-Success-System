import pandas as pd
import numpy as np

def cluster_drivers(df: pd.DataFrame, features: list, cluster_col: str = "cluster", top_n: int = 8) -> pd.DataFrame:
    """
    Simple explainability: for each cluster, show features with largest absolute difference from global mean.
    """
    global_mean = df[features].mean(numeric_only=True)
    rows = []
    for c, sub in df.groupby(cluster_col):
        cmean = sub[features].mean(numeric_only=True)
        diff = (cmean - global_mean).abs().sort_values(ascending=False).head(top_n)
        for feat, val in diff.items():
            rows.append({"cluster": int(c), "feature": feat, "abs_diff": float(val), "cluster_mean": float(cmean[feat]), "global_mean": float(global_mean[feat])})
    return pd.DataFrame(rows).sort_values(["cluster","abs_diff"], ascending=[True, False])

def explain_student(row: pd.Series, features: list, cluster_id: int) -> str:
    """
    Plain-language student explanation using key features.
    """
    # pick a few informative features if present
    keys = [f for f in ["CGPA","Failed_Subjects","Attendance_Percentage","Motivation_Mean","Stress_Mean","Confidence_Mean"] if f in features]
    parts = []
    for k in keys[:6]:
        parts.append(f"{k}={row.get(k)}")
    return f"Student assigned to Cluster {cluster_id}. Key indicators: " + ", ".join(parts) + "."
