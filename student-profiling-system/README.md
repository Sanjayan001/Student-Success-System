# 🎓 Institutional Student Success & Retention Intelligence
**Automated Behavioral Segmentation & Explainable AI (XAI) Advising Framework**

## 📌 Executive Overview
The **Student Success System** is a production-grade Machine Learning pipeline and Executive Dashboard designed for university administrators and academic advisors. By leveraging Unsupervised Machine Learning (K-Means Clustering) and Temporal Feature Engineering, this system autonomously processes raw semester survey data to discover distinct psychological and academic student profiles. 

Rather than functioning as a "black box," this platform features a robust **Explainable AI (XAI)** interface, translating complex multi-dimensional distances into actionable, plain-English intervention strategies for counseling departments.

## ✨ Core System Features
* **🧠 Unsupervised Behavioral Segmentation:** Dynamically groups students into mathematically proven cohorts (e.g., *High Performing*, *Average/Moderate*, *At-Risk*) without human bias.
* **⏳ Temporal Feature Engineering:** Calculates behavioral momentum (e.g., *Stress Trend*, *Motivation Trend*) across 4 distinct phases of the semester to detect early burnout.
* **🛡️ Data Drift Guardrails:** Continuously calculates live scientific validation metrics (Silhouette Score & Calinski-Harabasz Index) on every new dataset upload to monitor for shifts in institutional behavioral trends.
* **🔍 Explainable AI (XAI) Diagnostics:** Utilizes live ANOVA statistical testing and variance deltas to explicitly tell counselors *why* a student was flagged, accompanied by interactive Behavioral Radar Charts.
* **📊 One-Click Roster Extraction:** Generates targeted, department-specific intervention CSV lists for immediate deployment by academic advisors.

---

## 🔬 Scientific Methodology & Validation
This pipeline was mathematically validated against Centroid-based, Agglomerative, and Density-based algorithms. **K-Means (k=3)** was selected as the optimal intelligence engine after rigorous benchmarking:
1. **Hyperparameter Tuning:** k=3 was mathematically validated via the Within-Cluster Sum of Squares (WCSS) Elbow Method.
2. **Algorithmic Benchmarking:** K-Means outperformed both Hierarchical Clustering and DBSCAN, achieving superior Cluster Density (Calinski-Harabasz) and Partition Separation (Davies-Bouldin) while guaranteeing 0% unclassified noise.
3. **Missing Data Handling:** Robust Median Imputation is utilized to protect centroid calculations from extreme outliers.

---

## 🚀 Quick Start (Windows Setup)

### 1. Installation
Clone the repository and set up your virtual environment using Windows PowerShell:

```powershell
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Install required dependencies
python -m pip install -r requirements.txt
```

### 2. Launching the MLOps Dashboard
Start the Streamlit Executive UI:
```powershell
python -m streamlit run dashboard/app.py
```

### 3. Secure Authentication
The system is protected by secure admin routing. 
* **Default Admin ID:** `admin`
* **Default Password:** `admin123`

---

## 📂 System Architecture & Workflow

### Directory Structure
* `dashboard/` - Contains the Adaptive Dark/Light Mode Streamlit UI and secure routing.
* `src/` - The core mathematical engine (Preprocessing, Feature Engineering, K-Means Clustering, ANOVA XAI).
* `data/semester_uploads/` - Target directory for raw institutional CSV ingests.
* `models/` - Serialized ML models generated post-execution.
* `reports/` - Output directory for generated CSV intervention rosters.

### Executive Workflow
1. **Ingest:** Administrator securely logs in and uploads the end-of-semester CSV containing demographic, academic, and 4-phase psychological data.
2. **Compile:** The system validates the schema, applies temporal engineering, and executes the K-Means pipeline.
3. **Review:** Administrator verifies the structural integrity of the clusters via the live Data Drift Monitor (Silhouette Score).
4. **Intervene:** Advisors query specific `Student_IDs` to review XAI diagnostics or export department-wide targeted rosters.

---
*Developed as a Master's Level Research Application bridging the gap between Unsupervised Machine Learning and Institutional Academic Advising.*

