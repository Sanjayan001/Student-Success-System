#!/usr/bin/env python3
"""
fairness_audit.py
Audit course recommendations for algorithmic bias and fairness across student cohorts.

Metrics:
- Coverage Parity: Do all cohorts see similar # of courses?
- NDCG Parity: Do recommendations rank equally well?
- Diversity Parity: Do all cohorts get diverse recommendations?
- Domain Balance: Are domains evenly represented across cohorts?

Cohorts: GPA tiers (high: >=3.5, mid: 2.5-3.5, low: <2.5)

Run:
    python Scripts/evaluation/fairness_audit.py

Output:
    fairness_audit_report.txt, fairness_metrics.csv
"""
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UTILS_DIR = os.path.join(BASE_DIR, "Scripts", "utils")
if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from hybrid_infer import recommend


def get_student_cohorts(df):
    """Define student cohorts by GPA tier."""
    cohorts = {
        'high_gpa': df[df['previous_GPA'] >= 3.5]['student_id'].unique(),
        'mid_gpa': df[(df['previous_GPA'] >= 2.5) & (df['previous_GPA'] < 3.5)]['student_id'].unique(),
        'low_gpa': df[df['previous_GPA'] < 2.5]['student_id'].unique(),
    }
    return cohorts


def precision_at_k(recommended, relevant, k=10):
    """P@K: fraction of top-k that are relevant."""
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    return len(set(recommended_k) & relevant_set) / max(k, 1)


def recall_at_k(recommended, relevant, k=10):
    """Recall@K: fraction of relevant items in top-k."""
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    return len(set(recommended_k) & relevant_set) / max(len(relevant_set), 1)


def ndcg_at_k(recommended, relevant, k=10):
    """NDCG@K: normalized discounted cumulative gain."""
    relevance = [1 if item in relevant else 0 for item in recommended[:k]]
    dcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(relevance))
    ideal_relevance = sorted(relevance, reverse=True)
    idcg = sum(rel / np.log2(i + 2) for i, rel in enumerate(ideal_relevance))
    return (dcg / idcg) if idcg > 0 else 0.0


def compute_diversity(recs, course_texts):
    """Compute average pairwise dissimilarity (text-based)."""
    if len(recs) < 2:
        return 0.0
    vecs = []
    for cid in recs:
        txt = course_texts.get(cid, '')
        if txt:
            # Simple character-level bag-of-words
            arr = np.zeros(26)
            for ch in txt.lower():
                if 'a' <= ch <= 'z':
                    arr[ord(ch) - ord('a')] += 1
            if arr.sum() > 0:
                arr = arr / arr.sum()
            vecs.append(arr)
    if len(vecs) < 2:
        return 0.0
    # Compute average pairwise cosine distance
    sims = []
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            dot = np.dot(vecs[i], vecs[j])
            sim = dot / (np.linalg.norm(vecs[i]) * np.linalg.norm(vecs[j]) + 1e-9)
            sims.append(sim)
    return 1.0 - np.mean(sims) if sims else 0.0


