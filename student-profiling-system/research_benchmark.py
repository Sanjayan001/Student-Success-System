import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import logging

# Import your excellent feature engineering code
from src.features import add_phase_features, get_model_features

# Set up simple logging
logging.basicConfig(level=logging.INFO, format="%(message)s")

def run_algorithmic_benchmark(csv_path):
    logging.info("Starting Algorithmic Benchmarking...")
    
    # 1. Load the pre-cleaned data directly
    logging.info(f"Loading dataset from: {csv_path}")
    df_clean = pd.read_csv(csv_path)
    
    # 2. Apply your Temporal Feature Engineering
    df_feat = add_phase_features(df_clean)
    features = get_model_features(df_feat)
    
    # This is the "Magic Line" that isolates only the mathematical behavioral data
    X = df_feat[features].fillna(0)
    
    logging.info(f"Feature Engineering complete. Extracted {len(features)} strict behavioral features.")
    
    # 3. Define Algorithms to Test
    algorithms = {
        "K-Means (k=3)": KMeans(n_clusters=3, random_state=42, n_init=10),
        "Hierarchical (k=3)": AgglomerativeClustering(n_clusters=3, linkage='ward'),
        "DBSCAN": DBSCAN(eps=2.5, min_samples=5) 
    }
    
    results = []
    
    # 4. Execute Benchmarking
    for name, model in algorithms.items():
        logging.info(f"Evaluating {name}...")
        
        # Fit model and get labels
        labels = model.fit_predict(X)
        
        # Check if algorithm found valid clusters
        unique_labels = len(set(labels)) - (1 if -1 in labels else 0)
        
        if unique_labels > 1:
            # Calculate Academic Metrics
            sil = silhouette_score(X, labels)
            ch_score = calinski_harabasz_score(X, labels)
            db_score = davies_bouldin_score(X, labels)
        else:
            sil, ch_score, db_score = "Failed", "Failed", "Failed"
            
        # Count outliers (specifically for DBSCAN)
        outliers = list(labels).count(-1)
        
        results.append({
            "Algorithm": name,
            "Clusters Found": unique_labels,
            "Noise/Outliers Ignored": outliers,
            "Silhouette Score (Higher = Better)": sil if isinstance(sil, str) else round(sil, 4),
            "Calinski-Harabasz (Higher = Better)": ch_score if isinstance(ch_score, str) else round(ch_score, 2),
            "Davies-Bouldin (Lower = Better)": db_score if isinstance(db_score, str) else round(db_score, 4)
        })

    # 5. Generate Report
    report_df = pd.DataFrame(results)
    
    print("\n" + "="*80)
    print("🎓 ALGORITHMIC VALIDATION REPORT FOR RESEARCH PAPER")
    print("="*80)
    print(report_df.to_string(index=False))
    print("="*80 + "\n")
    
    # Save to CSV for your records
    report_df.to_csv("algorithmic_validation_report.csv", index=False)
    logging.info("Saved complete report to 'algorithmic_validation_report.csv'")

if __name__ == "__main__":
    # Point directly to the dataset you uploaded
    DATASET_PATH = "C:\\Users\\anman\\Desktop\\final project\\Student-Success-System\\student-profiling-system\\data\\interim\\cleaned_data.csv" 
    
    try:
        run_algorithmic_benchmark(DATASET_PATH)
    except FileNotFoundError:
        print(f"\n[ERROR] Could not find dataset at '{DATASET_PATH}'.")
        print("Please ensure 'cleaned_data_New.csv' is in the same folder as this script.")