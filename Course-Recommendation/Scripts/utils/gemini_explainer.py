#!/usr/bin/env python3
"""
gemini_explainer.py
Generates human-friendly course recommendation explanations using Google Gemini Pro API.
"""

import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API via environment (no hardcoded keys)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Only configure if API key is present; otherwise, generation will fallback
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception:
        # If configuration fails, we'll rely on fallback explanations later
        GEMINI_API_KEY = None

def generate_explanation(student_data, course_data, scores, verbose=False):
    """
    Generate a friendly, personalized explanation for a course recommendation.
    
    Args:
        student_data (dict): Student profile with keys:
            - previous_GPA: float (0-4.0)
            - attendance_rate: float (0-1.0)
            - risk_score: float (0-1.0, lower is better)
            - student_id: str (optional)
        
        course_data (dict): Course information with keys:
            - course_name: str
            - course_domain: str
            - course_difficulty: float (0-1.0)
            - job_market: float (0-1.0)
        
        scores (dict): Model scores with keys:
            - cf_score: float (collaborative filtering)
            - cbf_score: float (content-based filtering)
            - p_success: float (predicted success probability)
            - final_score: float (overall recommendation score)
    
    Returns:
        str: Human-friendly explanation text from Gemini Pro
    """
    
    # Extract and format data safely
    gpa = student_data.get('previous_GPA', 0)
    attendance = student_data.get('attendance_rate', 0) * 100
    risk = student_data.get('risk_score', 0)
    
    course_name = course_data.get('course_name', 'this course')
    domain = course_data.get('course_domain', 'General')
    difficulty = course_data.get('course_difficulty', 0.5) * 100
    job_demand = course_data.get('job_market', 0) * 100
    
    cf_score = scores.get('cf_score', 0) * 100
    cbf_score = scores.get('cbf_score', 0) * 100
    p_success = scores.get('p_success', 0) * 100
    final_score = scores.get('final_score', 0)
    
    # Build prompt for Gemini - Enhanced for more personal, empathetic responses
    prompt = f"""You are a caring and experienced university academic advisor helping a student understand why an AI-powered recommendation system has suggested a specific course for them.

**Student Profile:**
- Current GPA: {gpa:.2f}/4.0
- Attendance Record: {attendance:.0f}%
- Academic Risk Assessment: {"Low risk" if risk < 0.3 else "Moderate support needed" if risk < 0.6 else "Needs extra support"}

**Recommended Course:**
- **{course_name}**
- Field: {domain}
- Difficulty: {difficulty:.0f}%
- Career Relevance (Job Market 2035): {job_demand:.0f}%

**AI Analysis Results:**
- Similar Students' Success Pattern Match: {cf_score:.0f}%
- Interest & Background Alignment: {cbf_score:.0f}%
- Your Predicted Success Rate: {p_success:.0f}%
- Overall Match Strength: {final_score:.2f}/1.0

**Your Task:**
Write a warm, encouraging, and genuinely personalized explanation (2-4 sentences) that helps this student understand why this course is a great fit for them.

**CRITICAL Requirements:**
1. **Be empathetic and supportive** - Acknowledge their journey, not just their numbers
2. **Tell a story** - Connect their profile to why this specific course makes sense
3. **Sound human** - Use phrases like "we've carefully considered", "we see great opportunity", "we're confident"
4. **Be specific** - Reference actual scores naturally (e.g., "87% match with similar students")
5. **Encourage growth** - Frame challenges positively ("opportunity to develop", "build on your potential")
6. **Highlight strengths** - Mention their GPA or attendance if good
7. **Career connection** - If job market >70%, mention real-world value
8. **Avoid robotic language** - Don't say "based on analysis" or "the system recommends"

**Example of the EXACT tone and style you should match:**

*For a struggling student (GPA 2.1, low attendance):*
"While your academic journey has presented some challenges, we've carefully considered your profile and see a great opportunity here. {course_name} is strongly recommended because the AI found that students with similar experiences have genuinely excelled in this course (an {cf_score:.0f}% match!), and it predicts a solid {p_success:.0f}% chance of success for you. We're confident this course will help you build on your potential and develop valuable skills."

*For a high achiever (GPA 3.8, excellent attendance):*
"Your outstanding {gpa:.2f} GPA and exemplary {attendance:.0f}% attendance show you're ready for exciting challenges! {course_name} is an excellent match—students with your strong academic profile have thrived here ({cf_score:.0f}% similarity), and we predict an impressive {p_success:.0f}% success rate for you. Plus, this field shows exceptional career prospects with {job_demand:.0f}% job market demand!"

**Now generate a similar explanation for THIS student. Make it feel personal, supportive, and genuinely helpful:**"""
    
    try:
        # Initialize Gemini model (configurable via env)
        if not GEMINI_API_KEY:
            raise RuntimeError("Gemini API key not configured")
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        
        # Add retry logic for rate limiting
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Generate explanation
                response = model.generate_content(prompt)
                explanation_text = response.text.strip()
                
                if verbose:
                    print(f"\n[Gemini XAI] Generated explanation for {course_name}")
                    print(f"Response: {explanation_text}\n")
                
                return explanation_text
                
            except Exception as retry_error:
                if "429" in str(retry_error) or "quota" in str(retry_error).lower():
                    # Rate limit hit - wait and retry
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2  # 2s, 4s, 6s
                        if verbose:
                            print(f"Rate limit hit, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                raise retry_error
    
    except Exception as e:
        # Fallback to empathetic explanation if API fails
        # Make fallback more personal too
        if gpa >= 3.5:
            fallback = (f"Your excellent {gpa:.2f} GPA shows you're ready for this challenge! "
                       f"Students with similar profiles have achieved {p_success:.0f}% success rates here. "
                       f"This course aligns strongly with your academic journey.")
        elif gpa >= 2.5:
            fallback = (f"With your {gpa:.2f} GPA and consistent performance, you're well-positioned for this course. "
                       f"The AI found a {cf_score:.0f}% match with successful students, predicting {p_success:.0f}% success for you. "
                       f"We're confident you'll excel here!")
        else:
            fallback = (f"We've carefully considered your profile and see real potential here. "
                       f"Students with similar backgrounds have succeeded at {p_success:.0f}% rates, "
                       f"and this course can help you develop valuable skills for your future.")
        
        if verbose:
            print(f"\n[Gemini XAI] API error: {e}")
            print(f"Using enhanced fallback explanation\n")
        
        return fallback


def batch_generate_explanations(recommendations_df, student_data_dict, verbose=False):
    """
    Generate explanations for a batch of recommendations.
    
    Args:
        recommendations_df (pd.DataFrame): DataFrame with recommendations
        student_data_dict (dict): Mapping of student_id to student data
        verbose (bool): Print progress
    
    Returns:
        pd.DataFrame: Input DataFrame with 'gemini_explanation' column added
    """
    explanations = []
    
    for idx, row in recommendations_df.iterrows():
        student_id = row.get('student_id', 'unknown')
        student_data = student_data_dict.get(student_id, {})
        
        course_data = {
            'course_name': row.get('course_name', 'Unknown Course'),
            'course_domain': row.get('course_domain', 'General'),
            'course_difficulty': row.get('course_difficulty', 0.5),
            'job_market': row.get('job_market', 0.5)
        }
        
        scores = {
            'cf_score': row.get('cf_score', 0),
            'cbf_score': row.get('cbf_score', 0),
            'p_success': row.get('p_success', 0),
            'final_score': row.get('final_score', 0)
        }
        
        explanation = generate_explanation(student_data, course_data, scores, verbose)
        explanations.append(explanation)
        
        if verbose and (idx + 1) % 5 == 0:
            print(f"Generated {idx + 1}/{len(recommendations_df)} explanations")
    
    recommendations_df['gemini_explanation'] = explanations
    return recommendations_df


if __name__ == "__main__":
    # Test with sample data
    print("Testing Gemini Explainer...\n")
    
    test_student = {
        'student_id': 'S01290',
        'previous_GPA': 3.2,
        'attendance_rate': 0.85,
        'risk_score': 0.25
    }
    
    test_course = {
        'course_name': 'Machine Learning Advanced',
        'course_domain': 'AI',
        'course_difficulty': 0.72,
        'job_market': 0.92
    }
    
    test_scores = {
        'cf_score': 0.78,
        'cbf_score': 0.85,
        'p_success': 0.71,
        'final_score': 0.79
    }
    
    print("Generating explanation...")
    explanation = generate_explanation(test_student, test_course, test_scores, verbose=True)
    
    print("\n" + "="*70)
    print("FINAL EXPLANATION:")
    print("="*70)
    print(explanation)
    print("="*70)
    print("\n✅ Gemini Explainer test completed successfully!")
