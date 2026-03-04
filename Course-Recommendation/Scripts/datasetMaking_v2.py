import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# --- CONFIGURABLE PARAMETERS ---
NUM_STUDENTS = 10000
TOTAL_RECORDS = 250000

# --- UNIVERSITY AND DEGREE DEFINITIONS ---
universities = [
    "University of Colombo", "University of Moratuwa", "University of Peradeniya",
    "University of Ruhuna", "University of Jaffna", "University of Kelaniya",
    "Sabaragamuwa University", "SLTC", "NSBM Green University", "KDU"
]

degree_programs = [
    "Information Technology", "Computer Science", "Data Science", "Artificial Intelligence",
    "Cybersecurity", "Electrical Engineering", "Mechanical Engineering",
    "Business Management", "Finance", "Tourism and Hospitality",
    "Medicine", "Nursing", "Law", "Agriculture", "Renewable Energy"
]

# --- REALISTIC COURSE CATALOG BY DOMAIN ---
realistic_courses = {
    # Data Science & AI Courses
    "Data Science": [
        ("Introduction to Data Science", 0.4, 0.85),
        ("Data Mining and Warehousing", 0.6, 0.80),
        ("Big Data Analytics", 0.7, 0.88),
        ("Statistical Learning", 0.65, 0.75),
        ("Data Visualization", 0.45, 0.70),
        ("Business Intelligence", 0.55, 0.78),
        ("Predictive Analytics", 0.70, 0.85),
        ("Time Series Analysis", 0.68, 0.72),
    ],
    
    "AI": [
        ("Introduction to Artificial Intelligence", 0.5, 0.90),
        ("Machine Learning", 0.70, 0.92),
        ("Deep Learning", 0.80, 0.95),
        ("Natural Language Processing", 0.75, 0.88),
        ("Computer Vision", 0.78, 0.90),
        ("Reinforcement Learning", 0.85, 0.87),
        ("Image Understanding and Processing", 0.72, 0.85),
        ("Neural Networks", 0.75, 0.90),
        ("AI Ethics and Governance", 0.40, 0.70),
        ("Generative AI", 0.80, 0.95),
    ],
    
    # Computer Science Core
    "Software Engineering": [
        ("Programming Fundamentals", 0.35, 0.75),
        ("Object-Oriented Programming", 0.50, 0.78),
        ("Data Structures and Algorithms", 0.70, 0.85),
        ("Software Engineering Principles", 0.60, 0.80),
        ("Web Development", 0.45, 0.82),
        ("Mobile Application Development", 0.60, 0.85),
        ("Cloud Computing", 0.65, 0.90),
        ("DevOps and CI/CD", 0.68, 0.85),
        ("Microservices Architecture", 0.75, 0.88),
        ("Software Testing and QA", 0.55, 0.75),
    ],
    
    "Cybersecurity": [
        ("Introduction to Cybersecurity", 0.45, 0.88),
        ("Network Security", 0.65, 0.85),
        ("Ethical Hacking", 0.70, 0.90),
        ("Cryptography", 0.75, 0.82),
        ("Security Operations", 0.68, 0.85),
        ("Penetration Testing", 0.72, 0.88),
        ("Incident Response", 0.65, 0.80),
        ("Security Architecture", 0.70, 0.83),
    ],
    
    "Networking": [
        ("Computer Networks", 0.55, 0.70),
        ("Network Administration", 0.60, 0.72),
        ("Wireless Networks", 0.58, 0.68),
        ("Internet of Things", 0.65, 0.82),
        ("Network Design", 0.68, 0.70),
        ("5G and Next Generation Networks", 0.72, 0.85),
    ],
    
    # Engineering Courses
    "Electrical": [
        ("Circuit Analysis", 0.65, 0.68),
        ("Digital Electronics", 0.60, 0.70),
        ("Power Systems", 0.70, 0.72),
        ("Control Systems", 0.72, 0.68),
        ("Embedded Systems", 0.68, 0.75),
        ("Signal Processing", 0.70, 0.70),
        ("Renewable Energy Systems", 0.65, 0.80),
    ],
    
    "Mechanical": [
        ("Engineering Mechanics", 0.60, 0.65),
        ("Thermodynamics", 0.70, 0.68),
        ("Fluid Mechanics", 0.68, 0.65),
        ("Manufacturing Processes", 0.62, 0.70),
        ("CAD/CAM", 0.55, 0.72),
        ("Robotics", 0.75, 0.82),
        ("Mechatronics", 0.72, 0.78),
    ],
    
    # Business & Management
    "Management": [
        ("Principles of Management", 0.40, 0.65),
        ("Project Management", 0.55, 0.75),
        ("Human Resource Management", 0.50, 0.68),
        ("Operations Management", 0.60, 0.70),
        ("Strategic Management", 0.65, 0.72),
        ("Organizational Behavior", 0.45, 0.65),
        ("Supply Chain Management", 0.62, 0.75),
    ],
    
    "Finance": [
        ("Financial Accounting", 0.55, 0.72),
        ("Corporate Finance", 0.65, 0.75),
        ("Investment Analysis", 0.68, 0.78),
        ("Financial Markets", 0.60, 0.75),
        ("Risk Management", 0.70, 0.80),
        ("Financial Technology", 0.65, 0.85),
    ],
    
    # Healthcare
    "Healthcare": [
        ("Medical Informatics", 0.60, 0.85),
        ("Healthcare Management", 0.55, 0.80),
        ("Public Health", 0.50, 0.75),
        ("Epidemiology", 0.65, 0.78),
        ("Health Data Analytics", 0.68, 0.88),
        ("Telemedicine", 0.60, 0.85),
    ],
    
    # Other Domains
    "Tourism": [
        ("Tourism Management", 0.45, 0.60),
        ("Hospitality Operations", 0.50, 0.65),
        ("Event Management", 0.48, 0.68),
        ("Sustainable Tourism", 0.52, 0.70),
    ],
    
    "Agriculture": [
        ("Agricultural Science", 0.50, 0.50),
        ("Precision Agriculture", 0.60, 0.65),
        ("Agribusiness Management", 0.55, 0.58),
        ("Sustainable Farming", 0.52, 0.62),
    ],
    
    "Energy": [
        ("Renewable Energy Technologies", 0.65, 0.85),
        ("Solar Power Systems", 0.60, 0.82),
        ("Energy Management", 0.62, 0.78),
        ("Smart Grid Technology", 0.68, 0.80),
    ],
    
    "Ethics": [
        ("Technology Ethics", 0.40, 0.65),
        ("Data Privacy and Law", 0.55, 0.72),
        ("Professional Ethics", 0.38, 0.60),
    ],
    
    "Law": [
        ("Cyber Law", 0.58, 0.72),
        ("Intellectual Property", 0.60, 0.70),
        ("Business Law", 0.55, 0.68),
    ],
}

