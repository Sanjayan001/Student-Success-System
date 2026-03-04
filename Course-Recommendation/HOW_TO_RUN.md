# How to Run — SmartEduPath: Sri Lankan Course Recommendation System

## Prerequisites

- Python 3.12 or higher installed
- Windows PowerShell or Command Prompt
- Project folder: `c:\Users\MALSHIKA\Documents\SLIIT\SmartEduPath\Research-Project`

---

## Step 1 — Open Terminal and Navigate to Project

Open **PowerShell** and run:

```powershell
cd "c:\Users\MALSHIKA\Documents\SLIIT\SmartEduPath\Research-Project"
```

---

## Step 2 — Set Up the Virtual Environment (First Time Only)

If `.venv` does not exist yet, create it:

```powershell
python -m venv .venv
```

---

## Step 3 — Install Dependencies (First Time Only)

Install all required packages inside `.venv`:

```powershell
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
```

> This installs: streamlit, pandas, numpy, scikit-learn, xgboost, lightgbm, shap, plotly, google-generativeai, and more.

---

## Step 4 — Run the Web Application

Use this command to launch the Streamlit app inside `.venv`:

```powershell
& "c:\Users\MALSHIKA\Documents\SLIIT\SmartEduPath\Research-Project\.venv\Scripts\python.exe" -m streamlit run "c:\Users\MALSHIKA\Documents\SLIIT\SmartEduPath\Research-Project\streamlit_app.py"
```

**Shortcut** (if you are already inside the project folder):

```powershell
& ".\.venv\Scripts\python.exe" -m streamlit run streamlit_app.py
```

---

## Step 5 — Open the App in Your Browser

After running, the terminal will show:

```
You can now view your Streamlit app in your browser.
Local URL:  http://localhost:8501
```

Open your browser and go to:

```
http://localhost:8501
```

---

## Step 6 — Using the App

The app supports **two user flows**:

### Option A — Existing Student
1. Select **"Existing Student"** radio button
2. Pick a Student ID from the dropdown (e.g., `S00001`, `S00123`, `S00500`)
3. Set number of recommendations (1–20)
4. Adjust job priority slider (0.0–1.0)
5. Toggle **Show Explanations** if needed
6. Click **Get Recommendations**

**Output:** Student profile card · Recommended courses · Bar & Radar charts · AI explanations

---

### Option B — New User (No Account)
1. Select **"New User (No Account)"** radio button
2. Multi-select your **skills** (Python, Java, Machine Learning, AWS, etc.)
3. Multi-select your **interest areas** (Computer Science, Data Science, AI, etc.)
4. Enter your **GPA** (0.00–4.00)
5. Enter **career focus** (optional)
6. Click **Get Recommendations**

**Output:** Predicted specialization path · Recommended courses · Skills to develop · Success rate predictions

---

## Step 7 — Stop the App

Press `Ctrl + C` in the terminal to stop the server.

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `streamlit: command not found` | Use `& ".venv\Scripts\python.exe" -m streamlit run streamlit_app.py` |
| `ModuleNotFoundError` | Run: `& ".venv\Scripts\python.exe" -m pip install -r requirements.txt` |
| `FileNotFoundError` for models | Train models first: `& ".venv\Scripts\python.exe" Scripts/master_training_script.py` |
| Port 8501 already in use | Add `--server.port 8502` at the end of the run command |
| App loads slowly | Clear Streamlit cache: press **C** in the app or delete `C:\Users\MALSHIKA\.streamlit\cache\` |

---

## Important File Locations

| File | Path |
|---|---|
| **Main App** | `Research-Project\streamlit_app.py` |
| **Core Engine** | `Research-Project\Scripts\utils\hybrid_infer.py` |
| **Models** | `Research-Project\Models\` |
| **Dataset** | `Research-Project\dataset\dataset_processed_for_modeling.csv` |
| **Requirements** | `Research-Project\requirements.txt` |

---

## Advanced Run Options

```powershell
# Run on a different port
& ".\.venv\Scripts\python.exe" -m streamlit run streamlit_app.py --server.port 8080

# Auto-reload on file save (development mode)
& ".\.venv\Scripts\python.exe" -m streamlit run streamlit_app.py --server.runOnSave true

# Run without auto-opening browser
& ".\.venv\Scripts\python.exe" -m streamlit run streamlit_app.py --server.headless true
```

---

## Test Student IDs

Try these IDs in the Existing Student dropdown:

```
S00001   S00123   S00500   S01000   S03532   S09855
```

---

## Project Folder Structure

```
Research-Project/
├── streamlit_app.py          ← Main web application
├── requirements.txt          ← Python dependencies
├── .venv/                    ← Virtual environment (do not edit)
├── dataset/
│   └── dataset_processed_for_modeling.csv
├── Models/                   ← Trained ML model files (.npy, .pkl)
└── Scripts/
    ├── utils/
    │   └── hybrid_infer.py   ← Recommendation engine
    ├── training/             ← Model training scripts
    └── evaluation/           ← Evaluation & fairness scripts
```

---

*Last Updated: March 4, 2026*
