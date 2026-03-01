import os
import logging
import json
import joblib
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score, adjusted_rand_score
from scipy.stats import f_oneway

# ==========================================
# 1. ENTERPRISE LOGGING SETUP
# ==========================================
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/mlops.log", 
    level=logging.INFO, 
    format="%(asctime)s - [%(levelname)s] - %(message)s"
)

# ==========================================
# 2. PATHS & DIRECTORIES
# ==========================================
MODEL_DIR = "models"
EXP_DIR = "experiments"
PIPELINE_PATH = os.path.join(MODEL_DIR, "clustering_pipeline.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "features.json")
METRICS_PATH = os.path.join(MODEL_DIR, "metrics.json")

def _safe_impute(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy().replace([np.inf, -np.inf], np.nan)
    return X.fillna(X.median(numeric_only=True)).fillna(0)

def model_exists() -> bool:
    return os.path.exists(PIPELINE_PATH) and os.path.exists(FEATURES_PATH)

def train_kmeans(df: pd.DataFrame, features: list, k: int = 3, random_state: int = 42) -> dict:
    logging.info(f"Starting pipeline. Training on {len(df)} records with k={k}.")
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(EXP_DIR, exist_ok=True)
    
    X = _safe_impute(df[features])
    
    # Professional Pipeline (Prevents data leakage)
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('kmeans', KMeans(n_clusters=int(k), random_state=random_state, n_init=10))
    ])
    
    labels = pipeline.fit_predict(X)
    Xs = pipeline.named_steps['scaler'].transform(X)
    
    # Advanced Validation Metrics
    metrics = {
        "k": int(k),
        "rows": int(len(df)),
        "silhouette": float(silhouette_score(Xs, labels)) if len(set(labels)) > 1 else 0.0,
        "davies_bouldin": float(davies_bouldin_score(Xs, labels)) if len(set(labels)) > 1 else 0.0,
        "calinski_harabasz": float(calinski_harabasz_score(Xs, labels)) if len(set(labels)) > 1 else 0.0
    }
    
    # Stability Testing (10 Seeds) via Adjusted Rand Index
    history = []
    for seed in range(10):
        model = KMeans(n_clusters=k, random_state=seed, n_init=5)
        history.append(model.fit_predict(Xs))
    
    ari_scores = [adjusted_rand_score(history[i], history[j]) for i in range(10) for j in range(i + 1, 10)]
    metrics["stability_ari"] = float(np.mean(ari_scores)) if ari_scores else 0.0
    
    logging.info(f"Model validated. Silhouette: {metrics['silhouette']:.3f} | Stability ARI: {metrics['stability_ari']:.3f}")
    
    # ==========================================
    # 3. EXPERIMENT TRACKING (Model Registry)
    # ==========================================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_folder = os.path.join(EXP_DIR, f"run_{timestamp}")
    os.makedirs(run_folder, exist_ok=True)
    
    # Save historical archive to experiments folder
    joblib.dump(pipeline, os.path.join(run_folder, "pipeline.pkl"))
    with open(os.path.join(run_folder, "metrics.json"), "w") as f: json.dump(metrics, f)
    with open(os.path.join(run_folder, "features.json"), "w") as f: json.dump(features, f)
    logging.info(f"Experiment saved to registry: {run_folder}")
    
    # Save active model for the live dashboard
    joblib.dump(pipeline, PIPELINE_PATH)
    with open(FEATURES_PATH, "w") as f: json.dump(features, f)
    with open(METRICS_PATH, "w") as f: json.dump(metrics, f)
    
    return metrics

def load_model():
    pipeline = joblib.load(PIPELINE_PATH)
    with open(FEATURES_PATH, "r") as f: features = json.load(f)
    
    metrics = None
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f: metrics = json.load(f)
        
    return pipeline, features, metrics

def predict(df: pd.DataFrame):
    pipeline, features, _ = load_model()
    X = _safe_impute(df[features])
    return pipeline.predict(X)

def run_anova(df: pd.DataFrame, features: list, cluster_col: str = "cluster") -> int:
    """Returns the number of statistically significant features using ANOVA."""
    clusters = df[cluster_col].unique()
    sig_count = 0
    for feat in features:
        groups = [df[df[cluster_col] == c][feat].dropna().values for c in clusters]
        
        # FIXED: Only run ANOVA if all clusters have > 1 sample. 
        # This prevents the 'numpy RuntimeWarning: Mean of empty slice'
        if all(len(g) > 1 for g in groups):
            _, p_val = f_oneway(*groups)
            if p_val < 0.05:
                sig_count += 1
                
    return sig_count