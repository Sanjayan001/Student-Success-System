# Institutional-Level Student Profiling & Clustering (Admin Dashboard)

This project supports **university administrators / academic advisors** to upload **semester survey data** and automatically:
- validate schema
- preprocess and convert survey ranges to numeric
- engineer Phase 1–4 features (mean + trend)
- train/load **KMeans** clustering (default k=3)
- generate **3-cluster profiles** (names + explanation + interventions)
- provide **XAI-style drivers** (top differentiating features)
- export institutional and individual reports

## Run (Windows / VS Code)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run dashboard/app.py
```

Default admin: `admin / admin123`

## Semester uploads
Place new semester CSVs in:
`data/semester_uploads/`  
Or upload directly via the dashboard.

## Outputs
- Trained artifacts: `models/`
- Processed data: `data/processed/`
- Reports: `reports/`
