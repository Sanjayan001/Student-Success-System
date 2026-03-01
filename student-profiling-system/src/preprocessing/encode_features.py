import re
import pandas as pd
import numpy as np

LIKERT_5 = {
    "very low": 1, "low": 2, "medium": 3, "neutral": 3, "high": 4, "very high": 5,
    "strongly disagree": 1, "disagree": 2, "agree": 4, "strongly agree": 5
}

def _parse_percent(s: str):
    s = s.strip().lower()
    # "76-100%" -> 88, "Above 90%" -> 95
    m = re.search(r"(\d+)\s*-\s*(\d+)\s*%?", s)
    if m:
        a,b = float(m.group(1)), float(m.group(2))
        return (a+b)/2.0
    m = re.search(r"above\s*(\d+)", s)
    if m:
        return float(m.group(1)) + 5
    m = re.search(r"below\s*(\d+)", s)
    if m:
        return max(0.0, float(m.group(1)) - 5)
    return None

def _parse_range_number(s: str):
    # "16-20 hours" / "9-12 times" / "0-3" -> midpoint
    s = s.strip().lower()
    m = re.search(r"(\d+)\s*-\s*(\d+)", s)
    if m:
        a,b = float(m.group(1)), float(m.group(2))
        return (a+b)/2.0
    m = re.search(r"more than\s*(\d+)", s)
    if m:
        return float(m.group(1)) + 2
    m = re.search(r"(\d+)\s*or more", s)
    if m:
        return float(m.group(1))
    return None

def encode_survey_ranges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert common survey text ranges to numeric.
    Leaves unknown strings as NaN (handled later by imputation).
    """
    df = df.copy()

    for col in df.columns:
        if df[col].dtype == "object":
            # try likert mapping
            lowered = df[col].astype(str).str.strip().str.lower()
            if lowered.isin(LIKERT_5.keys()).mean() > 0.5:
                df[col] = lowered.map(LIKERT_5)
                continue

            # try percent mapping
            if lowered.str.contains("%").mean() > 0.3 or lowered.str.contains("above|below").mean() > 0.3:
                df[col] = lowered.apply(lambda x: _parse_percent(x) if isinstance(x, str) else np.nan)
                continue

            # try numeric range mapping
            if lowered.str.contains(r"\d+\s*-\s*\d+").mean() > 0.3 or lowered.str.contains("more than|or more").mean() > 0.2:
                df[col] = lowered.apply(lambda x: _parse_range_number(x) if isinstance(x, str) else np.nan)
                continue

    return df
