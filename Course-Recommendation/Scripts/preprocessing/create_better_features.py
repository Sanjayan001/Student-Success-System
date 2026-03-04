"""
Create Better Features for Specialization Prediction
The key insight: Students choose specializations based on which courses they do WELL in,
not just general stats. We need course-specific features.
"""
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_better_features():
    """Create features that actually predict specialization"""
    
    # Load course-level data
    df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv"))
    
    print("Creating powerful features for specialization prediction...")
    print(f"Original data: {len(df)} course enrollments")
    
    # Group by student
    student_features = []
    
    for student_id in df['student_id'].unique():
        student_data = df[df['student_id'] == student_id].copy()
        
        features = {'student_id': student_id}
        
        # 1. BEST PERFORMING DOMAIN (Key feature!)
        domain_grades = student_data.groupby('course_domain')['final_grade'].mean()
        features['best_domain'] = domain_grades.idxmax() if len(domain_grades) > 0 else 'Unknown'
        features['best_domain_avg_grade'] = domain_grades.max() if len(domain_grades) > 0 else 0
        features['worst_domain_avg_grade'] = domain_grades.min() if len(domain_grades) > 0 else 0
        features['grade_range'] = features['best_domain_avg_grade'] - features['worst_domain_avg_grade']
        
        # 2. INTEREST IN EACH DOMAIN (Important!)
        domain_interest = student_data.groupby('course_domain')['course_interest'].mean()
        features['highest_interest_domain'] = domain_interest.idxmax() if len(domain_interest) > 0 else 'Unknown'
        features['max_interest'] = domain_interest.max() if len(domain_interest) > 0 else 0
        
        # 3. DOMAIN COMPLETION RATE
        domain_counts = student_data.groupby('course_domain').size()
        features['most_taken_domain'] = domain_counts.idxmax() if len(domain_counts) > 0 else 'Unknown'
        features['n_domains_explored'] = len(domain_counts)
        
        # 4. PERFORMANCE TREND
        student_data_sorted = student_data.sort_values('course_difficulty')
        if len(student_data_sorted) >= 2:
            # Are grades improving or declining?
            features['grade_trend'] = np.corrcoef(range(len(student_data_sorted)), 
                                                  student_data_sorted['final_grade'].fillna(0))[0,1]
        else:
            features['grade_trend'] = 0
        
        # 5. INTEREST × PERFORMANCE (Best predictor!)
        student_data['interest_x_grade'] = student_data['course_interest'] * student_data['final_grade'].fillna(0)
        domain_combined = student_data.groupby('course_domain')['interest_x_grade'].mean()
        features['best_interest_grade_domain'] = domain_combined.idxmax() if len(domain_combined) > 0 else 'Unknown'
        
        # 6. JOB MARKET ALIGNMENT
        student_data['job_x_interest'] = student_data['job_market_demand_2035'] * student_data['course_interest']
        domain_job = student_data.groupby('course_domain')['job_x_interest'].mean()
        features['best_job_aligned_domain'] = domain_job.idxmax() if len(domain_job) > 0 else 'Unknown'
        
        # 7. BASIC STATS
        features['previous_GPA'] = student_data['previous_GPA'].iloc[0]
        features['attendance_rate'] = student_data['attendance_rate'].mean()
        features['avg_course_grade'] = student_data['final_grade'].mean()
        features['n_courses'] = len(student_data)
        
        # 8. PER-DOMAIN GRADES AND COUNTS
        for domain in student_data['course_domain'].unique():
            domain_data = student_data[student_data['course_domain'] == domain]
            features[f'domain_{domain}_avg_grade'] = domain_data['final_grade'].mean()
            features[f'domain_{domain}_count'] = len(domain_data)
            features[f'domain_{domain}_interest'] = domain_data['course_interest'].mean()
        
        student_features.append(features)
    
    # Create DataFrame
    df_features = pd.DataFrame(student_features)
    
    # Fill missing values
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    df_features[numeric_cols] = df_features[numeric_cols].fillna(0)
    
    # Get labels
    labels_df = pd.read_csv(os.path.join(BASE_DIR, "dataset", "student_level_labeled.csv"))[['student_id', 'chosen_specialization']]
    df_final = df_features.merge(labels_df, on='student_id', how='left')
    
    # Save
    output_file = os.path.join(BASE_DIR, "dataset", "student_level_features_improved.csv")
    df_final.to_csv(output_file, index=False)
    
    print(f"\n✅ Created {len(df_final)} student records with {len(df_final.columns)-2} features")
    print(f"   Saved to: {output_file}")
    
    # Show feature importance preview
    print("\n🔑 KEY FEATURES CREATED:")
    print("   1. best_domain - Which domain student performed best in")
    print("   2. best_interest_grade_domain - Domain with highest (interest × grade)")
    print("   3. best_job_aligned_domain - Domain with highest (job_demand × interest)")
    print("   4. Per-domain grades and counts")
    print("   5. Performance trends and patterns")
    
    return df_final


if __name__ == "__main__":
    print("="*60)
    print("FEATURE ENGINEERING FOR SPECIALIZATION PREDICTION")
    print("="*60)
    print()
    
    df = create_better_features()
    
    print("\n" + "="*60)
    print("✅ FEATURE CREATION COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Use 'student_level_features_improved.csv' for training")
    print("  2. Focus on 'best_domain' and interaction features")
    print("  3. These features should give MUCH better accuracy!")
