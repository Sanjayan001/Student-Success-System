import pandas as pd
import numpy as np
from typing import Tuple, List
from .clean_data import clean_dataframe
from .encode_features import encode_survey_ranges

def preprocess(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    df = clean_dataframe(df)
    df = encode_survey_ranges(df)

    # enforce numeric for key columns if present
    for c in ["CGPA", "Failed_Subjects", "Attendance_Percentage"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # clip CGPA realistic range
    if "CGPA" in df.columns:
        df["CGPA"] = df["CGPA"].clip(0, 4)

    # fill numeric missing with median, fallback 0
    filled = []
    for c in df.select_dtypes(include="number").columns:
        if df[c].isna().any():
            filled.append(c)
            med = df[c].median()
            if pd.isna(med):
                med = 0
            df[c] = df[c].fillna(med)

    # replace remaining inf/nan
    df = df.replace([np.inf, -np.inf], np.nan)
    for c in df.select_dtypes(include="number").columns:
        df[c] = df[c].fillna(0)

    return df, filled