# Skills mapping for each domain
domain_skills = {
    "Data Science": ["Python", "R", "SQL", "Data Analysis", "Statistics", "Tableau"],
    "AI": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "Neural Networks"],
    "Software Engineering": ["Java", "Python", "Git", "Agile", "Docker", "Kubernetes"],
    "Cybersecurity": ["Cyber Defense", "Penetration Testing", "Security Auditing", "Firewalls", "Encryption"],
    "Networking": ["TCP/IP", "Network Design", "Cisco", "Network Security", "IoT"],
    "Electrical": ["Circuit Design", "MATLAB", "Power Systems", "Control Theory"],
    "Mechanical": ["CAD", "SolidWorks", "Thermodynamics", "Manufacturing"],
    "Management": ["Project Management", "Leadership", "Communication", "Strategy"],
    "Finance": ["Accounting", "Financial Modeling", "Excel", "Risk Analysis"],
    "Healthcare": ["Medical Data", "Health Informatics", "Patient Care", "HIPAA"],
    "Tourism": ["Customer Service", "Event Planning", "Marketing"],
    "Agriculture": ["Crop Management", "Sustainability", "Agritech"],
    "Energy": ["Renewable Systems", "Solar Design", "Energy Efficiency"],
    "Ethics": ["AI Ethics", "Data Privacy", "Legal Compliance"],
    "Law": ["Legal Writing", "Contract Law", "Compliance"],
}

# Build comprehensive course catalog
courses = []
course_id = 1

for domain, course_list in realistic_courses.items():
    for course_name, difficulty, job_demand in course_list:
        # Get relevant skills for this domain
        skills = random.sample(domain_skills.get(domain, ["General Skills"]), 
                              min(3, len(domain_skills.get(domain, ["General Skills"]))))
        
        course = {
            "course_id": f"C{course_id:03}",
            "course_name": course_name,
            "course_domain": domain,
            "course_difficulty": round(difficulty, 2),
            "job_market_demand_2035": round(job_demand, 2),
            "course_skills": ", ".join(skills)
        }
        courses.append(course)
        course_id += 1

courses_df = pd.DataFrame(courses)
print(f"✅ Created {len(courses_df)} realistic courses")

# Student generation
students = []
for i in range(NUM_STUDENTS):
    student = {
        "student_id": f"S{i+1:05}",
        "gender": random.choice(["Male", "Female"]),
        "age": random.randint(18, 26),
        "university": random.choice(universities),
        "degree_program": random.choice(degree_programs),
        "current_year": random.randint(1, 4),
        "previous_GPA": round(np.clip(np.random.normal(3.0, 0.5), 0, 4), 2),
        "attendance_rate": round(np.clip(np.random.normal(0.85, 0.1), 0.4, 1.0), 2)
    }
    students.append(student)

