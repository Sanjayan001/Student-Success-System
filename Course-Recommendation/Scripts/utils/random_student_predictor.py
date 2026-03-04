#!/usr/bin/env python3
"""
random_student_predictor.py
Accepts input for a NEW/RANDOM student (not in database) and generates:
1. Course recommendations
2. Risk assessment
3. SHAP + LIME + Gemini explanations

Input format:
- Past courses taken and their grades
- Interest areas
- GPA and attendance
"""

import pandas as pd
import numpy as np
import joblib
from hybrid_infer import recommend_new_user
from shap_lime_explainer import SHAPLIMEExplainer, generate_success_explanation
from gemini_explainer import generate_explanation
import warnings
warnings.filterwarnings('ignore')

# Model paths - ORGANIZED VERSION
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUCCESS_MODEL = os.path.join(BASE_DIR, "Models", "logreg_success.pkl")
SUCCESS_SCALER = os.path.join(BASE_DIR, "Models", "success_scaler.pkl")
DF_PATH = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")


def calculate_risk_score(gpa, attendance_rate):
    """
    Calculate student risk score based on GPA and attendance.
    Lower is better.
    
    Args:
        gpa: GPA (0-4.0 scale)
        attendance_rate: Attendance percentage (0-1.0)
    
    Returns:
        float: Risk score (0-1, where 0 is low risk)
    """
    # Risk is inverse of performance
    gpa_normalized = gpa / 4.0  # Normalize to 0-1
    
    # Weighted combination (lower GPA and attendance = higher risk)
    risk = 1.0 - (gpa_normalized * 0.6 + attendance_rate * 0.4)
    
    # Add some variance
    risk = np.clip(risk, 0.0, 1.0)
    
    return round(risk, 2)


