from typing import List, Tuple
import pandas as pd

# Minimal columns. Others are optional and handled gracefully.
MIN_REQUIRED = ["CGPA", "Failed_Subjects"]

def validate_dataset(df: pd.DataFrame) -> Tuple[List[str], pd.DataFrame]:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    missing = [c for c in MIN_REQUIRED if c not in df.columns]

    # auto-add student_id if missing
    if "student_id" not in df.columns:
        df.insert(0, "student_id", [f"S{i:04d}" for i in range(1, len(df)+1)])

    # standardize semester column name (optional)
    if "Semester" not in df.columns and "semester" in df.columns:
        df.rename(columns={"semester": "Semester"}, inplace=True)
    if "Semester" not in df.columns:
        df["Semester"] = "Unknown"

    return missing, df