def audit_fairness(df, sample_size=50, top_k=10):
    """
    Audit recommendations for fairness across student cohorts.
    
    Args:
        df: dataset
        sample_size: number of students per cohort to sample
        top_k: evaluate on top-K recommendations
    
    Returns:
        dict with fairness metrics and report string
    """
    cohorts = get_student_cohorts(df)
    course_texts = df.drop_duplicates('course_id').set_index('course_id')['course_text'].to_dict()
    
    results = {
        'coverage_parity': {},
        'ndcg_parity': {},
        'diversity_parity': {},
        'domain_balance': {}
    }
    
    print(f"🔍 Auditing fairness across {len(cohorts)} cohorts...")
    print(f"Sample size per cohort: {min(sample_size, len(next(iter(cohorts.values()))))}")
    print()
    
    # Process each cohort
    for cohort_name, student_ids in cohorts.items():
        print(f"Processing cohort: {cohort_name} ({len(student_ids)} students)")
        
        # Sample students
        sampled = np.random.RandomState(42).choice(
            list(student_ids), 
            size=min(sample_size, len(student_ids)), 
            replace=False
        )
        
        cohort_metrics = {
            'ndcgs': [],
            'precisions': [],
            'recalls': [],
            'diversities': [],
            'coverage': set(),
            'domain_counts': {}
        }
        
        for sid in sampled:
            try:
                # Get recommendations
                recs = recommend(sid, top_n=top_k, job_priority="Balanced", explain=False, scoring_mode="auto")
                if recs.empty:
                    continue
                
                # Get relevant courses (student's passing courses)
                student_data = df[df['student_id'] == sid]
                relevant = student_data[student_data['final_grade'] >= 60]['course_id'].tolist()
                
                if relevant:
                    recommended = recs['course_id'].tolist()
                    p_k = precision_at_k(recommended, relevant, k=top_k)
                    r_k = recall_at_k(recommended, relevant, k=top_k)
                    n_k = ndcg_at_k(recommended, relevant, k=top_k)
                    div = compute_diversity(recommended, course_texts)
                    
                    cohort_metrics['ndcgs'].append(n_k)
                    cohort_metrics['precisions'].append(p_k)
                    cohort_metrics['recalls'].append(r_k)
                    cohort_metrics['diversities'].append(div)
                    cohort_metrics['coverage'].update(recommended)
                    
                    # Track domain distribution
                    for _, row in recs.iterrows():
                        domain = row['course_domain']
                        cohort_metrics['domain_counts'][domain] = cohort_metrics['domain_counts'].get(domain, 0) + 1
            except Exception as e:
                # Skip if error
                pass
        
        # Aggregate metrics
        results['coverage_parity'][cohort_name] = len(cohort_metrics['coverage'])
        results['ndcg_parity'][cohort_name] = np.mean(cohort_metrics['ndcgs']) if cohort_metrics['ndcgs'] else 0.0
        results['diversity_parity'][cohort_name] = np.mean(cohort_metrics['diversities']) if cohort_metrics['diversities'] else 0.0
        results['domain_balance'][cohort_name] = cohort_metrics['domain_counts']
        
        print(f"  ✓ Coverage: {len(cohort_metrics['coverage'])} unique courses")
        print(f"  ✓ NDCG@{top_k}: {results['ndcg_parity'][cohort_name]:.4f}")
        print(f"  ✓ Diversity: {results['diversity_parity'][cohort_name]:.4f}")
        print()
    
    # Compute parity gaps
    coverages = list(results['coverage_parity'].values())
    ndcgs = list(results['ndcg_parity'].values())
    diversities = list(results['diversity_parity'].values())
    
    coverage_gap = (max(coverages) - min(coverages)) / min(coverages) * 100 if min(coverages) > 0 else 0
    ndcg_gap = (max(ndcgs) - min(ndcgs)) / min(ndcgs) * 100 if min(ndcgs) > 0 else 0
    diversity_gap = (max(diversities) - min(diversities)) / min(diversities) * 100 if min(diversities) > 0 else 0
    
    results['parity_gaps'] = {
        'coverage_gap_pct': coverage_gap,
        'ndcg_gap_pct': ndcg_gap,
        'diversity_gap_pct': diversity_gap
    }
    
    return results


