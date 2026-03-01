import pandas as pd

def institution_tables(df: pd.DataFrame):
    dist = (
        df["cluster"]
        .value_counts()
        .rename_axis("cluster")
        .reset_index(name="students")
        .sort_values("cluster")
    )
    return {"cluster_distribution": dist}

def individual_row(df: pd.DataFrame, student_id: str) -> pd.DataFrame:
    return df[df["student_id"] == student_id].head(1)

def integration_export(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["student_id","Semester","cluster","CGPA","Failed_Subjects","Attendance_Percentage"] if c in df.columns]
    return df[cols].copy()