def get_random_student_recommendations(student_profile, top_n=10, job_priority="Balanced", 
                                       use_shap=True, use_lime=True, use_gemini=True):
    """
    Get course recommendations and explanations for a random/new student.
    
    Args:
        student_profile (dict): Student information
            Required keys:
                - past_courses: list of course names taken
                - grades: list of grades (A, B, C, D, F) for each course
                - interest_areas: list of interest domains (e.g., ["Data Science", "AI"])
                - gpa: current GPA (0-4.0)
                - attendance_rate: attendance percentage (0-1.0)
            Optional:
                - age: int
                - university: str
                - degree_program: str
                - career_goal: str
        
        top_n (int): Number of recommendations
        job_priority (str): "Job Market First", "Interest First", or "Balanced"
        use_shap (bool): Include SHAP explanations
        use_lime (bool): Include LIME explanations
        use_gemini (bool): Include Gemini AI explanations
    
    Returns:
        dict with recommendations, risk assessment, and explanations
    """
    
    # Validate input
    required_keys = ['past_courses', 'grades', 'interest_areas', 'gpa', 'attendance_rate']
    for key in required_keys:
        if key not in student_profile:
            raise ValueError(f"Missing required field: {key}")
    
    # Extract student data
    past_courses = student_profile['past_courses']
    grades = student_profile['grades']
    interest_areas = student_profile['interest_areas']
    gpa = float(student_profile['gpa'])
    attendance_rate = float(student_profile['attendance_rate'])
    
    # Validate lengths
    if len(past_courses) != len(grades):
        raise ValueError("past_courses and grades must have the same length")
    
    # Calculate risk score
    risk_score = calculate_risk_score(gpa, attendance_rate)
    
    # Determine risk level
    if risk_score < 0.3:
        risk_level = "LOW"
        risk_message = "Student shows strong academic performance with low dropout risk."
    elif risk_score < 0.6:
        risk_level = "MEDIUM"
        risk_message = "Student has moderate risk. Consider support services or lighter course load."
    else:
        risk_level = "HIGH"
        risk_message = "Student is at high risk of academic difficulties. Immediate intervention recommended."
    
    # Build skills from interest areas and past courses
    skills = ", ".join(interest_areas + past_courses[:3])  # Use interest areas + recent courses as skills
    interests = ", ".join(interest_areas)
    
    # Get course recommendations using hybrid inference
    print("🔄 Generating course recommendations...")
    recommendations = recommend_new_user(
        skills=skills,
        interests=interests,
        gpa=gpa,
        top_n=top_n,
        job_priority=job_priority,
        explain=use_gemini
    )
    
    # Load success model for additional explanations
    try:
        clf = joblib.load(SUCCESS_MODEL)
        scaler = joblib.load(SUCCESS_SCALER)
        df = pd.read_csv(DF_PATH)
        
        # Get background data for SHAP/LIME initialization
        features = ['previous_GPA', 'attendance_rate', 'course_difficulty', 
                   'course_interest', 'job_market_demand_2035', 'risk_score']
        background_data = df[features].dropna().sample(min(1000, len(df)), random_state=42)
        background_data_scaled = scaler.transform(background_data)
        
        model_available = True
    except Exception as e:
        print(f"⚠️ Could not load success model: {e}")
        model_available = False
        background_data_scaled = None
    
    # Add SHAP/LIME explanations to top recommendations
    if model_available and (use_shap or use_lime):
        print("🔬 Generating SHAP/LIME explanations...")
        
        for idx, rec in recommendations.iterrows():
            if idx >= 3:  # Only explain top 3 recommendations
                break
            
            student_data = {
                'previous_GPA': gpa,
                'attendance_rate': attendance_rate,
                'risk_score': risk_score,
                'course_interest': 0.8  # Assume high interest for recommended courses
            }
            
            course_data = {
                'course_difficulty': rec.get('course_difficulty', 0.6),
                'job_market_demand_2035': rec.get('job_market', 0.7)
            }
            
            try:
                shap_lime_exp = generate_success_explanation(
                    clf, scaler, student_data, course_data,
                    background_data=background_data_scaled,
                    use_shap=use_shap,
                    use_lime=use_lime
                )
                recommendations.at[idx, 'shap_lime_explanation'] = shap_lime_exp.get('summary', '')
            except Exception as e:
                print(f"⚠️ SHAP/LIME explanation failed for {rec['course_name']}: {e}")
                recommendations.at[idx, 'shap_lime_explanation'] = "Explanation unavailable"
    
    # Format output
    result = {
        "student_profile": {
            "gpa": gpa,
            "attendance_rate": attendance_rate,
            "past_courses": past_courses,
            "grades": grades,
            "interest_areas": interest_areas,
            "career_goal": student_profile.get('career_goal', 'Not specified'),
            "degree_program": student_profile.get('degree_program', 'Not specified')
        },
        
        "risk_assessment": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_probability": risk_score,
            "explanation": risk_message,
            "factors": {
                "gpa_impact": f"GPA {gpa}/4.0 contributes {(1 - gpa/4.0) * 0.6:.2f} to risk",
                "attendance_impact": f"Attendance {attendance_rate*100:.0f}% contributes {(1 - attendance_rate) * 0.4:.2f} to risk"
            }
        },
        
        "recommended_courses": [],
        
        "explanation_types": {
            "gemini_ai": use_gemini,
            "shap": use_shap and model_available,
            "lime": use_lime and model_available
        }
    }
    
    # Format recommendations
    for idx, rec in recommendations.iterrows():
        course_rec = {
            "rank": idx + 1,
            "course_name": rec['course_name'],
            "course_domain": rec.get('course_domain', 'Unknown'),
            "confidence_score": round(rec['final_score'], 3),
            "success_probability": round(rec.get('p_success', 0.5), 3),
            "difficulty": rec.get('course_difficulty', 'N/A'),
            "job_market_demand": round(rec.get('job_market', 0), 3),
            "why_recommended": rec.get('explanation', 'Based on your profile')
        }
        
        # Add SHAP/LIME explanation if available
        if 'shap_lime_explanation' in rec and pd.notna(rec['shap_lime_explanation']):
            course_rec['technical_explanation'] = rec['shap_lime_explanation']
        
        result["recommended_courses"].append(course_rec)
    
    return result


