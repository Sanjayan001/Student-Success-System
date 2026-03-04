#!/usr/bin/env python3
"""
meta_learner_deep.py
Train a deep learning (MLP) meta-learner to fuse CF/CBF/Success/Job/Risk features.

Approach:
- Same training data as LogisticRegression meta-learner.
- MLP with 2-3 hidden layers + dropout.
- Compare AUC/Acc vs LogisticRegression baseline.
- Save best model and weights.

Run:
    python Scripts/training/meta_learner_deep.py
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UTILS_DIR = os.path.join(BASE_DIR, "Scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from hybrid_infer import load_artifacts, build_student_profile, compute_p_success

DF_PATH = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
OUT_MODEL = os.path.join(BASE_DIR, "Models", "meta_learner_deep.pkl")
OUT_SCALER = os.path.join(BASE_DIR, "Models", "meta_learner_deep_scaler.pkl")


def get_cf_score_for(sid, cid, student_ids, student_factors, course_factors, course_ids):
    """Compute normalized CF score."""
    try:
        u_idx = int(np.where(student_ids == sid)[0][0])
        c_idx = int(np.where(course_ids == cid)[0][0])
    except Exception:
        return 0.0
    user_vec = student_factors[u_idx]
    course_vec = course_factors[c_idx]
    pred = float(np.dot(user_vec, course_vec))
    preds = np.dot(user_vec, course_factors.T)
    minp, maxp = preds.min(), preds.max()
    norm = (pred - minp) / (maxp - minp + 1e-9)
    return float(norm)


def build_training_rows(df, tfidf, course_index_map, student_factors, course_factors,
                        student_ids, course_ids, clf_success, scaler_success):
    """Build training data (same as meta_learner.py)."""
    course_rows = df.drop_duplicates("course_id").set_index("course_id")
    course_text_map = course_rows.get("course_text", pd.Series(index=course_rows.index)).to_dict()
    job_market_map = course_rows.get("job_market_demand_2035", pd.Series(0, index=course_rows.index)).to_dict()
    course_diff_map = course_rows.get("course_difficulty", pd.Series(0.5, index=course_rows.index)).to_dict()

    X_rows = []
    y_rows = []

    students = df['student_id'].drop_duplicates().tolist()
    if len(students) > 2000:
        students = list(np.random.RandomState(42).choice(students, size=2000, replace=False))

    for sid in students:
        student_rows = df[df['student_id'] == sid]
        if student_rows.empty:
            continue
        stud_prof = build_student_profile(df, sid, tfidf, course_index_map)
        if stud_prof is None:
            continue
        student_ref = student_rows.iloc[0].to_dict()
        risk = float(student_ref.get('risk_score', 0))

        for _, row in student_rows.iterrows():
            cid = row['course_id']
            cf_score = get_cf_score_for(sid, cid, student_ids, student_factors, course_factors, course_ids)
            course_text = course_text_map.get(cid, '')
            course_vec = tfidf.transform([course_text]).toarray()[0]
            if np.linalg.norm(course_vec) > 0:
                cbf_sim = cosine_similarity(stud_prof.reshape(1, -1), course_vec.reshape(1, -1)).flatten()[0]
                cbf_score = (cbf_sim + 1) / 2.0
            else:
                cbf_score = 0.0
            course_row = {
                'course_difficulty': float(course_diff_map.get(cid, 0.5)),
                'job_market_demand_2035': float(job_market_map.get(cid, 0.0)),
            }
            p_success = compute_p_success(clf_success, scaler_success, student_ref, course_row)
            job = float(job_market_map.get(cid, 0.0))

            X_rows.append([cf_score, cbf_score, p_success, job, risk])
            y_rows.append(1 if float(row.get('final_grade', np.nan)) >= 60 else 0)

    return np.array(X_rows, dtype=float), np.array(y_rows, dtype=int)


def build_model(input_shape=5):
    """Build MLP model for fusion using scikit-learn."""
    model = MLPClassifier(
        hidden_layer_sizes=(64, 32, 16),
        activation='relu',
        solver='adam',
        max_iter=200,
        early_stopping=True,
        validation_fraction=0.1,
        random_state=42,
        verbose=1
    )
    return model


def main():
    print("Loading artifacts...")
    df, tfidf, course_index_map, student_factors, course_factors, student_ids, course_ids, clf, scaler, _, _ = load_artifacts()

    print("Building training dataset...")
    X, y = build_training_rows(df, tfidf, course_index_map, student_factors, course_factors,
                               student_ids, course_ids, clf, scaler)
    if X.size == 0:
        print("No training data. Check dataset and artifacts.")
        return

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Normalize features
    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_val_scaled = scaler_X.transform(X_val)

    print("Training deep learning fusion model...")
    model = build_model(input_shape=5)
    
    # Train
    model.fit(X_train_scaled, y_train)

    # Evaluate on validation set
    proba = model.predict_proba(X_val_scaled)[:, 1]
    preds = model.predict(X_val_scaled)
    auc = roc_auc_score(y_val, proba)
    acc = accuracy_score(y_val, preds)
    prec = precision_score(y_val, preds)
    rec = recall_score(y_val, preds)

    print(f"\n=== DEEP LEARNING META-LEARNER RESULTS ===")
    print(f"AUC: {auc:.4f}")
    print(f"Acc: {acc:.4f} Prec: {prec:.4f} Rec: {rec:.4f}")

    # Save model and scaler
    joblib.dump(model, OUT_MODEL)
    joblib.dump(scaler_X, OUT_SCALER)
    print(f"\nSaved model to {OUT_MODEL}")
    print(f"Saved scaler to {OUT_SCALER}")

    # Compare to LogisticRegression baseline
    print("\n=== COMPARISON TO BASELINE ===")
    print("For reference, LogisticRegression baseline (from meta_learner.py):")
    print("AUC: 0.7362, Acc: 0.6718, Prec: 0.8865, Rec: 0.6723")
    print(f"\nImprovement: AUC +{(auc - 0.7362):.4f} ({(auc - 0.7362) / 0.7362 * 100:.2f}%)")


if __name__ == "__main__":
    main()
