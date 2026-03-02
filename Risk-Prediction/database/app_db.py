import sqlite3
from datetime import datetime
import os

import os
import sqlite3

# This gets the folder: .../Risk-Prediction/database/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'student_success.db')

# Add this print so you can see the path in the terminal when you run Streamlit
print(f"🧬 Database Connection Active: {DB_PATH}")

def init_db():
    """Initializes the high-capacity database for student risk tracking."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # We create a table that stores the core prediction result 
    # and dumps the 70+ variables into a JSON 'blob' for the Counselor.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS risk_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            prediction_date TIMESTAMP,
            risk_score REAL,
            risk_status TEXT,
            full_data_json TEXT  -- This will store all 70+ variables
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ High-Capacity Database Ready.")

def initialize_intervention_table():
    """Initializes the High-Fidelity Simulation Table (9 Levers)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # DROP allows us to upgrade the schema to the 'Deep' version
    cursor.execute("DROP TABLE IF EXISTS intervention_goals")
    
    # High-Fidelity Schema matching your Simulation Theater
    create_query = """
    CREATE TABLE intervention_goals (
        student_id TEXT PRIMARY KEY,
        target_cgpa REAL,
        target_attendance REAL,
        target_failed_subs REAL,
        target_motivation REAL,
        target_confidence REAL,
        target_stress REAL,
        target_sleep REAL,
        target_relaxation REAL,
        target_support REAL,
        predicted_risk_reduction REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    try:
        cursor.execute(create_query)
        conn.commit()
        print("✅ Intervention Goals (Deep Schema): Operational")
    except Exception as e:
        print(f"❌ Schema Error: {e}")
    finally:
        conn.close()

def save_prediction(student_id, score, status, data_dict):
    """Saves the student profile and AI result."""
    import json
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO risk_history (student_id, prediction_date, risk_score, risk_status, full_data_json)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
          score, status, json.dumps(data_dict)))
    conn.commit()
    conn.close()

def setup_all_tables():
    """The Master Initializer for the Research Database."""
    print("🚀 Starting Database Synchronization...")
    init_db()
    initialize_intervention_table()
    print("🏁 All Research Tables are Live.")

# THIS IS THE ONLY BLOCK YOU NEED AT THE BOTTOM
if __name__ == "__main__":
    setup_all_tables()