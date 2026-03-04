#!/usr/bin/env python3
"""
streamlit_app.py
Interactive web dashboard for the Course Recommendation System with Gemini XAI.

Run with: streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

# Add Scripts/utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Scripts', 'utils'))

from hybrid_infer import recommend, recommend_new_user
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="AI Course Recommender",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Predefined skills for quick selection (can be extended)
AVAILABLE_SKILLS = [
    # Computer Science & IT
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript",
    "Machine Learning", "Deep Learning", "Data Analysis", "Statistics", "Linear Algebra",
    "SQL", "NoSQL", "Data Engineering", "ETL", "Big Data",
    "Artificial Intelligence", "NLP", "Computer Vision",
    "Web Development", "Frontend", "Backend", "Full Stack", "React", "Angular", "Vue",
    "Node.js", "Django", "Flask", "Spring", ".NET",
    "Cloud", "AWS", "Azure", "GCP",
    "DevOps", "CI/CD", "Docker", "Kubernetes",
    "Cybersecurity", "Networking", "Blockchain",
    "R", "Tableau", "Power BI", "Excel",
    
    # Engineering (General & Mechanical)
    "AutoCAD", "SolidWorks", "CATIA", "ANSYS", "MATLAB", "Simulink",
    "CAD Design", "3D Modeling", "Finite Element Analysis", "CFD",
    "Mechanical Design", "Thermodynamics", "Fluid Mechanics", "Material Science",
    "Manufacturing", "CNC Programming", "Robotics", "Mechatronics",
    "Quality Control", "Six Sigma", "Lean Manufacturing",
    
    # Electronics & Electrical Engineering
    "Circuit Design", "PCB Design", "Embedded Systems", "Microcontrollers",
    "Arduino", "Raspberry Pi", "PLC Programming", "SCADA",
    "VHDL", "Verilog", "FPGA", "Signal Processing",
    "Power Electronics", "Control Systems", "Instrumentation",
    "MATLAB Simulink", "LTSpice", "Eagle", "KiCad", "Altium Designer",
    "IoT", "Sensor Technology", "Automation",
    
    # Agriculture & Environmental Science
    "Precision Agriculture", "Agronomy", "Soil Science", "Crop Management",
    "Agricultural Economics", "Farm Management", "Irrigation Systems",
    "GIS", "Remote Sensing", "GPS Technology", "Drone Technology",
    "Sustainable Farming", "Organic Farming", "Hydroponics", "Aquaponics",
    "Pest Management", "Plant Pathology", "Animal Husbandry", "Veterinary Science",
    "Food Science", "Food Safety", "Post-Harvest Technology",
    "Agricultural Biotechnology", "Seed Technology",
    "Climate Smart Agriculture", "Environmental Impact Assessment",
    
    # Business Management & Commerce
    "Financial Accounting", "Management Accounting", "Cost Accounting",
    "Financial Analysis", "Budgeting", "Financial Planning",
    "Marketing", "Digital Marketing", "Brand Management", "Market Research",
    "Sales Management", "Customer Relationship Management", "CRM",
    "Human Resource Management", "Talent Acquisition", "Performance Management",
    "Strategic Management", "Project Management", "Agile", "Scrum",
    "Supply Chain Management", "Logistics", "Operations Management",
    "Business Analytics", "Business Intelligence", "SAP", "ERP",
    "Risk Management", "Compliance", "Corporate Governance",
    "Entrepreneurship", "Business Development", "E-commerce",
    "QuickBooks", "Tally", "MS Office Suite",
    
    # Arts, Design & Creative
    "Graphic Design", "UI/UX Design", "Adobe Photoshop", "Adobe Illustrator",
    "Adobe InDesign", "Figma", "Sketch", "Canva",
    "Video Editing", "Adobe Premiere Pro", "Final Cut Pro", "After Effects",
    "3D Animation", "Blender", "Maya", "Cinema 4D",
    "Photography", "Videography", "Digital Art", "Illustration",
    "Web Design", "Motion Graphics", "Typography",
    "Creative Writing", "Content Writing", "Copywriting", "SEO Writing",
    "Social Media Management", "Content Strategy",
    "Music Production", "Audio Engineering", "Sound Design",
    "Interior Design", "Fashion Design", "Product Design",
    
    # Civil & Construction Engineering
    "Structural Engineering", "Geotechnical Engineering", "Transportation Engineering",
    "Construction Management", "Building Information Modeling", "BIM", "Revit",
    "Surveying", "Site Planning", "Urban Planning",
    "Concrete Technology", "Steel Structures", "Highway Engineering",
    
    # Chemical & Process Engineering
    "Chemical Process Design", "Process Simulation", "Aspen HYSYS",
    "Chemical Safety", "Process Control", "Refinery Operations",
    "Polymer Engineering", "Pharmaceutical Engineering",
    
    # Other Professional Skills
    "Communication", "Leadership", "Teamwork", "Problem Solving",
    "Critical Thinking", "Time Management", "Presentation Skills",
    "Research", "Technical Writing", "Report Writing"
]

# Study resources mapped by course domain
STUDY_RESOURCES = {
    "AI": {
        "youtube": [
            ("Python for Machine Learning – Full Course (freeCodeCamp)", "https://www.youtube.com/watch?v=i_LwzRVP7bg"),
            ("Deep Learning Specialization – Andrew Ng (Coursera playlist)", "https://www.youtube.com/watch?v=CS4cs9xVecg"),
            ("Neural Networks Zero to Hero (Andrej Karpathy)", "https://www.youtube.com/watch?v=VMj-3S1tku0"),
            ("Practical AI / ML – Sentdex playlist", "https://www.youtube.com/watch?v=OGxgnH8y2NM"),
        ],
        "references": [
            ("fast.ai (Practical Deep Learning)", "https://www.fast.ai/"),
            ("Hugging Face Documentation", "https://huggingface.co/docs"),
            ("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"),
        ],
    },
    "Data Science": {
        "youtube": [
            ("Data Science Full Course – Simplilearn", "https://www.youtube.com/watch?v=-ETQ97mXXF0"),
            ("Pandas Tutorial – Corey Schafer", "https://www.youtube.com/watch?v=ZyhVh-qRZPA"),
            ("Statistics for Data Science (StatQuest)", "https://www.youtube.com/watch?v=qBigTkBLU6g"),
            ("Tableau Full Course for Beginners", "https://www.youtube.com/watch?v=TPMlZxRRaBQ"),
        ],
        "references": [
            ("Kaggle Learn (free micro-courses)", "https://www.kaggle.com/learn"),
            ("Towards Data Science (Medium)", "https://towardsdatascience.com/"),
            ("DataCamp Community Tutorials", "https://www.datacamp.com/tutorial"),
        ],
    },
    "Software Engineering": {
        "youtube": [
            ("CS50 – Harvard (Full Course)", "https://www.youtube.com/watch?v=8mAITcNt710"),
            ("Clean Code Principles – freeCodeCamp", "https://www.youtube.com/watch?v=SqrbIlUwR0U"),
            ("System Design Primer (Gaurav Sen)", "https://www.youtube.com/watch?v=xpDnVSmNFX0"),
            ("Git & GitHub Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=RGOj5yH7evk"),
        ],
        "references": [
            ("The Odin Project (Web Dev)", "https://www.theodinproject.com/"),
            ("MDN Web Docs", "https://developer.mozilla.org/"),
            ("Refactoring Guru (Design Patterns)", "https://refactoring.guru/design-patterns"),
        ],
    },
    "Cybersecurity": {
        "youtube": [
            ("Cybersecurity Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=U_P23SqJaDc"),
            ("Ethical Hacking – TCM Security (full course)", "https://www.youtube.com/watch?v=3Kq1MIfTWCE"),
            ("Network Security Fundamentals – Professor Messer", "https://www.youtube.com/watch?v=0bTU-tl5tSU"),
        ],
        "references": [
            ("TryHackMe (Hands-on labs)", "https://tryhackme.com/"),
            ("OWASP Top 10", "https://owasp.org/www-project-top-ten/"),
            ("NIST Cybersecurity Framework", "https://www.nist.gov/cyberframework"),
        ],
    },
    "Networking": {
        "youtube": [
            ("CompTIA Network+ Full Course – Professor Messer", "https://www.youtube.com/watch?v=As6g6IXcVa4"),
            ("Computer Networking Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=qiQR5rTSshw"),
            ("Cisco CCNA Full Course", "https://www.youtube.com/watch?v=n2D1o-aM-2s"),
        ],
        "references": [
            ("Cisco NetAcad", "https://www.netacad.com/"),
            ("Network+ Study Guide (CompTIA)", "https://www.comptia.org/certifications/network"),
            ("Packet Tracer Labs (Cisco)", "https://www.netacad.com/courses/packet-tracer"),
        ],
    },
    "Mechanical": {
        "youtube": [
            ("Mechanical Engineering Full Course – GATE Lectures", "https://www.youtube.com/c/GATELectures"),
            ("SolidWorks Tutorial for Beginners", "https://www.youtube.com/watch?v=MkFx7uQUhpk"),
            ("ANSYS FEA Tutorial – LearnEngineering.in", "https://www.youtube.com/watch?v=vHrSpMEFAXk"),
            ("Thermodynamics Full Course – Michel van Biezen", "https://www.youtube.com/watch?v=dONNKIqoMn8"),
        ],
        "references": [
            ("MIT OpenCourseWare – Mechanical Engineering", "https://ocw.mit.edu/courses/mechanical-engineering/"),
            ("Engineering Toolbox", "https://www.engineeringtoolbox.com/"),
            ("ASME Standards & Resources", "https://www.asme.org/"),
        ],
    },
    "Electrical": {
        "youtube": [
            ("Electrical Engineering – freeCodeCamp", "https://www.youtube.com/watch?v=mc979OhitAg"),
            ("Circuit Analysis Full Course – Michel van Biezen", "https://www.youtube.com/watch?v=8Ow6D-s5F3k"),
            ("Power Systems Engineering – NPTEL", "https://www.youtube.com/watch?v=3NxJHDRDiys"),
        ],
        "references": [
            ("MIT OCW – Electrical Engineering", "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/"),
            ("AllAboutCircuits", "https://www.allaboutcircuits.com/"),
            ("IEEE Xplore", "https://ieeexplore.ieee.org/"),
        ],
    },
    "Finance": {
        "youtube": [
            ("Financial Accounting Full Course – AccountingStuff", "https://www.youtube.com/watch?v=yYX4bvQSqbo"),
            ("Corporate Finance – Aswath Damodaran (NYU)", "https://www.youtube.com/c/AswathDamodaranonValuation"),
            ("CFA Level 1 – IFT (free playlist)", "https://www.youtube.com/watch?v=SjhDWjfhJLM"),
        ],
        "references": [
            ("Investopedia Academy", "https://www.investopedia.com/financial-edge/"),
            ("Khan Academy – Finance", "https://www.khanacademy.org/economics-finance-domain"),
            ("Corporate Finance Institute", "https://corporatefinanceinstitute.com/resources/"),
        ],
    },
    "Management": {
        "youtube": [
            ("MBA Core Concepts – IIM Bangalore (NPTEL)", "https://www.youtube.com/watch?v=Gl_r9fWDj7E"),
            ("Project Management Full Course – Simplilearn", "https://www.youtube.com/watch?v=GC7pN8Mjot8"),
            ("Strategic Management – freeCodeCamp", "https://www.youtube.com/watch?v=xIqM4A9EJZY"),
        ],
        "references": [
            ("PMI (Project Management Institute)", "https://www.pmi.org/learning/library"),
            ("Harvard Business Review", "https://hbr.org/"),
            ("Coursera – Business Fundamentals", "https://www.coursera.org/browse/business"),
        ],
    },
    "Healthcare": {
        "youtube": [
            ("Medical Terminology Full Course", "https://www.youtube.com/watch?v=hTf8kpzGzsk"),
            ("Public Health & Epidemiology – Coursera (Johns Hopkins)", "https://www.youtube.com/watch?v=C0n1qHVDsOM"),
            ("Healthcare Management – WHO OpenWHO", "https://openwho.org/"),
        ],
        "references": [
            ("WHO Learning Hub", "https://www.who.int/emergencies/learning-hub"),
            ("OpenWHO Free Courses", "https://openwho.org/"),
            ("PubMed Central (Research)", "https://www.ncbi.nlm.nih.gov/pmc/"),
        ],
    },
    "Agriculture": {
        "youtube": [
            ("Sustainable Agriculture – UC Davis (YouTube)", "https://www.youtube.com/watch?v=1Bz1LLQGi3s"),
            ("Plant Science / Agronomy – NPTEL", "https://www.youtube.com/watch?v=Z7Xa4Bw7JMk"),
            ("Precision Agriculture & GIS – Esri", "https://www.youtube.com/watch?v=lRWD0SjKJP8"),
        ],
        "references": [
            ("FAO e-Learning Academy", "https://www.fao.org/elearning/"),
            ("CGIAR Research Outputs", "https://www.cgiar.org/research/"),
            ("AgriInfo Online Courses", "https://agriinfo.in/"),
        ],
    },
    "Tourism": {
        "youtube": [
            ("Tourism Management – NPTEL", "https://www.youtube.com/watch?v=0FnXGkbMH-4"),
            ("Hospitality Management Full Course", "https://www.youtube.com/watch?v=CyJlZ-1Hmx8"),
        ],
        "references": [
            ("UNWTO E-Learning Platform", "https://elearning.unwto.org/"),
            ("Cornell School of Hotel Administration (edX)", "https://www.edx.org/school/cornellx"),
            ("Hospitality Net", "https://www.hospitalitynet.org/"),
        ],
    },
    "Law": {
        "youtube": [
            ("Introduction to Law – Yale Law School (Coursera)", "https://www.youtube.com/watch?v=7V6pMBQzrzo"),
            ("Contract Law Full Course", "https://www.youtube.com/watch?v=e_sDhSsHVqA"),
        ],
        "references": [
            ("Coursera – Law Courses", "https://www.coursera.org/browse/social-sciences/law"),
            ("LII (Legal Information Institute – Cornell)", "https://www.law.cornell.edu/"),
            ("edX – Law & Legal Studies", "https://www.edx.org/learn/law"),
        ],
    },
    "Ethics": {
        "youtube": [
            ("Ethics – Crash Course Philosophy", "https://www.youtube.com/watch?v=FOoffXFpAlU"),
            ("AI Ethics – MIT Open Learning", "https://www.youtube.com/watch?v=aGwYtUzMQUk"),
        ],
        "references": [
            ("MIT Moral Reasoning (OpenCourseWare)", "https://ocw.mit.edu/courses/24-02-moral-problems-and-the-good-life-fall-2008/"),
            ("AI Fairness 360 (IBM)", "https://aif360.mybluemix.net/"),
            ("Stanford Encyclopedia of Philosophy", "https://plato.stanford.edu/"),
        ],
    },
    "Energy": {
        "youtube": [
            ("Renewable Energy Full Course – NPTEL", "https://www.youtube.com/watch?v=gGWKMnT7f9U"),
            ("Solar Energy Engineering – Delft University (edX)", "https://www.youtube.com/watch?v=nFrjHFbBD0Q"),
        ],
        "references": [
            ("IEA (International Energy Agency) Reports", "https://www.iea.org/reports"),
            ("IRENA (Renewable Energy)", "https://www.irena.org/"),
            ("MIT Energy Initiative", "https://energy.mit.edu/education/"),
        ],
    },
}

def get_study_resources(domain):
    """Return study resources for a given course domain."""
    return STUDY_RESOURCES.get(domain, {
        "youtube": [
            ("Khan Academy – Free Courses", "https://www.khanacademy.org/"),
            ("Coursera Top Courses", "https://www.coursera.org/browse"),
            ("edX Free Courses", "https://www.edx.org/"),
        ],
        "references": [
            ("MIT OpenCourseWare", "https://ocw.mit.edu/"),
            ("Google Scholar", "https://scholar.google.com/"),
        ],
    })


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .recommendation-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .explanation-box {
        background: #e3f2fd;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        color: #1a1a1a;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)
  
# Load dataset for metadata
@st.cache_data
def load_dataset():
    base = os.path.dirname(__file__)
    return pd.read_csv(os.path.join(base, "dataset", "dataset_processed_for_modeling.csv"))

# Cache recommendations for better performance
@st.cache_data(ttl=3600, show_spinner="🔄 Loading cached recommendations...")
def get_recommendations(student_id, top_n, job_priority):
    """Get recommendations with caching for better performance"""
    return recommend(student_id, top_n=top_n, job_priority=job_priority)

# Cache new user recommendations
@st.cache_data(ttl=3600, show_spinner="🔄 Generating recommendations...")
def get_new_user_recommendations(skills, interests, gpa, top_n, job_priority):
    """Get recommendations for new users with detailed explanations"""
    return recommend_new_user(skills, interests, gpa, top_n=top_n, job_priority=job_priority, explain=True)

# Get student profile
def get_student_profile(df, student_id):
    student_data = df[df['student_id'] == student_id]
    if student_data.empty:
        return None
    
    return {
        'gpa': student_data['previous_GPA'].mean(),
        'attendance': student_data['attendance_rate'].mean(),
        'risk': student_data['risk_score'].mean(),
        'courses_taken': len(student_data),
        'degree': student_data['degree_program'].iloc[0] if 'degree_program' in student_data.columns else "Unknown"
    }

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 AI Course Recommender</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Hybrid ML + Google Gemini XAI</p>', unsafe_allow_html=True)
    
    # User type selector
    st.divider()
    user_type = st.radio(
        "👤 Select User Type",
        options=["🎓 Existing Student", "✨ New User (No Account)"],
        horizontal=True,
        help="Choose your user type to get personalized recommendations"
    )
    st.divider()
    
    # Load data
    df = load_dataset()
    available_students = df['student_id'].unique()
    available_domains = df['course_domain'].unique().tolist() if 'course_domain' in df.columns else []
    
    if user_type == "🎓 Existing Student":
        show_existing_student_ui(df, available_students, available_domains)
    else:
        show_new_user_ui(df, available_domains)


def show_existing_student_ui(df, available_students, available_domains):
    """UI for existing students with student_id"""
    with st.sidebar:
        st.header("📋 Your Preferences")
        
        # Student ID input with autocomplete
        student_id = st.selectbox(
            "Student ID",
            options=available_students[:100],  # Show first 100
            index=0,
            help="Select your student ID"
        )
        
        # Or enter manually
        manual_id = st.text_input("Or enter Student ID manually", "")
        if manual_id:
            student_id = manual_id
        
        st.divider()
        
        # Number of recommendations
        num_recs = st.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=20,
            value=10,
            step=1,
            help="How many courses do you want to see?"
        )
        
        # Domain filter
        domains = st.multiselect(
            "Preferred Domains (Optional)",
            options=sorted(available_domains),
            default=None,
            help="Filter by specific academic domains"
        )
        
        # Difficulty preference
        difficulty_range = st.slider(
            "Difficulty Range",
            min_value=0.0,
            max_value=1.0,
            value=(0.0, 1.0),
            step=0.1,
            help="0 = Easy, 1 = Very Hard"
        )
        
        # Job market priority
        job_priority = st.select_slider(
            "Career Focus",
            options=["Interest First", "Balanced", "Job Market First"],
            value="Balanced",
            help="Prioritize your interests or job market demand?"
        )
        
        st.divider()
        
        # Generate button with better styling
        generate_btn = st.button(
            "🔍 Get Recommendations", 
            type="primary", 
            use_container_width=True,
            help="Click to generate personalized course recommendations"
        )
        
        # Show helpful tip
        if not generate_btn:
            st.info("💡 Tip: Click the button above to see your recommendations!")
    
    # Main content
    if generate_btn:
        # Show immediate feedback
        st.toast("🚀 Processing your request...", icon="⏳")
        
        # Get student profile
        profile = get_student_profile(df, student_id)
        
        if profile is None:
            st.error(f"❌ Student ID '{student_id}' not found in database!")
            st.info("💡 Try selecting from the dropdown or check your ID.")
            return
        
        # Generate recommendations with progress
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            progress_text.text("📊 Step 1/4: Loading student profile...")
            progress_bar.progress(25)
            
            progress_text.text("🤖 Step 2/4: Running AI models (Hybrid ML + Gemini)...")
            progress_bar.progress(50)
            
            # Get recommendations (with caching)
            recs = get_recommendations(student_id, num_recs, job_priority)
            
            progress_text.text("🔍 Step 3/4: Applying filters...")
            progress_bar.progress(75)
            
            # Apply filters
            if domains:
                recs = recs[recs['course_domain'].isin(domains)] if 'course_domain' in recs.columns else recs
            
            if 'course_difficulty' in recs.columns:
                recs = recs[
                    (recs['course_difficulty'] >= difficulty_range[0]) &
                    (recs['course_difficulty'] <= difficulty_range[1])
                ]
            
            progress_text.text("✅ Step 4/4: Preparing recommendations...")
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_text.empty()
            progress_bar.empty()
            
            # Store in session
            st.session_state['recommendations'] = recs
            st.session_state['profile'] = profile
            st.session_state['student_id'] = student_id
            
            st.success(f"✅ Generated {len(recs)} recommendations successfully!")
            
        except Exception as e:
            progress_text.empty()
            progress_bar.empty()
            st.error(f"❌ Error generating recommendations: {str(e)}")
            st.info("💡 Make sure all model artifacts are present and try again.")
            with st.expander("🔍 Error Details"):
                st.code(str(e))
            return
    
    # Display results if available
    if 'recommendations' in st.session_state:
        recs = st.session_state['recommendations']
        profile = st.session_state['profile']
        sid = st.session_state['student_id']
        
        if len(recs) == 0:
            st.warning("⚠️ No recommendations match your filters. Try adjusting them!")
            return
        
        # Student Profile Dashboard
        st.header(f"👤 Student Profile: {sid}")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "GPA",
                f"{profile['gpa']:.2f}/4.0",
                delta="Good" if profile['gpa'] >= 3.0 else "Improving"
            )
        
        with col2:
            st.metric(
                "Attendance",
                f"{profile['attendance']*100:.0f}%",
                delta="Excellent" if profile['attendance'] >= 0.8 else "Needs Work"
            )
        
        with col3:
            risk_label = "Low" if profile['risk'] < 0.3 else "Moderate" if profile['risk'] < 0.6 else "High"
            st.metric(
                "Risk Level",
                risk_label,
                delta="Good" if profile['risk'] < 0.4 else "Monitor"
            )
        
        with col4:
            st.metric(
                "Courses Taken",
                profile['courses_taken']
            )
        
        with col5:
            st.metric(
                "Degree Program",
                profile['degree'][:15] + "..." if len(profile['degree']) > 15 else profile['degree']
            )
        
        st.divider()
        
        # Visualizations
        st.header("📊 Recommendation Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Algorithm breakdown
            fig1 = go.Figure(data=[go.Pie(
                labels=['Collaborative Filtering<br>(40%)', 'Content Match<br>(35%)', 
                       'Success Prediction<br>(20%)', 'Job Market<br>(5%)'],
                values=[40, 35, 20, 5],
                hole=0.4,
                marker=dict(colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'])
            )])
            fig1.update_layout(
                title="How Recommendations Are Generated",
                showlegend=True,
                height=350
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Domain distribution
            if 'course_domain' in recs.columns:
                domain_counts = recs['course_domain'].value_counts().head(8)
                fig2 = px.bar(
                    x=domain_counts.index,
                    y=domain_counts.values,
                    labels={'x': 'Domain', 'y': 'Number of Courses'},
                    title="Recommendations by Domain",
                    color=domain_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig2.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Recommendation Cards with count
        st.header(f"📚 Your Top {len(recs)} Personalized Recommendations")
        
        # Show filter results if applicable
        if len(recs) < num_recs:
            st.info(f"ℹ️ Showing {len(recs)} of {num_recs} recommendations after applying your filters.")
        
        # Add tabs for different views
        tab1, tab2 = st.tabs(["📋 List View", "📊 Detailed View"])
        
        with tab1:
            # Compact list view
            for idx, rec in recs.head(10).iterrows():
                with st.expander(f"**{idx + 1}. {rec['course_name']}** - Score: ⭐ {rec['final_score']:.3f}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Course ID:** {rec['course_id']}")
                        if 'course_domain' in rec:
                            st.markdown(f"**Domain:** {rec['course_domain']}")
                        
                        # Progress bars for metrics
                        st.markdown("**Key Metrics:**")
                        st.progress(rec['p_success'], text=f"Success Rate: {rec['p_success']*100:.1f}%")
                        st.progress(rec['job_market'], text=f"Job Market: {rec['job_market']*100:.1f}%")
                        st.progress(rec['cbf_score'], text=f"Interest Match: {rec['cbf_score']*100:.1f}%")
                    
                    with col2:
                        # Action buttons
                        st.button("📄 View Details", key=f"view_{idx}", use_container_width=True)
                        st.button("⭐ Add to Wishlist", key=f"wish_{idx}", use_container_width=True)
                    
                    # Gemini explanation with better formatting
                    st.markdown("---")
                    st.markdown(f"""
                    <div style="background: linear-gradient(to right, #e3f2fd, #f3e5f5); 
                         border-left: 5px solid #2196F3; padding: 1.2rem; 
                         border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="display: flex; align-items: center; margin-bottom: 0.8rem;">
                            <span style="font-size: 24px; margin-right: 10px;">🤖</span>
                            <strong style="color: #1565C0; font-size: 17px;">AI Advisor Recommendation</strong>
                        </div>
                        <p style="color: #212121; font-size: 15px; line-height: 1.8; 
                           margin: 0; font-weight: 500; text-align: justify;">
                            {rec['explanation']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Study resources panel
                    domain = rec.get('course_domain', '')
                    resources = get_study_resources(domain)
                    with st.expander("📚 Study Resources & References", expanded=False):
                        res_col1, res_col2 = st.columns(2)
                        with res_col1:
                            st.markdown("**🎬 YouTube Tutorials**")
                            for title, url in resources.get("youtube", []):
                                st.markdown(f"- [▶ {title}]({url})")
                        with res_col2:
                            st.markdown("**🔗 References & Docs**")
                            for title, url in resources.get("references", []):
                                st.markdown(f"- [🌐 {title}]({url})")

        with tab2:
            # Detailed cards view
            for idx, rec in recs.head(10).iterrows():
                st.markdown(f"### {idx + 1}. {rec['course_name']}")
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Course ID:** {rec['course_id']}")
                    if 'course_domain' in rec:
                        st.markdown(f"**📊 Domain:** {rec['course_domain']}")
                    if 'course_difficulty' in rec:
                        st.markdown(f"**📈 Difficulty:** {rec['course_difficulty']*100:.0f}%")
                
                with col2:
                    st.metric("Overall Score", f"{rec['final_score']:.3f}")
                    st.metric("Success Rate", f"{rec['p_success']*100:.1f}%")
                
                with col3:
                    st.metric("Job Market", f"{rec['job_market']*100:.1f}%")
                    st.metric("CF Score", f"{rec['cf_score']*100:.1f}%")
                
                # Score breakdown chart
                scores = {
                    'CF': rec['cf_score'] * 100,
                    'CBF': rec['cbf_score'] * 100,
                    'Success': rec['p_success'] * 100,
                    'Job': rec['job_market'] * 100
                }
                fig = px.bar(
                    x=list(scores.keys()),
                    y=list(scores.values()),
                    labels={'x': 'Component', 'y': 'Score (%)'},
                    title=f"Score Breakdown for {rec['course_name']}",
                    color=list(scores.values()),
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=250, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                
                # Gemini explanation with enhanced formatting
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea15, #764ba215); 
                     border: 2px solid #667eea; border-radius: 12px; 
                     padding: 1.5rem; margin: 1rem 0;">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 28px; margin-right: 12px;">🤖</span>
                        <strong style="color: #667eea; font-size: 18px; 
                               text-transform: uppercase; letter-spacing: 1px;">AI Recommendation Analysis</strong>
                    </div>
                    <div style="background: white; padding: 1.2rem; border-radius: 8px; 
                         border-left: 4px solid #667eea;">
                        <p style="color: #2c3e50; font-size: 16px; line-height: 1.9; 
                           margin: 0; font-weight: 500; text-align: justify;">
                            {rec['explanation']}
                        </p>
                    </div>
                    <div style="margin-top: 1rem; font-size: 13px; color: #7f8c8d; 
                         font-style: italic; text-align: right;">
                        ✨ Generated by Google Gemini AI
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.button("📄 View Full Details", key=f"detail_{idx}", use_container_width=True)
                with col2:
                    st.button("⭐ Add to Wishlist", key=f"wishlist_{idx}", use_container_width=True)
                with col3:
                    st.button("✉️ Email Advisor", key=f"email_{idx}", use_container_width=True)
                with col4:
                    st.button("✅ Enroll Now", key=f"enroll_{idx}", use_container_width=True)

                # Study resources panel
                domain = rec.get('course_domain', '')
                resources = get_study_resources(domain)
                with st.expander("📚 Study Resources & References", expanded=False):
                    res_col1, res_col2 = st.columns(2)
                    with res_col1:
                        st.markdown("**🎬 YouTube Tutorials**")
                        for title, url in resources.get("youtube", []):
                            st.markdown(f"- [▶ {title}]({url})")
                    with res_col2:
                        st.markdown("**🔗 References & Docs**")
                        for title, url in resources.get("references", []):
                            st.markdown(f"- [🌐 {title}]({url})")

                st.divider()
        
        # Export options
        st.header("📥 Export Your Recommendations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = recs.to_csv(index=False)
            st.download_button(
                "📄 Download CSV",
                csv,
                f"recommendations_{sid}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            # Create a simple text report
            report = f"Course Recommendations for {sid}\n\n"
            for idx, rec in recs.iterrows():
                report += f"{idx + 1}. {rec['course_name']} (Score: {rec['final_score']:.3f})\n"
                report += f"   {rec['explanation']}\n\n"
            
            st.download_button(
                "📝 Download Report",
                report,
                f"report_{sid}.txt",
                "text/plain",
                use_container_width=True
            )
        
        with col3:
            st.button(
                "📧 Email to Advisor",
                use_container_width=True,
                help="Send recommendations to your academic advisor"
            )
    
    else:
        # Welcome message with instructions
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             padding: 2rem; border-radius: 15px; color: white; text-align: center;">
            <h2 style="color: white; margin-bottom: 1rem;">👋 Welcome to AI Course Recommender!</h2>
            <p style="font-size: 18px; margin-bottom: 1.5rem;">
                Get personalized course recommendations powered by advanced AI
            </p>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px;">
                <h3 style="color: white;">🚀 Quick Start</h3>
                <p style="font-size: 16px; text-align: left; margin-left: 20%;">
                    1️⃣ Select your Student ID from the sidebar<br>
                    2️⃣ Adjust preferences (optional)<br>
                    3️⃣ Click "Get Recommendations"<br>
                    4️⃣ Review AI-powered suggestions!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Show some stats
        st.header("📊 System Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", f"{len(available_students):,}")
        
        with col2:
            st.metric("Total Courses", f"{df['course_id'].nunique():,}")
        
        with col3:
            st.metric("Academic Domains", len(available_domains))
        
        with col4:
            st.metric("Avg Success Rate", f"{df['final_grade'].mean():.1f}%")


def show_new_user_ui(df, available_domains):
    """UI for new users without student_id"""
    with st.sidebar:
        st.header("✨ New User Setup")
        st.info("💡 Enter your details to get personalized recommendations")
        
        # Skills selection (multi-select) + optional free-text
        skills_selected = st.multiselect(
            "🛠️ Your Skills",
            options=sorted(AVAILABLE_SKILLS),
            help="Select your strengths (you can also add other skills below)",
        )
        other_skills = st.text_input(
            "➕ Other Skills (comma-separated)",
            value="",
            help="Add any skills not in the list"
        )
        
        # Interests selection (multi-select from domains)
        interests_selected = st.multiselect(
            "💡 Interest Areas",
            options=sorted(available_domains),
            help="Choose the domains/topics that interest you",
        )
        
        # GPA input (precise)
        gpa = st.number_input(
            "📊 Your GPA",
            min_value=0.0,
            max_value=4.0,
            value=3.0,
            step=0.01,
            format="%.2f",
            help="Your current or expected GPA (0.0–4.0)"
        )
        
        st.divider()
        
        # Number of recommendations
        num_recs = st.slider(
            "Number of Recommendations",
            min_value=5,
            max_value=20,
            value=10,
            step=1,
            help="How many courses do you want to see?"
        )
        
        # Job market priority
        job_priority = st.select_slider(
            "Career Focus",
            options=["Interest First", "Balanced", "Job Market First"],
            value="Balanced",
            help="Prioritize your interests or job market demand?"
        )
        
        st.divider()
        
        # Generate button
        generate_btn = st.button(
            "🔍 Get Recommendations", 
            type="primary", 
            use_container_width=True,
            help="Click to generate personalized course recommendations"
        )
        
        if not generate_btn:
            st.info("💡 Fill in your details and click the button above!")
    
    # Main content
    if generate_btn:
        # Validation
        parsed_other_skills = [s.strip() for s in other_skills.split(',') if s.strip()]
        all_skills = list(skills_selected) + parsed_other_skills
        if not all_skills:
            st.error("❌ Please select or enter at least one skill!")
            return
        if not interests_selected:
            st.warning("⚠️ Interest areas help improve recommendations. Consider selecting them!")
        
        # Show immediate feedback
        st.toast("🚀 Analyzing your profile...", icon="⏳")
        
        # Generate recommendations
        progress_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            progress_text.text("📊 Step 1/3: Building your skill profile...")
            progress_bar.progress(33)
            
            progress_text.text("🤖 Step 2/3: Running AI recommendation engine...")
            progress_bar.progress(66)
            
            # Get recommendations
            skills_str = ", ".join(all_skills)
            interests_str = ", ".join(interests_selected)
            recs = get_new_user_recommendations(
                skills=skills_str,
                interests=interests_str,
                gpa=gpa,
                top_n=num_recs,
                job_priority=job_priority
            )
            
            progress_text.text("✨ Step 3/3: Finalizing recommendations...")
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_text.empty()
            progress_bar.empty()
            
            if recs.empty:
                st.warning("⚠️ No matching courses found. Try broader interest areas.")
                return
            
            # Success message
            st.success(f"✅ Found {len(recs)} personalized recommendations!")
            st.toast("🎉 Recommendations ready!", icon="✨")
            
            # Display profile summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Your GPA", f"{gpa:.2f}/4.0")
            with col2:
                st.metric("🛠️ Skills Listed", len(all_skills))
            with col3:
                avg_success = recs['p_success'].mean()
                st.metric("🎯 Avg Success Rate", f"{avg_success*100:.1f}%")
            
            st.divider()
            
            # Recommendations table
            st.subheader("📚 Recommended Courses")
            
            for idx, row in recs.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h3 style="color: #1E88E5; margin-bottom: 0.5rem;">
                            {idx+1}. {row['course_name']}
                        </h3>
                        <p style="color: #666; margin-bottom: 1rem;">
                            📁 {row['course_domain']} | 🎯 Match Score: {row['final_score']:.3f}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Score breakdown
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("🔍 Content Match", f"{row['cbf_score']:.2f}")
                    with col2:
                        st.metric("✅ Success Rate", f"{row['p_success']*100:.1f}%")
                    with col3:
                        st.metric("💼 Job Demand", f"{row['job_market']:.2f}")
                    with col4:
                        st.metric("⚠️ Risk", f"{row['risk_score']:.2f}")
                    
                    # Show detailed explanation
                    if 'explanation' in row and row['explanation']:
                        with st.expander("📖 View Detailed AI Analysis", expanded=(idx < 3)):
                            st.markdown(row['explanation'])

                    # Study resources panel
                    nu_domain = row.get('course_domain', '')
                    nu_resources = get_study_resources(nu_domain)
                    with st.expander("📚 Study Resources & References", expanded=False):
                        nr_col1, nr_col2 = st.columns(2)
                        with nr_col1:
                            st.markdown("**🎬 YouTube Tutorials**")
                            for title, url in nu_resources.get("youtube", []):
                                st.markdown(f"- [▶ {title}]({url})")
                        with nr_col2:
                            st.markdown("**🔗 References & Docs**")
                            for title, url in nu_resources.get("references", []):
                                st.markdown(f"- [🌐 {title}]({url})")

                    st.divider()
            
            # Visualizations
            st.subheader("📊 Analysis Dashboard")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Score breakdown
                fig_scores = go.Figure(data=[
                    go.Bar(
                        x=['Content Match', 'Success Rate', 'Job Demand'],
                        y=[
                            recs['cbf_score'].mean(),
                            recs['p_success'].mean(),
                            recs['job_market'].mean()
                        ],
                        marker_color=['#2196F3', '#4CAF50', '#FF9800']
                    )
                ])
                fig_scores.update_layout(
                    title="Average Component Scores",
                    yaxis_title="Score",
                    showlegend=False,
                    height=350
                )
                st.plotly_chart(fig_scores, use_container_width=True)
            
            with col2:
                # Domain distribution
                domain_counts = recs['course_domain'].value_counts().head(5)
                fig_domains = px.pie(
                    values=domain_counts.values,
                    names=domain_counts.index,
                    title="Recommended Domains",
                    hole=0.4
                )
                fig_domains.update_layout(height=350)
                st.plotly_chart(fig_domains, use_container_width=True)
            
            # Download options
            st.divider()
            st.subheader("💾 Export Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = recs.to_csv(index=False)
                st.download_button(
                    "📊 Download CSV",
                    csv,
                    f"new_user_recommendations.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Generate text report
                report = f"Course Recommendations for New User\n"
                report += f"{'='*50}\n\n"
                report += f"Profile:\n"
                report += f"- Skills: {skills_str}\n"
                report += f"- Interests: {interests_str}\n"
                report += f"- GPA: {gpa:.2f}\n"
                report += f"- Job Priority: {job_priority}\n\n"
                report += f"Top {len(recs)} Recommendations:\n"
                report += f"{'-'*50}\n\n"
                for idx, rec in recs.iterrows():
                    report += f"{idx+1}. {rec['course_name']}\n"
                    report += f"   Domain: {rec['course_domain']}\n"
                    report += f"   Match Score: {rec['final_score']:.3f}\n"
                    report += f"   Success Rate: {rec['p_success']*100:.1f}%\n\n"
                
                st.download_button(
                    "📝 Download Report",
                    report,
                    f"new_user_report.txt",
                    "text/plain",
                    use_container_width=True
                )
            
            with col3:
                st.button(
                    "🔄 Get More Recommendations",
                    use_container_width=True,
                    on_click=st.cache_data.clear,
                    help="Clear cache and generate fresh recommendations"
                )
            
            # Add to Dataset & Retrain Section
            st.divider()
            st.subheader("💾 Save Profile & Retrain Models")
            
            st.info("""
            **📌 Add Your Profile to Training Data**
            
            Save your profile and course history to the dataset. This will:
            - Add your data to improve future recommendations
            - Allow system to learn from your preferences
            - Help train better models for similar students
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Save My Profile to Dataset", type="primary", use_container_width=True):
                    with st.spinner("Saving your profile..."):
                        if save_new_user_to_dataset(profile):
                            st.success("✅ Profile saved successfully!")
                            st.balloons()
                            
                            # Store flag in session
                            st.session_state['profile_saved'] = True
                        else:
                            st.error("❌ Failed to save profile")
            
            with col2:
                if st.session_state.get('profile_saved', False):
                    if st.button("🔄 Retrain All Models", type="secondary", use_container_width=True):
                        with st.spinner("Retraining models... This may take a few minutes."):
                            if retrain_models():
                                st.success("🎉 Models retrained! Restart app to use updated models.")
                                st.info("💡 Tip: Use Ctrl+C to stop and run `streamlit run streamlit_app.py` again")
                else:
                    st.button(
                        "🔄 Retrain All Models", 
                        disabled=True, 
                        use_container_width=True,
                        help="Save your profile first to enable retraining"
                    )
        
        except Exception as e:
            st.error(f"❌ Error generating recommendations: {str(e)}")
            st.info("💡 Please check your inputs and try again.")
    
    else:
        # Welcome message for new users
        st.markdown("""
        <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
             padding: 2rem; border-radius: 15px; color: white; text-align: center;">
            <h2 style="color: white; margin-bottom: 1rem;">👋 Welcome New User!</h2>
            <p style="font-size: 18px; margin-bottom: 1.5rem;">
                Get AI-powered course recommendations based on your skills and interests
            </p>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 10px;">
                <h3 style="color: white;">🚀 How It Works</h3>
                <p style="font-size: 16px; text-align: left; margin-left: 15%;">
                    1️⃣ Enter your technical skills<br>
                    2️⃣ Specify your interest areas<br>
                    3️⃣ Input your current GPA<br>
                    4️⃣ Set career focus preference<br>
                    5️⃣ Click "Get Recommendations"
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)


def save_new_user_to_dataset(student_profile):
    """Save new user data to the dataset and trigger retraining"""
    import pandas as pd
    from datetime import datetime
    
    try:
        # Load existing dataset
        dataset_path = os.path.join("dataset", "sri_lanka_course_recommendation_dataset.csv")
        
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
        else:
            st.error("❌ Dataset not found! Generate dataset first.")
            return False
        
        # Generate unique student ID
        existing_ids = df['student_id'].unique()
        new_id = f"S{len(existing_ids) + 1:04d}"
        
        # Create records for each past course
        new_records = []
        for course in student_profile.get('past_courses', []):
            record = {
                'student_id': new_id,
                'gender': 'Unknown',  # Could be added to form
                'age': 20,  # Could be calculated from year
                'university': student_profile.get('university', 'Unknown'),
                'degree_program': student_profile.get('degree_program', 'Unknown'),
                'current_year': int(student_profile.get('current_year', 'Year 1').split()[-1]),
                'course_id': f"C{len(df['course_id'].unique()) + len(new_records) + 1:03d}",
                'course_name': course['course_name'],
                'course_domain': course['course_domain'],
                'course_difficulty': course['difficulty'],
                'previous_GPA': student_profile.get('overall_gpa', 3.0),
                'attendance_rate': student_profile.get('attendance_rate', 0.85),
                'risk_score': 1.0 - (student_profile.get('overall_gpa', 3.0) / 4.0 * 0.6 + 
                                    student_profile.get('attendance_rate', 0.85) * 0.4),
                'final_grade': course['grade'],
                'course_interest': course['interest'],
                'job_market_demand_2035': course.get('career_relevance', 0.7),
                'employability_relevance': course.get('career_relevance', 0.7),
                'course_skills': student_profile.get('skills', ''),
                'recommended': 1
            }
            new_records.append(record)
        
        if not new_records:
            st.warning("⚠️ No course data to save. Add at least one past course.")
            return False
        
        # Append to dataset
        new_df = pd.DataFrame(new_records)
        updated_df = pd.concat([df, new_df], ignore_index=True)
        
        # Save updated dataset
        updated_df.to_csv(dataset_path, index=False)
        
        st.success(f"✅ Added {len(new_records)} course records for student {new_id}")
        return True
        
    except Exception as e:
        st.error(f"❌ Error saving data: {str(e)}")
        return False


def retrain_models():
    """Retrain all models with updated dataset"""
    import subprocess
    import shutil
    from datetime import datetime
    
    st.subheader("🔄 Retraining Models")
    
    # Backup old models
    backup_dir = os.path.join("Models", f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    
    try:
        progress_container = st.container()
        
        with progress_container:
            # Step 1: Backup existing models
            st.info("📦 Step 1/5: Backing up existing models...")
            progress_bar = st.progress(0)
            
            if os.path.exists("Models"):
                os.makedirs(backup_dir, exist_ok=True)
                for file in os.listdir("Models"):
                    if file.endswith(('.pkl', '.npy')):
                        shutil.copy2(
                            os.path.join("Models", file),
                            os.path.join(backup_dir, file)
                        )
                st.success(f"✅ Backed up to {backup_dir}")
            progress_bar.progress(20)
            
            # Step 2: Preprocess data
            st.info("🔧 Step 2/5: Preprocessing dataset...")
            result = subprocess.run(
                ["python", "Scripts/preprocessing/preprocess.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                st.error(f"❌ Preprocessing failed: {result.stderr}")
                return False
            
            st.success("✅ Preprocessing complete")
            progress_bar.progress(40)
            
            # Step 3: Train success model
            st.info("🤖 Step 3/5: Training success prediction model...")
            result = subprocess.run(
                ["python", "Scripts/training/train_success_model.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                st.warning(f"⚠️ Success model training had issues: {result.stderr[:200]}")
            else:
                st.success("✅ Success model trained")
            progress_bar.progress(60)
            
            # Step 4: Train collaborative filtering
            st.info("🤖 Step 4/5: Training collaborative filtering...")
            result = subprocess.run(
                ["python", "Scripts/training/train_cf.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                st.warning(f"⚠️ CF training had issues: {result.stderr[:200]}")
            else:
                st.success("✅ Collaborative filtering trained")
            progress_bar.progress(80)
            
            # Step 5: Create student labels (optional)
            st.info("📊 Step 5/5: Creating student-level labels...")
            result = subprocess.run(
                ["python", "Scripts/preprocessing/create_student_level_labels.py"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()
            )
            
            if result.returncode != 0:
                st.warning(f"⚠️ Label creation had issues: {result.stderr[:200]}")
            else:
                st.success("✅ Labels created")
            progress_bar.progress(100)
            
            st.success("🎉 All models retrained successfully!")
            
            # Option to delete backup
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Delete Old Models Backup", type="secondary"):
                    shutil.rmtree(backup_dir)
                    st.success(f"✅ Deleted backup: {backup_dir}")
                    st.rerun()
            
            with col2:
                if st.button("♻️ Restore Old Models", type="secondary"):
                    for file in os.listdir(backup_dir):
                        shutil.copy2(
                            os.path.join(backup_dir, file),
                            os.path.join("Models", file)
                        )
                    st.success("✅ Restored old models")
                    st.rerun()
            
            return True
            
    except Exception as e:
        st.error(f"❌ Error during retraining: {str(e)}")
        with st.expander("🔍 Error Details"):
            st.code(str(e))
        return False


if __name__ == "__main__":
    main()
