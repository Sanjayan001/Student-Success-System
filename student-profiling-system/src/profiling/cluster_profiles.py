import pandas as pd

def cluster_summary(df: pd.DataFrame, features: list, cluster_col: str = "cluster") -> pd.DataFrame:
    return df.groupby(cluster_col)[features].mean(numeric_only=True)

def assign_profile_names(summary: pd.DataFrame) -> dict:
    profiles = {}
    clusters = list(summary.index)

    if "CGPA" in summary.columns:
        best = summary["CGPA"].idxmax()
        worst = summary["CGPA"].idxmin()
    else:
        best = clusters[0]
        worst = clusters[-1]

    for c in clusters:
        if c == best:
            profiles[c] = {
                "Profile": "High Performing & Motivated",
                "Explanation": "Strong academic performance and stable engagement.",
                "Intervention": "Advanced opportunities, leadership programs, mentorship roles."
            }
        elif c == worst:
            profiles[c] = {
                "Profile": "At-Risk Students",
                "Explanation": "Lower academic performance and/or low engagement indicators.",
                "Intervention": "Academic mentoring, counseling, attendance monitoring, study skills workshops."
            }
        else:
            profiles[c] = {
                "Profile": "Average / Moderate Students",
                "Explanation": "Moderate performance with mixed engagement patterns.",
                "Intervention": "Regular monitoring, peer study groups, targeted skill workshops."
            }
    return profiles

def profiles_table(profiles: dict) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(profiles, orient="index")
    df.index.name = "Cluster"
    return df.reset_index()
