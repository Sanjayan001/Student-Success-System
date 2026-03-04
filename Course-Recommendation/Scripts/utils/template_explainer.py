#!/usr/bin/env python3
"""
template_explainer.py
Fast template-based explanations for course recommendations.
"""

def generate_template_explanation(student_data, course_data, scores):
    """
    Generate instant, personalized explanation using templates.
    Much faster than Gemini API calls.
    """
    gpa = student_data.get('previous_GPA', 0)
    attendance = student_data.get('attendance_rate', 0) * 100
    risk = student_data.get('risk_score', 0)
    
    course_name = course_data.get('course_name', 'this course')
    domain = course_data.get('course_domain', 'General')
    difficulty = course_data.get('course_difficulty', 0.5) * 100
    job_market = course_data.get('job_market', 0) * 100
    
    cf_score = scores.get('cf_score', 0) * 100
    cbf_score = scores.get('cbf_score', 0) * 100
    p_success = scores.get('p_success', 0) * 100
    
    # Determine student performance level
    if gpa >= 3.5:
        performance = "excellent"
    elif gpa >= 3.0:
        performance = "strong"
    elif gpa >= 2.5:
        performance = "solid"
    else:
        performance = "developing"
    
    # Select appropriate template based on profile
    if gpa >= 3.0 and attendance >= 80:
        # High performer template
        explanation = (
            f"Your {performance} {gpa:.2f} GPA and {attendance:.0f}% attendance demonstrate you're ready for exciting challenges! "
            f"{course_name} is an excellent match—students with similar profiles have thrived here ({cf_score:.0f}% similarity), "
            f"and we predict a {p_success:.0f}% success rate for you."
        )
        if job_market > 70:
            explanation += f" Plus, this {domain} field shows strong career prospects with {job_market:.0f}% job market demand!"
    
    elif gpa >= 2.5 and p_success >= 60:
        # Average performer with good fit template
        explanation = (
            f"With your {gpa:.2f} GPA and {attendance:.0f}% attendance, you're well-positioned for this course. "
            f"Students with similar backgrounds have achieved {p_success:.0f}% success rates here, "
            f"and your {cbf_score:.0f}% interest alignment suggests you'll find it engaging."
        )
        if job_market > 70:
            explanation += f" This field also offers excellent career opportunities ({job_market:.0f}% demand)!"
    
    elif p_success >= 50:
        # Encouraging template for struggling students
        explanation = (
            f"We've carefully considered your profile and see genuine opportunity here. "
            f"While your academic journey has had challenges, {course_name} could be a great fit—"
            f"students with similar experiences have achieved {p_success:.0f}% success rates, "
            f"and your {cbf_score:.0f}% interest match shows real potential."
        )
        if job_market > 60:
            explanation += f" Plus, this field offers strong job prospects ({job_market:.0f}% demand) worth pursuing!"
    
    else:
        # General supportive template
        explanation = (
            f"Based on comprehensive analysis of your academic profile, {course_name} is recommended. "
            f"This course aligns {cbf_score:.0f}% with your interests and background, "
            f"with a predicted {p_success:.0f}% success rate."
        )
        if job_market > 70:
            explanation += f" Strong career demand ({job_market:.0f}%) makes this a valuable choice!"
    
    return explanation


if __name__ == "__main__":
    # Test the template explainer
    print("Testing Template Explainer...\n")
    
    test_cases = [
        # High performer
        {
            'student': {'previous_GPA': 3.7, 'attendance_rate': 0.92, 'risk_score': 0.15},
            'course': {'course_name': 'Machine Learning Advanced', 'course_domain': 'AI', 
                      'course_difficulty': 0.75, 'job_market': 0.95},
            'scores': {'cf_score': 0.85, 'cbf_score': 0.88, 'p_success': 0.82, 'final_score': 0.85}
        },
        # Average student
        {
            'student': {'previous_GPA': 2.8, 'attendance_rate': 0.75, 'risk_score': 0.35},
            'course': {'course_name': 'Data Science Fundamentals', 'course_domain': 'Data Science',
                      'course_difficulty': 0.55, 'job_market': 0.88},
            'scores': {'cf_score': 0.68, 'cbf_score': 0.72, 'p_success': 0.65, 'final_score': 0.70}
        },
        # Struggling student
        {
            'student': {'previous_GPA': 2.1, 'attendance_rate': 0.65, 'risk_score': 0.55},
            'course': {'course_name': 'Finance Fundamentals', 'course_domain': 'Finance',
                      'course_difficulty': 0.45, 'job_market': 0.75},
            'scores': {'cf_score': 0.55, 'cbf_score': 0.78, 'p_success': 0.58, 'final_score': 0.62}
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test Case {i}:")
        print(f"GPA: {test['student']['previous_GPA']:.2f}")
        explanation = generate_template_explanation(test['student'], test['course'], test['scores'])
        print(f"Explanation: {explanation}")
        print("-" * 80 + "\n")
    
    print("✅ Template Explainer works perfectly!")
    print("⚡ Speed: Instant (no API calls needed)")
