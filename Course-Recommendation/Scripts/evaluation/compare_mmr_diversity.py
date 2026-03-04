# compare_mmr_diversity.py
"""
Compare recommendation metrics with and without MMR diversity re-ranking.
Tests diversity_lambda = 0.0 (baseline) vs 0.05 (diversity-aware)
"""

import numpy as np
import pandas as pd
from hybrid_infer import recommend
from sklearn.metrics import ndcg_score
import matplotlib.pyplot as plt

def precision_at_k(recommended, actual, k=10):
    rec_k = set(recommended[:k])
    actual_set = set(actual)
    if len(actual_set) == 0:
        return 0.0
    return len(rec_k & actual_set) / k

def recall_at_k(recommended, actual, k=10):
    rec_k = set(recommended[:k])
    actual_set = set(actual)
    if len(actual_set) == 0:
        return 0.0
    return len(rec_k & actual_set) / len(actual_set)

def ndcg_at_k(recommended, actual, k=10):
    rec_k = recommended[:k]
    y_true = [1 if c in actual else 0 for c in rec_k]
    if sum(y_true) == 0:
        return 0.0
    y_score = list(range(k, 0, -1))
    return ndcg_score([y_true], [y_score])

def compute_diversity(course_ids, tfidf, df):
    """Compute average pairwise cosine distance among recommended courses"""
    from sklearn.metrics.pairwise import cosine_similarity
    if len(course_ids) < 2:
        return 0.0
    
    vectors = []
    for cid in course_ids:
        row = df[df['course_id'] == cid]
        if not row.empty:
            course_text = row['course_text'].iloc[0]
            vec = tfidf.transform([course_text]).toarray().ravel()
            if np.linalg.norm(vec) > 0:
                vec = vec / np.linalg.norm(vec)
            vectors.append(vec)
    
    if len(vectors) < 2:
        return 0.0
    
    # Compute average pairwise distance (1 - similarity)
    vectors = np.array(vectors)
    sim_matrix = cosine_similarity(vectors)
    # Get upper triangle (pairwise similarities)
    n = len(vectors)
    sims = []
    for i in range(n):
        for j in range(i+1, n):
            sims.append(sim_matrix[i, j])
    
    avg_sim = np.mean(sims) if sims else 0.0
    diversity = 1.0 - avg_sim
    return diversity

