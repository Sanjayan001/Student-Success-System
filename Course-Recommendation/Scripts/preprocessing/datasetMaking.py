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
NUM_COURSES = 200
TOTAL_RECORDS = 250000

# --- UNIVERSITY, DEGREE, AND COURSE DEFINITIONS ---
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

course_domains = [
    "AI", "Data Science", "Cybersecurity", "Networking", "Software Engineering",
    "Mechanical", "Electrical", "Management", "Finance", "Tourism",
    "Healthcare", "Agriculture", "Energy", "Ethics", "Law"
]

# Job demand mapping for next 10 years (2035 forecast)
job_demand_map = {
    "AI": (0.85, 1.0),
    "Data Science": (0.8, 0.95),
    "Cybersecurity": (0.8, 0.95),
    "Networking": (0.6, 0.8),
    "Software Engineering": (0.7, 0.9),
    "Mechanical": (0.5, 0.75),
    "Electrical": (0.6, 0.8),
    "Management": (0.5, 0.75),
    "Finance": (0.55, 0.8),
    "Tourism": (0.4, 0.7),
    "Healthcare": (0.75, 0.95),
    "Agriculture": (0.3, 0.6),
    "Energy": (0.65, 0.9),
    "Ethics": (0.4, 0.7),
    "Law": (0.5, 0.75)
}

# Course generation
courses = []
for i in range(NUM_COURSES):
    domain = random.choice(course_domains)
    difficulty = round(np.clip(np.random.normal(0.6, 0.2), 0, 1), 2)
    demand_range = job_demand_map[domain]
    job_demand = round(random.uniform(*demand_range), 2)
    course = {
        "course_id": f"C{i+1:03}",
        "course_name": f"{domain} Fundamentals {i+1}",
        "course_domain": domain,
        "course_difficulty": difficulty,
        "job_market_demand_2035": job_demand,
        "course_skills": ", ".join(random.sample([
            "Python", "Java", "Data Analysis", "Machine Learning", "Networking",
            "Cyber Defense", "Cloud Computing", "AI Ethics", "Project Management",
            "Statistics", "Renewable Systems", "Accounting", "Microbiology", "Legal Writing"
        ], k=3))
    }
    courses.append(course)

courses_df = pd.DataFrame(courses)

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

# Combine students and courses to create synthetic records
records = []
for _ in range(TOTAL_RECORDS):
    student = random.choice(students)
    course = random.choice(courses)

    risk_score = round(np.clip(1 - (student["previous_GPA"] / 4) + np.random.normal(0, 0.05), 0, 1), 2)
    interest = round(np.clip(np.random.normal(0.75, 0.2), 0, 1), 2)
    final_grade = round(np.clip(np.random.normal(student["previous_GPA"] * 25, 10), 0, 100), 1)
    employability = (
        "High" if course["job_market_demand_2035"] > 0.75 else
        "Medium" if course["job_market_demand_2035"] > 0.5 else
        "Low"
    )
    recommended = True if (interest > 0.6 and risk_score < 0.6 and final_grade > 60) else False

    record = {
        "student_id": student["student_id"],
        "gender": student["gender"],
        "age": student["age"],
        "university": student["university"],
        "degree_program": student["degree_program"],
        "current_year": student["current_year"],
        "course_id": course["course_id"],
        "course_name": course["course_name"],
        "course_domain": course["course_domain"],
        "course_difficulty": course["course_difficulty"],
        "previous_GPA": student["previous_GPA"],
        "attendance_rate": student["attendance_rate"],
        "risk_score": risk_score,
        "final_grade": final_grade,
        "course_interest": interest,
        "job_market_demand_2035": course["job_market_demand_2035"],
        "employability_relevance": employability,
        "course_skills": course["course_skills"],
        "recommended": recommended
    }
    records.append(record)

dataset = pd.DataFrame(records)

# Shuffle & save
dataset = dataset.sample(frac=1).reset_index(drop=True)
dataset.to_csv("sri_lanka_course_recommendation_dataset.csv", index=False)

print("✅ Dataset generated successfully!")
print("Rows:", len(dataset))
print("Saved to: sri_lanka_course_recommendation_dataset.csv")
print(dataset.head())