def interactive_input():
    """
    Interactive CLI for entering student information.
    """
    print("\n" + "="*60)
    print("🎓 SMART COURSE RECOMMENDATION SYSTEM")
    print("="*60)
    print("\nEnter Student Information:")
    print("-" * 60)
    
    # Basic info
    gpa = float(input("📊 Current GPA (0.0-4.0): "))
    attendance = float(input("📅 Attendance Rate (0.0-1.0, e.g., 0.85 for 85%): "))
    
    # Past courses
    print("\n📚 Past Courses Taken:")
    past_courses = []
    grades = []
    
    while True:
        course = input("  Course name (or 'done' to finish): ").strip()
        if course.lower() == 'done':
            break
        grade = input("  Grade (A/B/C/D/F): ").strip().upper()
        past_courses.append(course)
        grades.append(grade)
    
    # Interest areas
    print("\n🎯 Interest Areas (comma-separated):")
    print("   Examples: Data Science, AI, Cybersecurity, Web Development")
    interests_input = input("  Your interests: ")
    interest_areas = [i.strip() for i in interests_input.split(',')]
    
    # Optional info
    career_goal = input("\n💼 Career Goal (optional): ").strip() or "Not specified"
    degree_program = input("🎓 Degree Program (optional): ").strip() or "Not specified"
    
    # Job priority
    print("\n⚙️ Recommendation Priority:")
    print("  1. Job Market First")
    print("  2. Interest First")
    print("  3. Balanced (default)")
    priority_choice = input("  Choice (1/2/3): ").strip()
    
    priority_map = {
        "1": "Job Market First",
        "2": "Interest First",
        "3": "Balanced"
    }
    job_priority = priority_map.get(priority_choice, "Balanced")
    
    # Build profile
    student_profile = {
        "gpa": gpa,
        "attendance_rate": attendance,
        "past_courses": past_courses,
        "grades": grades,
        "interest_areas": interest_areas,
        "career_goal": career_goal,
        "degree_program": degree_program
    }
    
    return student_profile, job_priority


def print_results(result):
    """Pretty print results."""
    print("\n" + "="*60)
    print("📋 RESULTS")
    print("="*60)
    
    # Risk Assessment
    risk = result['risk_assessment']
    print(f"\n🚨 RISK ASSESSMENT")
    print(f"   Risk Level: {risk['risk_level']} (Score: {risk['risk_score']})")
    print(f"   {risk['explanation']}")
    print(f"\n   Contributing Factors:")
    for factor, impact in risk['factors'].items():
        print(f"      • {impact}")
    
    # Recommendations
    print(f"\n📚 TOP COURSE RECOMMENDATIONS")
    print("-" * 60)
    
    for course in result['recommended_courses'][:5]:
        print(f"\n#{course['rank']}. {course['course_name']}")
        print(f"   Domain: {course['course_domain']}")
        print(f"   Success Probability: {course['success_probability']*100:.1f}%")
        print(f"   Job Market Demand: {course['job_market_demand']*100:.0f}%")
        print(f"   \n   💡 Why: {course['why_recommended']}")
        
        if 'technical_explanation' in course:
            print(f"\n   {course['technical_explanation']}")
        
        print()


if __name__ == "__main__":
    # Example usage
    example_student = {
        "gpa": 3.2,
        "attendance_rate": 0.85,
        "past_courses": ["Introduction to Programming", "Data Structures", "Database Systems"],
        "grades": ["B", "A", "B"],
        "interest_areas": ["Data Science", "Machine Learning", "AI"],
        "career_goal": "Data Scientist",
        "degree_program": "Computer Science"
    }
    
    print("📝 Example Student Profile:")
    print(example_student)
    
    result = get_random_student_recommendations(
        example_student,
        top_n=5,
        job_priority="Balanced",
        use_shap=True,
        use_lime=True,
        use_gemini=True
    )
    
    print_results(result)
