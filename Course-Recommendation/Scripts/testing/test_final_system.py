"""
Test script to demonstrate the final recommendation system with all improvements
"""
from hybrid_infer import recommend
import pandas as pd

# Test with student S01424
student_id = 'S01424'
print(f"\n{'='*70}")
print(f"FINAL RECOMMENDATION SYSTEM TEST - STUDENT {student_id}")
print(f"{'='*70}\n")

# Get recommendations with all improvements enabled
print("⚙️  Configuration:")
print("   - Fusion Weights: CF=0.40, CBF=0.35, Success=0.20, Job=0.05 (baseline)")
print("   - MMR Diversity: λ=0.05 (enabled)")
print("   - Job Priority: Balanced")
print("   - Explanations: Enabled (Gemini AI)")

print("\n🔄 Generating recommendations...\n")

recs = recommend(
    student_id=student_id, 
    top_n=10, 
    job_priority='Balanced', 
    explain=True, 
    diversity_lambda=0.05
)

# Display top 10 recommendations
print(f"\n{'='*70}")
print("📊 TOP 10 COURSE RECOMMENDATIONS")
print(f"{'='*70}\n")

# Format the output table
display_cols = ['course_id', 'course_name', 'final_score', 'cf_score', 'cbf_score', 'p_success', 'job_market']
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 40)

for idx, row in recs.iterrows():
    print(f"{idx+1:2d}. {row['course_name'][:45]:45s} | Score: {row['final_score']:.3f}")
    print(f"    Course ID: {row['course_id']:10s} | CF: {row['cf_score']:.3f} | CBF: {row['cbf_score']:.3f} | P(Success): {row['p_success']:.3f} | Job: {row['job_market']:.2f}")
    print()

# Display detailed explanations for top 3
print(f"\n{'='*70}")
print("💡 DETAILED EXPLANATIONS (Top 3)")
print(f"{'='*70}\n")

for idx, row in recs.head(3).iterrows():
    print(f"\n{idx+1}. {row['course_name']} ({row['course_id']})")
    print(f"   {'─'*65}")
    print(f"   Final Score: {row['final_score']:.3f}")
    print(f"   Components: CF={row['cf_score']:.3f}, CBF={row['cbf_score']:.3f}, P(Success)={row['p_success']:.3f}, Job={row['job_market']:.2f}")
    print(f"\n   Explanation:")
    
    # Word wrap the explanation
    explanation = row['explanation']
    words = explanation.split()
    line = "   "
    for word in words:
        if len(line) + len(word) + 1 > 70:
            print(line)
            line = "   " + word
        else:
            line += (" " if line != "   " else "") + word
    if line.strip():
        print(line)
    print()

print(f"\n{'='*70}")
print("✅ RECOMMENDATION GENERATION COMPLETE")
print(f"{'='*70}\n")

# Summary statistics
print("📈 SUMMARY STATISTICS:")
print(f"   Average Final Score: {recs['final_score'].mean():.3f}")
print(f"   Average CF Score:    {recs['cf_score'].mean():.3f}")
print(f"   Average CBF Score:   {recs['cbf_score'].mean():.3f}")
print(f"   Average P(Success):  {recs['p_success'].mean():.3f}")
print(f"   Average Job Demand:  {recs['job_market'].mean():.2f}")

# Diversity check
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import numpy as np

tfidf = joblib.load("tfidf_course.pkl")
df = pd.read_csv("dataset_processed_for_modeling.csv")

course_ids = recs['course_id'].tolist()
vectors = []
for cid in course_ids:
    row = df[df['course_id'] == cid]
    if not row.empty:
        course_text = row['course_text'].iloc[0]
        vec = tfidf.transform([course_text]).toarray().ravel()
        if np.linalg.norm(vec) > 0:
            vec = vec / np.linalg.norm(vec)
        vectors.append(vec)

if len(vectors) >= 2:
    vectors = np.array(vectors)
    sim_matrix = cosine_similarity(vectors)
    n = len(vectors)
    sims = []
    for i in range(n):
        for j in range(i+1, n):
            sims.append(sim_matrix[i, j])
    
    avg_sim = np.mean(sims) if sims else 0.0
    diversity = 1.0 - avg_sim
    print(f"   Diversity Score:     {diversity:.3f} (1.0 = max diversity)")

print(f"\n{'='*70}\n")
