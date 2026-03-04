#!/usr/bin/env python3
"""
train_cf.py

Lightweight collaborative filtering using TruncatedSVD on a user-item (student-course) matrix.
No compiled dependencies beyond scipy/sklearn. Good fallback to Surprise's SVD.

Outputs:
 - svd_factors_student.npy
 - svd_factors_course.npy
 - cf_course_ids.npy (order of course columns)
 - cf_student_ids.npy (order of student rows)
 - cf_recommendations_sample.csv
"""

import os
import numpy as np
import pandas as pd
import joblib
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import math

# CONFIG - ORGANIZED VERSION
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_CSV = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
MODELS_DIR = os.path.join(BASE_DIR, "Models")
N_FACTORS = 60
TOP_N = 10
OUTPUT_PREFIX = "cf_alt_"

def load_df(path=PROCESSED_CSV):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed CSV not found: {path}")
    return pd.read_csv(path)

def build_matrix(df, user_col='student_id', item_col='course_id', rating_col='final_grade'):
    # encode ids to indices
    user_enc = LabelEncoder()
    item_enc = LabelEncoder()
    users = user_enc.fit_transform(df[user_col])
    items = item_enc.fit_transform(df[item_col])
    ratings = df[rating_col].astype(float).values

    n_users = users.max() + 1
    n_items = items.max() + 1
    print(f"Building sparse matrix: users={n_users}, items={n_items}, ratings={len(ratings)}")
    mat = csr_matrix((ratings, (users, items)), shape=(n_users, n_items))
    return mat, user_enc, item_enc

def train_truncated_svd(mat, n_factors=N_FACTORS):
    # We factorize the matrix into U (n_users x k) and Sigma*Vt (k x n_items)
    # sklearn TruncatedSVD returns components_ shape (k, n_items)
    print("Training TruncatedSVD (this approximates SVD on the sparse matrix)...")
    svd = TruncatedSVD(n_components=n_factors, random_state=42)
    user_factors = svd.fit_transform(mat)           # shape (n_users, k)
    item_factors = svd.components_.T                # shape (n_items, k)
    # note: svd.singular_values_ approximates sigma diag
    print("TruncatedSVD done. Explained variance (sum):", svd.explained_variance_ratio_.sum())
    return user_factors, item_factors, svd

def predict_all(user_factors, item_factors):
    # predicted rating matrix = user_factors dot item_factors.T
    return np.dot(user_factors, item_factors.T)

def rmse_on_known(mat, preds):
    # compute RMSE only on observed entries
    coo = mat.tocoo()
    true = coo.data
    pred = preds[coo.row, coo.col]
    return math.sqrt(mean_squared_error(true, pred))

def recommend_for_user_idx(user_idx, preds_matrix, item_ids, known_items_set, top_n=TOP_N):
    # preds_matrix: (n_users, n_items)
    row = preds_matrix[user_idx]
    # set scores for already-known items to -inf so they are not recommended
    row_masked = row.copy()
    for it in known_items_set:
        row_masked[it] = -np.inf
    top_idx = np.argpartition(-row_masked, range(top_n))[:top_n]
    top_idx = top_idx[np.argsort(-row_masked[top_idx])]
    recommended_item_ids = [item_ids[i] for i in top_idx]
    scores = [float(row[i]) for i in top_idx]
    return list(zip(recommended_item_ids, scores))

def main():
    df = load_df()
    # Build matrix
    mat, user_enc, item_enc = build_matrix(df)
    # Train factorization
    user_factors, item_factors, svd_model = train_truncated_svd(mat, n_factors=N_FACTORS)
    # Predict all
    preds = predict_all(user_factors, item_factors)
    # Evaluate RMSE on known entries
    rmse = rmse_on_known(mat, preds)
    print(f"RMSE on observed ratings (approx): {rmse:.4f}")

    # Save artifacts
    os.makedirs(MODELS_DIR, exist_ok=True)
    np.save(os.path.join(MODELS_DIR, OUTPUT_PREFIX + "student_factors.npy"), user_factors)
    np.save(os.path.join(MODELS_DIR, OUTPUT_PREFIX + "course_factors.npy"), item_factors)
    np.save(os.path.join(MODELS_DIR, OUTPUT_PREFIX + "course_ids.npy"), item_enc.inverse_transform(np.arange(item_factors.shape[0])))
    np.save(os.path.join(MODELS_DIR, OUTPUT_PREFIX + "student_ids.npy"), user_enc.inverse_transform(np.arange(user_factors.shape[0])))
    joblib.dump(svd_model, os.path.join(MODELS_DIR, OUTPUT_PREFIX + "svd_model.pkl"))
    joblib.dump(user_enc, os.path.join(MODELS_DIR, OUTPUT_PREFIX + "user_encoder.pkl"))
    joblib.dump(item_enc, os.path.join(MODELS_DIR, OUTPUT_PREFIX + "item_encoder.pkl"))
    print("Saved CF artifacts with prefix:", OUTPUT_PREFIX)

    # produce sample recommendations for 10 random students
    n_users = user_factors.shape[0]
    user_indices = np.random.choice(n_users, size=min(10, n_users), replace=False)
    all_item_ids = np.load(os.path.join(MODELS_DIR, OUTPUT_PREFIX + "course_ids.npy"), allow_pickle=True)
    # build known items per user to avoid recommending already-seen courses
    known_by_user = {}
    for uid_idx, uid in enumerate(user_enc.inverse_transform(np.arange(n_users))):
        known_by_user[uid_idx] = set(item_enc.transform(df[df['student_id']==uid]['course_id'].tolist()))

    all_recs_rows = []
    for uidx in user_indices:
        uid = user_enc.inverse_transform([uidx])[0]
        recs = recommend_for_user_idx(uidx, preds, all_item_ids, known_by_user.get(uidx, set()), top_n=TOP_N)
        for cid, score in recs:
            cname = df[df['course_id']==cid]['course_name'].iloc[0] if 'course_name' in df.columns else cid
            all_recs_rows.append({
                "student_id": uid,
                "course_id": cid,
                "course_name": cname,
                "pred_rating": round(float(score), 4)
            })
    recs_df = pd.DataFrame(all_recs_rows)
    output_csv = os.path.join(BASE_DIR, "cf_alt_recommendations_sample.csv")
    recs_df.to_csv(output_csv, index=False)
    print(f"Saved sample CF recommendations to {output_csv}")
    print(recs_df.head())

if __name__ == "__main__":
    main()
