import pandas as pd
import numpy as np


PHASE_PREFIXES = ["Motivation","Stress","Sleep_Hours","Confidence","Social","Relaxation","Workload"]

BASE_FEATURES = [
    "CGPA","Failed_Subjects","Attendance_Percentage","Study_Hours",
    "Assignment_Submission","Lecture_Participation","Lab_Participation",
    "Academic_Guidance","LMS_Logins","LMS_Hours"
]

def _fill_median_or_zero(s: pd.Series) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    med = s.median()
    if pd.isna(med):
        med = 0
    return s.fillna(med)

def add_phase_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for prefix in PHASE_PREFIXES:
        cols = [f"{prefix}_Phase{i}" for i in range(1,5)]
        if all(c in df.columns for c in cols):
            for c in cols:
                df[c] = pd.to_numeric(df[c], errors="coerce")
            mean_col = f"{prefix}_Mean"
            trend_col = f"{prefix}_Trend"
            df[mean_col] = df[cols].mean(axis=1)
            df[trend_col] = df[cols[-1]] - df[cols[0]]
            df[mean_col] = _fill_median_or_zero(df[mean_col])
            df[trend_col] = _fill_median_or_zero(df[trend_col])
    return df

def get_model_features(df: pd.DataFrame) -> list:
    feats = []
    for c in BASE_FEATURES:
        if c in df.columns:
            df[c] = _fill_median_or_zero(df[c])
            feats.append(c)
    for prefix in PHASE_PREFIXES:
        for suf in ["Mean","Trend"]:
            col = f"{prefix}_{suf}"
            if col in df.columns:
                df[col] = _fill_median_or_zero(df[col])
                feats.append(col)
    # safety: drop duplicates
    return list(dict.fromkeys(feats))