def main():
    # Load dataset
    df = pd.read_csv("dataset_processed_for_modeling.csv")
    import joblib
    tfidf = joblib.load("tfidf_course.pkl")
    
    # Sample 50 students for faster comparison
    student_ids = df['student_id'].unique()
    np.random.seed(42)
    sample_students = np.random.choice(student_ids, size=min(50, len(student_ids)), replace=False)
    
    print("Comparing MMR diversity impact...")
    print("=" * 60)
    
    results_baseline = []  # diversity_lambda = 0.0
    results_mmr = []       # diversity_lambda = 0.05
    
    for student_id in sample_students:
        # Get actual courses (use final_grade >= 50 as "passed")
        actual_courses = df[(df['student_id'] == student_id) & (df['final_grade'] >= 50)]['course_id'].unique().tolist()
        
        if len(actual_courses) == 0:
            continue
        
        # Baseline (no MMR diversity)
        try:
            recs_baseline = recommend(student_id, top_n=10, explain=False, diversity_lambda=0.0)
            rec_ids_baseline = recs_baseline['course_id'].tolist()
            
            p_baseline = precision_at_k(rec_ids_baseline, actual_courses, k=10)
            r_baseline = recall_at_k(rec_ids_baseline, actual_courses, k=10)
            n_baseline = ndcg_at_k(rec_ids_baseline, actual_courses, k=10)
            d_baseline = compute_diversity(rec_ids_baseline, tfidf, df)
            
            results_baseline.append({
                'student_id': student_id,
                'precision': p_baseline,
                'recall': r_baseline,
                'ndcg': n_baseline,
                'diversity': d_baseline
            })
        except Exception as e:
            print(f"Error processing {student_id} (baseline): {e}")
            continue
        
        # With MMR diversity
        try:
            recs_mmr = recommend(student_id, top_n=10, explain=False, diversity_lambda=0.05)
            rec_ids_mmr = recs_mmr['course_id'].tolist()
            
            p_mmr = precision_at_k(rec_ids_mmr, actual_courses, k=10)
            r_mmr = recall_at_k(rec_ids_mmr, actual_courses, k=10)
            n_mmr = ndcg_at_k(rec_ids_mmr, actual_courses, k=10)
            d_mmr = compute_diversity(rec_ids_mmr, tfidf, df)
            
            results_mmr.append({
                'student_id': student_id,
                'precision': p_mmr,
                'recall': r_mmr,
                'ndcg': n_mmr,
                'diversity': d_mmr
            })
            
            print(f"Processed {student_id}: Diversity {d_baseline:.3f} → {d_mmr:.3f}")
        except Exception as e:
            print(f"Error processing {student_id} (MMR): {e}")
            continue
    
    # Aggregate metrics
    df_baseline = pd.DataFrame(results_baseline)
    df_mmr = pd.DataFrame(results_mmr)
    
    print("\n" + "=" * 60)
    print("BASELINE (diversity_lambda=0.0):")
    print(f"  Precision@10:  {df_baseline['precision'].mean():.4f}")
    print(f"  Recall@10:     {df_baseline['recall'].mean():.4f}")
    print(f"  NDCG@10:       {df_baseline['ndcg'].mean():.4f}")
    print(f"  Diversity:     {df_baseline['diversity'].mean():.4f}")
    
    print("\nMMR (diversity_lambda=0.05):")
    print(f"  Precision@10:  {df_mmr['precision'].mean():.4f}")
    print(f"  Recall@10:     {df_mmr['recall'].mean():.4f}")
    print(f"  NDCG@10:       {df_mmr['ndcg'].mean():.4f}")
    print(f"  Diversity:     {df_mmr['diversity'].mean():.4f}")
    
    print("\n" + "=" * 60)
    print("IMPROVEMENT (MMR vs Baseline):")
    print(f"  Precision:  {((df_mmr['precision'].mean() / df_baseline['precision'].mean() - 1) * 100):.2f}%")
    print(f"  Recall:     {((df_mmr['recall'].mean() / df_baseline['recall'].mean() - 1) * 100):.2f}%")
    print(f"  NDCG:       {((df_mmr['ndcg'].mean() / df_baseline['ndcg'].mean() - 1) * 100):.2f}%")
    print(f"  Diversity:  {((df_mmr['diversity'].mean() / df_baseline['diversity'].mean() - 1) * 100):.2f}%")
    
    # Plot comparison
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    metrics = ['precision', 'recall', 'ndcg', 'diversity']
    titles = ['Precision@10', 'Recall@10', 'NDCG@10', 'Diversity']
    
    for idx, (metric, title) in enumerate(zip(metrics, titles)):
        ax = axes[idx // 2, idx % 2]
        
        baseline_vals = df_baseline[metric].values
        mmr_vals = df_mmr[metric].values
        
        x = np.arange(len(baseline_vals))
        width = 0.35
        
        ax.bar(x - width/2, baseline_vals, width, label='Baseline (λ=0.0)', alpha=0.8)
        ax.bar(x + width/2, mmr_vals, width, label='MMR (λ=0.05)', alpha=0.8)
        
        ax.set_ylabel(title)
        ax.set_xlabel('Student Index')
        ax.set_title(f'{title} Comparison')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('mmr_diversity_comparison.png', dpi=150, bbox_inches='tight')
    print("\n✅ Saved plot: mmr_diversity_comparison.png")

if __name__ == "__main__":
    main()
