import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

def scale_features(df: pd.DataFrame, feature_cols: list):
    X = df[feature_cols].copy()
    X = X.replace([np.inf, -np.inf], np.nan)

    med = X.median(numeric_only=True).fillna(0)
    X = X.fillna(med).fillna(0)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    return Xs, scaler
