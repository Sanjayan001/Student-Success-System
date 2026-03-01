import pandas as pd
import sys
import os

# Let the test find your src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_contract import validate_dataset

def test_data_contract_missing_columns():
    """Test that the system correctly identifies missing critical columns."""
    # Create fake, broken data (missing the CGPA column)
    fake_data = pd.DataFrame({
        "student_id": ["STU001"],
        "Attendance_Percentage": [85]
    })
    
    missing_cols, _ = validate_dataset(fake_data)
    
    # The test passes if the system successfully catches the error
    assert "CGPA" in missing_cols