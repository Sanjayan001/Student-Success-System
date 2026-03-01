import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join('database', 'student_success.db')

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

if __name__ == "__main__":
    init_db()