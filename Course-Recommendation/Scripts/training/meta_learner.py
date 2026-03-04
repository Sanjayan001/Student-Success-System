#!/usr/bin/env python3
"""
meta_learner.py
Train a meta-learner to combine CF/CBF/Success/Job/Risk features into a single relevance score.

Approach:
- For each student with history, build a TF-IDF interest profile.
- For each course that student actually took (enrolled rows), compute features:
    cf_score, cbf_score, p_success, job_market, risk
- Label y = 1 if final_grade >= 60 else 0 (proxy for relevance/success).
- Train a logistic regression classifier (fast and interpretable).
- Save model (Models/meta_learner.pkl) and linear weights (Models/meta_learner_weights.pkl).

Run:
    python Scripts/training/meta_learner.py
"""
import os
import sys
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score

# Resolve project root and add utils to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UTILS_DIR = os.path.join(BASE_DIR, "Scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from hybrid_infer import load_artifacts, build_student_profile, compute_p_success

# Output paths
OUT_MODEL = os.path.join(BASE_DIR, "Models", "meta_learner.pkl")
OUT_WEIGHTS = os.path.join(BASE_DIR, "Models", "meta_learner_weights.pkl")


def get_cf_score_for(sid, cid, student_ids, student_factors, course_factors, course_ids):
    # Return normalized CF score if both ids available
    try:
        # Find indices
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
    # Precompute course attribute maps
    course_rows = df.drop_duplicates("course_id").set_index("course_id")
    course_text_map = course_rows.get("course_text", pd.Series(index=course_rows.index)).to_dict()
    job_market_map = course_rows.get("job_market_demand_2035", pd.Series(0, index=course_rows.index)).to_dict()
    course_diff_map = course_rows.get("course_difficulty", pd.Series(0.5, index=course_rows.index)).to_dict()

    X_rows = []
    y_rows = []

    students = df['student_id'].drop_duplicates().tolist()
    # Limit runtime on large datasets
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

        # For each course the student took, compute features
        for _, row in student_rows.iterrows():
            cid = row['course_id']
            # CF
            cf_score = get_cf_score_for(sid, cid, student_ids, student_factors, course_factors, course_ids)
            # CBF
            course_text = course_text_map.get(cid, '')
            course_vec = tfidf.transform([course_text]).toarray()[0]
            if np.linalg.norm(course_vec) > 0:
                cbf_sim = cosine_similarity(stud_prof.reshape(1, -1), course_vec.reshape(1, -1)).flatten()[0]
                cbf_score = (cbf_sim + 1) / 2.0
            else:
                cbf_score = 0.0
            # Success probability
            course_row = {
                'course_difficulty': float(course_diff_map.get(cid, 0.5)),
                'job_market_demand_2035': float(job_market_map.get(cid, 0.0)),
            }
            p_success = compute_p_success(clf_success, scaler_success, student_ref, course_row)
            # Job market demand
            job = float(job_market_map.get(cid, 0.0))

            X_rows.append([cf_score, cbf_score, p_success, job, risk])
            y_rows.append(1 if float(row.get('final_grade', np.nan)) >= 60 else 0)

    return np.array(X_rows, dtype=float), np.array(y_rows, dtype=int)


def main():
    print("Loading artifacts...")
    df, tfidf, course_index_map, student_factors, course_factors, student_ids, course_ids, clf, scaler, _meta_model, _meta_weights = load_artifacts()

    print("Building training dataset...")
    X, y = build_training_rows(df, tfidf, course_index_map, student_factors, course_factors,
                               student_ids, course_ids, clf, scaler)
    if X.size == 0:
        print("No training data. Check dataset and artifacts.")
        return

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training logistic regression meta-learner...")
    clf_meta = LogisticRegression(max_iter=1000, class_weight='balanced')
    clf_meta.fit(X_train, y_train)

    proba = clf_meta.predict_proba(X_val)[:, 1]
    preds = (proba >= 0.5).astype(int)
    auc = roc_auc_score(y_val, proba)
    acc = accuracy_score(y_val, preds)
    prec = precision_score(y_val, preds)
    rec = recall_score(y_val, preds)

    print(f"Meta-Learner AUC: {auc:.4f}")
    print(f"Acc: {acc:.4f} Prec: {prec:.4f} Rec: {rec:.4f}")

    # Save model
    joblib.dump(clf_meta, OUT_MODEL)
    print(f"Saved meta-learner model to {OUT_MODEL}")

    # Save linear weights for fallback use
    try:
        coef = clf_meta.coef_[0]
        intercept = float(clf_meta.intercept_[0])
        joblib.dump({"coef": coef, "intercept": intercept, "features": ["cf","cbf","p_success","job","risk"]}, OUT_WEIGHTS)
        print(f"Saved meta-learner weights to {OUT_WEIGHTS}")
    except Exception:
        pass


if __name__ == "__main__":
    main()
