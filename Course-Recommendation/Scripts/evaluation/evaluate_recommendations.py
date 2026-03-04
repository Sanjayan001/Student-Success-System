#!/usr/bin/env python3
"""
evaluate_recommendations.py
Compute recommendation quality metrics (Precision@K, Recall@K, NDCG@K, Coverage, Diversity)
for a sample of students using the hybrid recommendation engine.

Run:
    python evaluate_recommendations.py

Outputs:
    - Prints aggregate metrics
    - Saves recommendation_quality_metrics.png
"""

import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

# Resolve project root and paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DF_PATH = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
UTILS_DIR = os.path.join(BASE_DIR, "Scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)
K = 10
SAMPLE_STUDENTS = 100


def precision_at_k(recommended, relevant, k=K):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    return len(set(recommended_k) & relevant_set) / max(k, 1)


def recall_at_k(recommended, relevant, k=K):
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    return len(set(recommended_k) & relevant_set) / max(len(relevant_set), 1)


def ndcg_at_k(recommended, relevant, k=K):
    relevance = [1 if item in relevant else 0 for item in recommended[:k]]
    dcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(relevance))
    ideal_relevance = sorted(relevance, reverse=True)
    idcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(ideal_relevance))
    return (dcg / idcg) if idcg > 0 else 0.0


def compute_coverage(all_recommendations, all_courses):
    recommended_courses = set()
    for recs in all_recommendations:
        recommended_courses.update(recs)
    return len(recommended_courses) / max(len(all_courses), 1)


def diversity_for_recs(recs, course_texts):
    # Use simple text TF-IDF cosine as proxy; fall back to 0 if not enough vectors
    vecs = []
    for cid in recs:
        txt = course_texts.get(cid)
        if txt is not None:
            vecs.append(txt)
    if len(vecs) < 2:
        return 0.0
    # naive bag-of-words using character-level counts as quick proxy
    # (to avoid loading heavy models here)
    # Convert to frequency vectors of characters a-z
    def text_to_vec(t):
        arr = np.zeros(26)
        for ch in t.lower():
            if 'a' <= ch <= 'z':
                arr[ord(ch) - ord('a')] += 1
        if arr.sum() > 0:
            arr = arr / arr.sum()
        return arr
    mats = np.stack([text_to_vec(t) for t in vecs])
    sims = cosine_similarity(mats)
    n = sims.shape[0]
    upper = []
    for i in range(n):
        for j in range(i + 1, n):
            upper.append(sims[i, j])
    avg_sim = float(np.mean(upper)) if upper else 0.0
    return 1.0 - avg_sim


def main():
    from hybrid_infer import recommend

    print("Loading dataset...")
    df = pd.read_csv(DF_PATH)
    students = df['student_id'].unique()[:SAMPLE_STUDENTS]
    all_courses = df['course_id'].unique().tolist()
    course_texts = df.drop_duplicates('course_id').set_index('course_id')['course_text'].to_dict()

    precisions, recalls, ndcgs, diversities = [], [], [], []
    all_recs_list = []

    for sid in students:
        # Relevant courses = courses student passed (grade >= 60)
        student_rows = df[df['student_id'] == sid]
        relevant = student_rows[student_rows['final_grade'] >= 60]['course_id'].tolist()
        if not relevant:
            continue
        # Get recommendations without explanations for speed
        out = recommend(sid, top_n=K, job_priority="Balanced", explain=False, scoring_mode="auto")
        recommended = out['course_id'].tolist()
        all_recs_list.append(recommended)

        precisions.append(precision_at_k(recommended, relevant))
        recalls.append(recall_at_k(recommended, relevant))
        ndcgs.append(ndcg_at_k(recommended, relevant))
        diversities.append(diversity_for_recs(recommended, course_texts))
        print(f"Processed {sid}: P@{K}={precisions[-1]:.3f} R@{K}={recalls[-1]:.3f} NDCG@{K}={ndcgs[-1]:.3f}")

    coverage = compute_coverage(all_recs_list, all_courses)

    print("\n=== AGGREGATE METRICS ===")
    def safe_mean(arr):
        return float(np.mean(arr)) if arr else 0.0
    print(f"Precision@{K}: {safe_mean(precisions):.4f}")
    print(f"Recall@{K}:    {safe_mean(recalls):.4f}")
    print(f"NDCG@{K}:      {safe_mean(ndcgs):.4f}")
    print(f"Coverage:      {coverage:.4f}")
    print(f"Diversity:     {safe_mean(diversities):.4f}")

    # Simple bar plot
    labels = [f"P@{K}", f"R@{K}", f"NDCG@{K}", "Coverage", "Diversity"]
    values = [safe_mean(precisions), safe_mean(recalls), safe_mean(ndcgs), coverage, safe_mean(diversities)]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['#4E79A7', '#59A14F', '#F28E2B', '#E15759', '#76B7B2'])
    plt.ylim(0, 1)
    plt.title("Recommendation Quality Metrics (Hybrid)")
    plt.tight_layout()
    plt.savefig("recommendation_quality_metrics.png", dpi=300)
    print("\n✅ Saved plot: recommendation_quality_metrics.png")


if __name__ == "__main__":
    main()
