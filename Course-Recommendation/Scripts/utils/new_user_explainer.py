#!/usr/bin/env python3
"""
new_user_explainer.py
Detailed explanations for cold-start new users without student_id.
"""

def generate_new_user_explanation(user_profile, course_data, scores, rank):
    """
    Generate detailed, encouraging explanation for new users.
    
    Args:
        user_profile: Dict with 'skills', 'interests', 'gpa'
        course_data: Course details
        scores: Recommendation scores
        rank: Position in recommendation list (1-10)
    """
    gpa = user_profile.get('gpa', 3.0)
    skills = user_profile.get('skills', '')
    interests = user_profile.get('interests', '')
    
    course_name = course_data.get('course_name', 'this course')
    domain = course_data.get('course_domain', 'General')
    difficulty = course_data.get('course_difficulty', 0.5)
    job_market = course_data.get('job_market', 0)
    
    cbf_score = scores.get('cbf_score', 0)
    p_success = scores.get('p_success', 0)
    final_score = scores.get('final_score', 0)
    
    # Build personalized explanation with more details
    explanation = "🤖 **AI Advisor Recommendation**\n\n"
    
    # Opening - personalized based on rank
    if rank == 1:
        explanation += "This is our **top recommendation** for you! "
    elif rank <= 3:
        explanation += "This is one of our **strongest matches** for your profile! "
    else:
        explanation += "This course is a **solid match** for your background. "
    
    # Profile analysis
    if gpa >= 3.5:
        explanation += f"With your excellent {gpa:.2f} GPA, you demonstrate strong academic capabilities. "
    elif gpa >= 3.0:
        explanation += f"Your {gpa:.2f} GPA shows solid academic performance. "
    elif gpa >= 2.5:
        explanation += f"Your {gpa:.2f} GPA indicates good foundational knowledge. "
    else:
        explanation += f"We've carefully considered your {gpa:.2f} GPA and see real growth potential. "
    
    # Skills match analysis
    skill_list = [s.strip().lower() for s in skills.split(',') if s.strip()]
    course_lower = course_name.lower()
    matching_skills = [skill for skill in skill_list if skill in course_lower or course_lower in skill]
    
    if matching_skills:
        explanation += f"Your skills in **{', '.join(matching_skills[:3])}** directly align with this course content. "
    elif cbf_score >= 0.7:
        explanation += f"Your skillset shows **{cbf_score*100:.0f}% alignment** with this course's requirements. "
    else:
        explanation += f"This course complements your current skills and will help you grow in new areas ({cbf_score*100:.0f}% content match). "
    
    # Success prediction with context
    explanation += f"\n\n📊 **Success Analysis:** "
    if p_success >= 0.85:
        explanation += f"Students with similar profiles achieve **{p_success*100:.0f}% success rates** in this course—you're very likely to excel! "
    elif p_success >= 0.70:
        explanation += f"Based on your profile, we predict a **{p_success*100:.0f}% success rate**—strong odds for completing successfully. "
    elif p_success >= 0.60:
        explanation += f"Students with comparable backgrounds achieve **{p_success*100:.0f}% success rates** here. With dedication, you can definitely succeed! "
    else:
        explanation += f"While challenging, students with your profile achieve **{p_success*100:.0f}% success rates**. We recommend this because it will push your growth. "
    
    # Difficulty assessment
    if difficulty >= 0.8:
        explanation += f"Note: This is an **advanced course** (difficulty: {difficulty*100:.0f}/100), best for those ready for serious challenges. "
    elif difficulty >= 0.6:
        explanation += f"This **intermediate-level** course (difficulty: {difficulty*100:.0f}/100) provides a good balance of challenge and achievability. "
    else:
        explanation += f"As a **foundational course** (difficulty: {difficulty*100:.0f}/100), it's great for building core competencies. "
    
    # Career relevance
    explanation += f"\n\n💼 **Career Impact:** "
    if job_market >= 0.8:
        explanation += f"**Excellent career prospects!** This {domain} field shows **{job_market*100:.0f}% job market demand** through 2035. Companies are actively seeking these skills. "
    elif job_market >= 0.6:
        explanation += f"Strong job market demand (**{job_market*100:.0f}%**) in {domain} makes this course valuable for your future career. "
    elif job_market >= 0.4:
        explanation += f"Moderate job demand ({job_market*100:.0f}%) in this field. Consider it for skill diversification. "
    else:
        explanation += f"While niche ({job_market*100:.0f}% demand), this could differentiate you in specialized roles. "
    
    # Interest alignment
    if interests.strip():
        interest_list = [i.strip().lower() for i in interests.split(',')]
        domain_lower = domain.lower()
        matching_interests = [interest for interest in interest_list if interest in domain_lower or domain_lower in interest]
        
        if matching_interests:
            explanation += f"This perfectly matches your stated interest in **{', '.join(matching_interests[:2])}**! "
        elif cbf_score >= 0.6:
            explanation += f"Based on your interests, this course offers strong alignment and should keep you engaged. "
    
    # Closing recommendation
    explanation += f"\n\n✨ **Our Verdict:** "
    if final_score >= 0.7:
        explanation += f"**Highly Recommended** (Match Score: {final_score:.2f}/1.00). This course checks all the boxes for your goals and capabilities. "
    elif final_score >= 0.5:
        explanation += f"**Recommended** (Match Score: {final_score:.2f}/1.00). A solid choice that balances your interests, abilities, and career goals. "
    else:
        explanation += f"**Worth Considering** (Match Score: {final_score:.2f}/1.00). While not a perfect fit, it offers unique learning opportunities. "
    
    if rank <= 3:
        explanation += "Start here! 🚀"
    
    return explanation


if __name__ == "__main__":
    # Test example
    user = {
        'skills': 'Python, Machine Learning, Data Analysis',
        'interests': 'Artificial Intelligence, Data Science',
        'gpa': 3.2
    }
    course = {
        'course_name': 'Advanced Machine Learning',
        'course_domain': 'Computer Science',
        'course_difficulty': 0.75,
        'job_market': 0.85
    }
    scores_ex = {
        'cbf_score': 0.82,
        'p_success': 0.78,
        'final_score': 0.73
    }
    
    explanation = generate_new_user_explanation(user, course, scores_ex, rank=1)
    print(explanation)
