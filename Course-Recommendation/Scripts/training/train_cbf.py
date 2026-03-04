#!/usr/bin/env python3
"""
train_cbf.py
Content-Based Recommender:
- Loads processed dataset and TF-IDF artifacts
- Builds student profile vectors (weighted by final_grade or course_interest)
- Recommends top-N courses using cosine similarity
- Simple Precision@K evaluator (if ground-truth available)
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack

# ----------------- CONFIG -----------------
PROCESSED_CSV = "dataset_processed_for_modeling.csv"
TFIDF_PATH = "tfidf_course.pkl"
COURSE_INDEX_MAP_PATH = "course_index_map.pkl"
SCALER_PATH = "scaler.pkl"

# output
RECS_OUT_CSV = "cbf_recommendations_sample.csv"

# Parameters
TOP_N = 10            # default top N recommendations
WEIGHT_BY = "final_grade"   # "final_grade" or "course_interest" or "previous_GPA"
MIN_COURSES_FOR_PROFILE = 1  # fallback if student has zero history
# ------------------------------------------


def safe_load_artifacts():
    if not os.path.exists(PROCESSED_CSV):
        raise FileNotFoundError(f"Processed CSV not found: {PROCESSED_CSV}")
    if not os.path.exists(TFIDF_PATH):
        raise FileNotFoundError(f"TF-IDF file not found: {TFIDF_PATH}")
    if not os.path.exists(COURSE_INDEX_MAP_PATH):
        raise FileNotFoundError(f"Course index map not found: {COURSE_INDEX_MAP_PATH}")
    print("Loading artifacts...")
    df = pd.read_csv(PROCESSED_CSV)
    tfidf = joblib.load(TFIDF_PATH)
    course_index_map = joblib.load(COURSE_INDEX_MAP_PATH)
    scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None
    print("Loaded dataset rows:", len(df))
    return df, tfidf, course_index_map, scaler


def get_course_tfidf_matrix(tfidf, course_index_map):
    # tfidf is a fitted TfidfVectorizer object; .transform() expects raw text.
    # But preprocess saved only the vectorizer. We need the course_texts used earlier.
    # To avoid re-reading text file, we can reconstruct course_texts from processed CSV.
    # This function assumes the course_text TF-IDF matrix can be rebuilt from course_text column in CSV.
    raise NotImplementedError("We will rebuild the TF-IDF matrix using course_text column in the processed CSV.")


def build_course_matrix_from_df(df, tfidf, course_index_map):
    """
    Build the TF-IDF matrix for unique courses using course_text column from df.
    Returns a scipy sparse matrix (n_courses x n_features) aligned with course_index_map ordering.
    """
    # extract unique course_texts in same order as course_index_map keys
    course_ids = list(course_index_map.keys())
    course_texts = []
    # create mapping to course text; use the first occurrence
    course_text_series = df[['course_id','course_text']].drop_duplicates().set_index('course_id')['course_text'].to_dict()
    for cid in course_ids:
        text = course_text_series.get(cid, "")
        course_texts.append(text)
    course_matrix = tfidf.transform(course_texts)   # sparse matrix
    return course_matrix


def build_student_profile_vector(student_id, df, course_matrix, course_index_map, weight_by="final_grade"):
    """
    Create a student profile vector as weighted average of course vectors they performed well in.
    weight_by: column name used as weight; falls back gracefully if not present.
    """
    rows = df[df['student_id'] == student_id]
    if rows.empty:
        return None  # cold start, caller handles
    # find indices of course vectors
    idxs = []
    weights = []
    for _, r in rows.iterrows():
        cid = r['course_id']
        if cid in course_index_map:
            idxs.append(course_index_map[cid])
            w = r.get(weight_by, np.nan)
            if pd.isna(w):
                w = 1.0
            weights.append(float(w))
    if len(idxs) < MIN_COURSES_FOR_PROFILE:
        return None
    # extract sparse rows
    sub = course_matrix[idxs]
    weights = np.array(weights)
    # if all weights zero, convert to ones
    if weights.sum() == 0:
        weights = np.ones_like(weights)
    weights = weights / weights.sum()
    # weighted average: multiply each row by its weight and sum
    # sparse matrices: convert weights to diagonal multiplication
    # easiest: multiply rows by weights and sum
    weighted = sub.multiply(weights[:, None])
    profile = weighted.sum(axis=0)  # shape (1, n_features) as matrix
    # normalize profile
    prof_array = np.asarray(profile).ravel()
    if np.linalg.norm(prof_array) == 0:
        return prof_array
    prof_array = prof_array / np.linalg.norm(prof_array)
    return prof_array


def recommend_for_student(student_id, df, tfidf, course_index_map, course_matrix, top_n=10,
                          weight_by="final_grade", blend_with_job=False):
    """
    Returns list of (course_id, course_name, similarity_score, optional job_score, optional risk_score)
    """
    prof = build_student_profile_vector(student_id, df, course_matrix, course_index_map, weight_by=weight_by)
    # Cold-start: if student has no history, fallback to population-average profile
    if prof is None:
        print(f"Student {student_id} cold-start: using average profile.")
        # build population average from all students' profiles
        # naive: average of all course vectors weighted by average final_grade
        avg_weights = df.groupby('course_id')['final_grade'].mean().to_dict()
        idxs = []
        weights = []
        for cid, idx in course_index_map.items():
            idxs.append(idx)
            weights.append(avg_weights.get(cid, 1.0))
        sub = course_matrix[idxs]
        weights = np.array(weights)
        weights = weights / weights.sum()
        weighted = sub.multiply(weights[:, None])
        profile = weighted.sum(axis=0)
        prof = np.asarray(profile).ravel()
        if np.linalg.norm(prof) != 0:
            prof = prof / np.linalg.norm(prof)

    # compute cosine similarity between profile and all course vectors
    # course_matrix is sparse (n_courses x n_features)
    sims = cosine_similarity(prof.reshape(1, -1), course_matrix).flatten()  # shape (n_courses,)
    # optionally blend job demand and risk (simple rule)
    # create mapping index -> course_id
    inv_map = {v: k for k, v in course_index_map.items()}
    rows = []
    for idx, sim in enumerate(sims):
        cid = inv_map[idx]
        # pull job demand and (optionally) other metadata from df (first occurrence)
        rows_df = df[df['course_id'] == cid]
        if rows_df.empty:
            jobd = np.nan
            cname = cid
        else:
            jobd = float(rows_df['job_market_demand_2035'].iloc[0]) if 'job_market_demand_2035' in rows_df.columns else np.nan
            cname = rows_df['course_name'].iloc[0] if 'course_name' in rows_df.columns else cid
        rows.append((cid, cname, float(sim), jobd))
    # convert to DataFrame for easy sorting
    recs_df = pd.DataFrame(rows, columns=['course_id', 'course_name', 'cbf_score', 'job_demand'])
    # normalize cbf_score 0-1
    recs_df['cbf_score'] = (recs_df['cbf_score'] - recs_df['cbf_score'].min()) / (recs_df['cbf_score'].max() - recs_df['cbf_score'].min() + 1e-9)
    # if blending with job demand:
    if blend_with_job:
        recs_df['job_demand_norm'] = recs_df['job_demand'].fillna(recs_df['job_demand'].mean())
        recs_df['final_score'] = 0.7 * recs_df['cbf_score'] + 0.3 * recs_df['job_demand_norm']
    else:
        recs_df['final_score'] = recs_df['cbf_score']
    recs_df = recs_df.sort_values('final_score', ascending=False).reset_index(drop=True)
    top = recs_df.head(top_n)
    return top


def precision_at_k(recs_df, df, student_id, k=5):
    """
    Simple Precision@K: if dataset contains a 'recommended' boolean for real positive labels (or final_grade >= threshold)
    We treat recommended==True as positive ground truth. If not available, use final_grade >= 60 as proxy.
    """
    if 'recommended' in df.columns:
        truth = df[(df['student_id'] == student_id) & (df['recommended'] == True)]['course_id'].unique().tolist()
    else:
        # proxy: courses where final_grade >= 60 for that student
        truth = df[(df['student_id'] == student_id) & (df['final_grade'] >= 60)]['course_id'].unique().tolist()
    preds = recs_df['course_id'].tolist()[:k]
    if len(truth) == 0:
        return None  # cannot compute
    hits = sum([1 for p in preds if p in truth])
    return hits / k


def batch_recommend_and_save(sample_student_ids, df, tfidf, course_index_map, course_matrix, out_csv=RECS_OUT_CSV, top_n=10):
    all_recs = []
    for sid in sample_student_ids:
        recs = recommend_for_student(sid, df, tfidf, course_index_map, course_matrix, top_n=top_n, weight_by=WEIGHT_BY)
        for _, r in recs.iterrows():
            all_recs.append({
                'student_id': sid,
                'course_id': r['course_id'],
                'course_name': r['course_name'],
                'cbf_score': r['cbf_score'],
                'job_demand': r['job_demand'],
                'final_score': r['final_score']
            })
    out_df = pd.DataFrame(all_recs)
    out_df.to_csv(out_csv, index=False)
    print(f"Saved batch recommendations to {out_csv}")
    return out_df


def main():
    df, tfidf, course_index_map, scaler = safe_load_artifacts()
    # build course_matrix from df (course_text column) and tfidf vectorizer
    course_matrix = build_course_matrix_from_df(df, tfidf, course_index_map)
    print("Course matrix shape:", course_matrix.shape)

    # Quick sanity check for a sample student
    sample_students = df['student_id'].drop_duplicates().sample(n=10, random_state=42).tolist()
    print("Sample students:", sample_students)

    # show recommendations for the first sample
    sid0 = sample_students[0]
    print(f"\nTop {TOP_N} recommendations for student {sid0}:")
    recs = recommend_for_student(sid0, df, tfidf, course_index_map, course_matrix, top_n=TOP_N, weight_by=WEIGHT_BY, blend_with_job=True)
    print(recs[['course_id','course_name','final_score','cbf_score','job_demand']])

    # Evaluate precision@5 for sample students (where possible)
    print("\nEvaluating Precision@5 (proxy using final_grade>=60 or recommended flag):")
    prec_list = []
    for s in sample_students:
        recs_s = recommend_for_student(s, df, tfidf, course_index_map, course_matrix, top_n=TOP_N, weight_by=WEIGHT_BY, blend_with_job=False)
        p = precision_at_k(recs_s, df, s, k=5)
        prec_list.append((s, p))
    for s, p in prec_list:
        print(f"Student {s}: Precision@5 = {p}")

    # Save batch recommendations for sample students
    batch_recommend_and_save(sample_students, df, tfidf, course_index_map, course_matrix, out_csv=RECS_OUT_CSV, top_n=TOP_N)


if __name__ == "__main__":
    main()
