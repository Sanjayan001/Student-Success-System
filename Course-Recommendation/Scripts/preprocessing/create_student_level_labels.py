# create_student_level_labels.py
"""
Aggregate course-level CSV into student-level labeled CSV.
Input: dataset_processed_for_modeling.csv
Output: student_level_labeled.csv
"""

import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
OUTPUT = os.path.join(BASE_DIR, "dataset", "student_level_labeled.csv")

def main():
    print("Loading:", INPUT)
    df = pd.read_csv(INPUT)
    print("Rows:", len(df))

    # Ensure expected columns exist
    required = ['student_id','degree_program','previous_GPA','attendance_rate','final_grade',
                'course_interest','job_market_demand_2035','risk_score','course_domain','course_id']
    for c in required:
        if c not in df.columns:
            print(f"Warning: column missing: {c} (some features may be incomplete)")

    # Aggregate per-student basic stats
    agg = df.groupby('student_id').agg(
        previous_GPA = ('previous_GPA','mean'),
        attendance_rate = ('attendance_rate','mean'),
        avg_course_grade = ('final_grade','mean'),
        avg_course_interest = ('course_interest','mean'),
        avg_job_demand = ('job_market_demand_2035','mean'),
        avg_risk = ('risk_score','mean'),
        n_courses = ('course_id','nunique')
    ).reset_index()

    # domain counts: create domain frequency features for top domains
    domain_counts = df.groupby(['student_id','course_domain']).size().unstack(fill_value=0)
    domain_counts.columns = [f"domain_cnt_{c}" for c in domain_counts.columns]
    agg = agg.merge(domain_counts.reset_index(), on='student_id', how='left')

    # Create chosen_specialization label from degree_program mode per student
    # If degree_program not present, fall back to most frequent course_domain
    def mode_or_na(x):
        try:
            return x.mode().iat[0]
        except:
            return np.nan

    spec = df.groupby('student_id')['degree_program'].agg(mode_or_na).reset_index().rename(columns={'degree_program':'chosen_specialization'})
    # Fill NAs with most common course_domain if necessary
    missing = spec['chosen_specialization'].isna().sum()
    if missing > 0:
        print(f"Filling {missing} missing specialization labels using most frequent course_domain")
        fallback = df.groupby('student_id')['course_domain'].agg(mode_or_na).reset_index().rename(columns={'course_domain':'chosen_specialization'})
        spec = spec.set_index('student_id')
        fallback = fallback.set_index('student_id')
        spec['chosen_specialization'] = spec['chosen_specialization'].fillna(fallback['chosen_specialization'])
        spec = spec.reset_index()

    out = agg.merge(spec, on='student_id', how='left')

    # Drop students without label (rare)
    before = len(out)
    out = out.dropna(subset=['chosen_specialization'])
    after = len(out)
    print(f"Dropped {before-after} students without specialization label")

    print("Saving:", OUTPUT)
    out.to_csv(OUTPUT, index=False)
    print("Done. Saved", OUTPUT, "Rows:", len(out))

if __name__ == "__main__":
    main()
