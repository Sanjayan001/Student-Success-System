#!/usr/bin/env python3
"""
Quick test to see enhanced Gemini explanations in action
"""

from hybrid_infer import recommend

print("Testing Enhanced Gemini Explanations\n")
print("="*80)

# Test with a real student
student_id = "S01290"
print(f"Generating recommendations for {student_id}...\n")

recs = recommend(student_id, top_n=3)

print("="*80)
print("TOP 3 RECOMMENDATIONS WITH GEMINI EXPLANATIONS")
print("="*80)

for idx, row in recs.iterrows():
    print(f"\n📚 {idx+1}. {row['course_name']}")
    print(f"   Score: {row['final_score']:.3f}")
    print(f"   Success Rate: {row['p_success']*100:.0f}%")
    print(f"\n   🤖 AI Explanation:")
    print(f"   {row['explanation']}")
    print("-" * 80)

print("\n✅ Test completed! Check if explanations are now more personal and empathetic.")