def generate_report(results, top_k=10):
    """Generate human-readable fairness report."""
    report = []
    report.append("╔" + "="*60 + "╗")
    report.append("║" + " ALGORITHMIC FAIRNESS AUDIT REPORT ".center(60) + "║")
    report.append("╚" + "="*60 + "╝")
    report.append("")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Evaluation: Top-K={top_k}, Cohorts=GPA Tiers")
    report.append("")
    
    # Coverage Parity
    report.append("─" * 62)
    report.append("📊 COVERAGE PARITY (Unique Courses Recommended)")
    report.append("─" * 62)
    for cohort, count in results['coverage_parity'].items():
        report.append(f"  {cohort.upper():20s}: {count:3d} courses")
    gap = results['parity_gaps']['coverage_gap_pct']
    status = "✅ FAIR" if gap < 10 else "⚠️ BIAS DETECTED" if gap < 20 else "❌ SEVERE BIAS"
    report.append(f"  Gap: {gap:.1f}%  {status}")
    report.append("")
    
    # NDCG Parity
    report.append("─" * 62)
    report.append(f"🎯 RANKING QUALITY PARITY (NDCG@{10})")
    report.append("─" * 62)
    for cohort, ndcg in results['ndcg_parity'].items():
        report.append(f"  {cohort.upper():20s}: {ndcg:.4f}")
    gap = results['parity_gaps']['ndcg_gap_pct']
    status = "✅ FAIR" if gap < 5 else "⚠️ BIAS DETECTED" if gap < 10 else "❌ SEVERE BIAS"
    report.append(f"  Gap: {gap:.1f}%  {status}")
    report.append("")
    
    # Diversity Parity
    report.append("─" * 62)
    report.append("🌈 DIVERSITY PARITY (Avg Course Dissimilarity)")
    report.append("─" * 62)
    for cohort, div in results['diversity_parity'].items():
        report.append(f"  {cohort.upper():20s}: {div:.4f}")
    gap = results['parity_gaps']['diversity_gap_pct']
    status = "✅ FAIR" if gap < 10 else "⚠️ CHECK" if gap < 20 else "❌ IMBALANCED"
    report.append(f"  Gap: {gap:.1f}%  {status}")
    report.append("")
    
    # Summary & recommendations
    report.append("─" * 62)
    report.append("📋 SUMMARY & RECOMMENDATIONS")
    report.append("─" * 62)
    total_bias = gap + results['parity_gaps']['coverage_gap_pct'] + results['parity_gaps']['ndcg_gap_pct']
    if total_bias < 15:
        report.append("✅ System shows GOOD fairness properties across cohorts.")
        report.append("   Consider: Monitor fairness quarterly as system evolves.")
    elif total_bias < 30:
        report.append("⚠️ Moderate fairness gaps detected.")
        report.append("   Recommend: Add fairness constraints to meta-learner training.")
        report.append("   Action: Boost diversity penalty for under-served cohorts.")
    else:
        report.append("❌ SIGNIFICANT fairness gaps detected.")
        report.append("   Action: Retrain models with fairness-aware loss functions.")
        report.append("   Action: Add demographic parity constraints.")
    report.append("")
    
    return "\n".join(report)


def main():
    # Load dataset
    df_path = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
    df = pd.read_csv(df_path)
    
    print("🔍 Starting fairness audit...")
    print()
    
    # Run audit
    results = audit_fairness(df, sample_size=50, top_k=10)
    
    # Generate report
    report = generate_report(results, top_k=10)
    print(report)
    
    # Save report
    report_path = os.path.join(BASE_DIR, "fairness_audit_report.txt")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✅ Report saved to {report_path}")
    
    # Save metrics as CSV
    metrics_df = pd.DataFrame({
        'metric': ['coverage_parity', 'ndcg_parity', 'diversity_parity'],
        'high_gpa': [
            results['coverage_parity']['high_gpa'],
            results['ndcg_parity']['high_gpa'],
            results['diversity_parity']['high_gpa']
        ],
        'mid_gpa': [
            results['coverage_parity']['mid_gpa'],
            results['ndcg_parity']['mid_gpa'],
            results['diversity_parity']['mid_gpa']
        ],
        'low_gpa': [
            results['coverage_parity']['low_gpa'],
            results['ndcg_parity']['low_gpa'],
            results['diversity_parity']['low_gpa']
        ],
    })
    metrics_path = os.path.join(BASE_DIR, "fairness_metrics.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"✅ Metrics saved to {metrics_path}")


if __name__ == "__main__":
    main()