students_df = pd.DataFrame(students)
print(f"✅ Created {len(students_df)} students")

# Combine students and courses to create synthetic records with realistic patterns
records = []
print("⏳ Generating student-course records...")

for _ in range(TOTAL_RECORDS):
    student = random.choice(students)
    course_row = courses_df.sample(1).iloc[0]
    
    # Calculate course interest based on degree program alignment
    degree_domain_alignment = {
        "Data Science": ["Data Science", "AI", "Software Engineering"],
        "Computer Science": ["Software Engineering", "AI", "Cybersecurity"],
        "Artificial Intelligence": ["AI", "Data Science", "Software Engineering"],
        "Cybersecurity": ["Cybersecurity", "Networking", "Software Engineering"],
        "Information Technology": ["Software Engineering", "Networking", "Cybersecurity"],
    }
    
    # Check if course domain aligns with degree
    aligned_domains = degree_domain_alignment.get(student["degree_program"], [])
    if course_row["course_domain"] in aligned_domains:
        course_interest = round(np.clip(np.random.normal(0.8, 0.1), 0.5, 1.0), 2)
    else:
        course_interest = round(np.clip(np.random.normal(0.5, 0.15), 0.2, 0.9), 2)
    
    # Risk score calculation (inverse of performance indicators)
    base_risk = 1.0 - (student["previous_GPA"] / 4.0) * 0.5 - student["attendance_rate"] * 0.3
    risk_score = round(np.clip(base_risk + np.random.normal(0, 0.1), 0, 1), 2)
    
    # Final grade calculation (influenced by GPA, attendance, interest, difficulty, risk)
    performance_factor = (
        student["previous_GPA"] / 4.0 * 0.4 +
        student["attendance_rate"] * 0.3 +
        course_interest * 0.2 +
        (1 - course_row["course_difficulty"]) * 0.1
    )
    
    final_grade = round(np.clip(
        performance_factor * 100 + np.random.normal(0, 10),
        0, 100
    ), 1)
    
    # Adjust risk based on actual performance
    if final_grade < 50:
        risk_score = min(1.0, risk_score + 0.2)
    
    # Determine if recommended (high interest, good alignment, manageable difficulty)
    recommended = (
        course_interest >= 0.7 and 
        risk_score < 0.4 and
        course_row["course_difficulty"] < 0.75
    )
    
    # Employability relevance
    if course_row["job_market_demand_2035"] > 0.8:
        employability = "High"
    elif course_row["job_market_demand_2035"] > 0.65:
        employability = "Medium"
    else:
        employability = "Low"
    
    record = {
        **student,
        "course_id": course_row["course_id"],
        "course_name": course_row["course_name"],
        "course_domain": course_row["course_domain"],
        "course_difficulty": course_row["course_difficulty"],
        "risk_score": risk_score,
        "final_grade": final_grade,
        "course_interest": course_interest,
        "job_market_demand_2035": course_row["job_market_demand_2035"],
        "employability_relevance": employability,
        "course_skills": course_row["course_skills"],
        "recommended": recommended
    }
    records.append(record)

dataset = pd.DataFrame(records)

# Add NaN indicators
nan_cols = ['previous_GPA', 'attendance_rate', 'course_difficulty', 
             'job_market_demand_2035', 'course_interest', 'final_grade', 'risk_score']
for col in nan_cols:
    dataset[f"{col}_was_nan"] = False

# Create course_text for TF-IDF
dataset['course_text'] = (
    dataset['course_name'] + ' ' + 
    dataset['course_skills'] + ' ' + 
    dataset['course_domain']
)

# Add indices for CF
dataset['student_idx'] = dataset.groupby('student_id').ngroup()
dataset['course_idx'] = dataset.groupby('course_id').ngroup()

# Save with error handling
import os
os.makedirs("dataset", exist_ok=True)
output_file = "dataset/sri_lanka_course_recommendation_dataset.csv"
try:
    dataset.to_csv(output_file, index=False)
    print(f"✅ Dataset saved: {output_file}")
except PermissionError:
    # File is open - try with timestamp
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"dataset/sri_lanka_course_recommendation_dataset_{timestamp}.csv"
    dataset.to_csv(output_file, index=False)
    print(f"⚠️  Original file was open. Saved as: {output_file}")
    print(f"💡 Close the original file and rename this one to 'sri_lanka_course_recommendation_dataset.csv'")

print(f"📊 Total records: {len(dataset)}")
print(f"👨‍🎓 Unique students: {dataset['student_id'].nunique()}")
print(f"📚 Unique courses: {dataset['course_id'].nunique()}")
print(f"\n📋 Sample courses:")
print(courses_df[['course_id', 'course_name', 'course_domain']].head(15).to_string(index=False))
