# 🚀 SmartEduPath Organized Workflow Guide

**Quick Reference for the New Organized Structure**

---

## 📂 Where Everything Lives

```
✅ All Datasets    → dataset/
✅ All Models      → Models/
✅ All Scripts     → Scripts/ (with subdirectories)
✅ Main UI         → streamlit_app.py (root)
✅ Documentation   → *.md files (root)
```

---

## 🎯 Complete Workflow (Step-by-Step)

### **STEP 1: Generate Dataset** 
```bash
python Scripts/datasetMaking_v2.py
```
**Creates:**
- `dataset/sri_lanka_course_recommendation_dataset.csv` (10,000 students, 93 realistic courses)

---

### **STEP 2: Preprocess Data**
```bash
python Scripts/preprocessing/preprocess.py
```
**Creates:**
- `dataset/dataset_clean.csv`
- `dataset/dataset_processed_for_modeling.csv`
- `Models/tfidf_course.pkl`
- `Models/course_index_map.pkl`
- `Models/scaler.pkl`
- `Models/student_encoder.pkl`
- `Models/course_encoder.pkl`

---

### **STEP 3: Create Student Labels**
```bash
python Scripts/preprocessing/create_student_level_labels.py
```
**Creates:**
- `dataset/student_level_labeled.csv`

---

### **STEP 4: Train Success Model**
```bash
python Scripts/training/train_success_model.py
```
**Creates:**
- `Models/logreg_success.pkl`
- `Models/success_scaler.pkl`

---

### **STEP 5: Train Collaborative Filtering**
```bash
python Scripts/training/train_cf.py
```
**Creates:**
- `Models/cf_alt_student_factors.npy`
- `Models/cf_alt_course_factors.npy`
- `Models/cf_alt_student_ids.npy`
- `Models/cf_alt_course_ids.npy`
- `Models/cf_alt_svd_model.pkl`
- `Models/cf_alt_user_encoder.pkl`
- `Models/cf_alt_item_encoder.pkl`

---

### **STEP 6: Train Specialization Model** (Optional)
```bash
python Scripts/training/train_specialization_model.py
```
**Creates:**
- `Models/spec_model_v2.pkl`
- `Models/spec_feature_cols_v2.pkl`
- `Models/spec_label_map_v2.pkl`

---

### **STEP 7: Run the System** 

#### **Option A: Web UI (Recommended)**
```bash
streamlit run streamlit_app.py
```
🌐 Opens at: http://localhost:8501

#### **Option B: Random Student CLI**
```bash
python Scripts/utils/random_student_predictor.py
```

#### **Option C: Python API**
```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'Scripts', 'utils'))

from hybrid_infer import recommend

# Get recommendations for existing student
recs = recommend(student_id="S0001", top_n=5)
print(recs)
```

---

## 🔄 Quick Commands Cheat Sheet

| Action | Command |
|--------|---------|
| **Generate new dataset** | `python Scripts/datasetMaking_v2.py` |
| **Preprocess data** | `python Scripts/preprocessing/preprocess.py` |
| **Train success model** | `python Scripts/training/train_success_model.py` |
| **Train CF model** | `python Scripts/training/train_cf.py` |
| **Launch web UI** | `streamlit run streamlit_app.py` |
| **Test random student** | `python Scripts/utils/random_student_predictor.py` |
| **Evaluate system** | `python Scripts/evaluation/evaluate_recommendations.py` |
| **Run tests** | `python Scripts/testing/test_new_features.py` |

---

## 📁 Folder Quick Reference

### **dataset/** - All CSV files
- Raw, clean, and processed datasets
- Student-level aggregated data
- Feature-engineered datasets

### **Models/** - All .pkl and .npy files
- Trained ML models
- Encoders and scalers
- TF-IDF vectorizers
- Embeddings

### **Scripts/training/** - Model training
- `train_success_model.py` - Success prediction
- `train_cf.py` - Collaborative filtering
- `train_specialization_model.py` - Specialization classifier
- `meta_learner.py` - Meta-learner

### **Scripts/preprocessing/** - Data preparation
- `datasetMaking_v2.py` - Generate realistic dataset
- `preprocess.py` - Main preprocessing pipeline
- `create_student_level_labels.py` - Aggregate student data
- `create_better_features.py` - Feature engineering

### **Scripts/evaluation/** - Performance analysis
- `evaluate_recommendations.py` - Quality metrics
- `compare_mmr_diversity.py` - Diversity analysis
- `visualize_model_accuracy.py` - Create charts

### **Scripts/testing/** - System validation
- `test_new_features.py` - Test new additions
- `test_final_system.py` - End-to-end test
- `test_enhanced_gemini.py` - Gemini integration test

### **Scripts/utils/** - Core modules
- `hybrid_infer.py` - Main recommendation engine
- `random_student_predictor.py` - Random student handler
- `shap_lime_explainer.py` - SHAP & LIME explanations
- `gemini_explainer.py` - Gemini AI explanations

---

## 🎓 Using Random Student Input

### **Interactive Mode:**
```bash
python Scripts/utils/random_student_predictor.py
```
Then follow the prompts to enter:
- Student GPA
- Attendance rate
- Interest areas
- Past courses

### **Programmatic Mode:**
```python
from Scripts.utils.random_student_predictor import get_random_student_recommendations

student = {
    'student_id': 'NEW001',
    'previous_GPA': 3.2,
    'attendance_rate': 0.85,
    'interest_areas': ['AI', 'Data Science', 'Machine Learning'],
    'past_courses': ['Introduction to Programming', 'Statistics', 'Databases']
}

recommendations = get_random_student_recommendations(
    student_profile=student,
    top_n=5,
    job_priority='high',
    use_shap=True,
    use_lime=True,
    use_gemini=True
)
```

---

## 🔧 Troubleshooting

### **Import Errors**
If you see `ModuleNotFoundError`:
```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'Scripts', 'utils'))
```

### **File Not Found**
All scripts auto-detect `BASE_DIR`. If issues persist:
```python
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### **Missing Models**
Train models in this order:
1. `python Scripts/training/train_success_model.py`
2. `python Scripts/training/train_cf.py`
3. (Optional) `python Scripts/training/train_specialization_model.py`

### **Missing Datasets**
Generate and preprocess:
1. `python Scripts/datasetMaking_v2.py`
2. `python Scripts/preprocessing/preprocess.py`

---

## 📊 Realistic Course Examples

Our dataset includes 93 industry-standard courses like:

**AI/ML:**
- Deep Learning
- Computer Vision
- Natural Language Processing
- Image Understanding and Processing (IUP)
- Reinforcement Learning

**Data Science:**
- Big Data Analytics
- Statistical Learning
- Time Series Analysis
- Data Visualization

**Software Engineering:**
- Microservices Architecture
- DevOps and CI/CD
- Cloud Native Applications
- System Design

**Cybersecurity:**
- Ethical Hacking
- Cryptography
- Penetration Testing
- Security Operations

---

## ✅ Verification Checklist

Before running the system, ensure:

- [ ] Virtual environment activated (`.venv\Scripts\activate`)
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] Dataset generated (`dataset/sri_lanka_course_recommendation_dataset.csv` exists)
- [ ] Data preprocessed (`dataset/dataset_processed_for_modeling.csv` exists)
- [ ] Success model trained (`Models/logreg_success.pkl` exists)
- [ ] CF model trained (`Models/cf_alt_student_factors.npy` exists)
- [ ] Gemini API key set (`.env` file with `GEMINI_API_KEY`)

---

## 🎉 Success!

Your system is now fully organized and ready to use!

**Next Steps:**
1. Generate dataset if not done: `python Scripts/datasetMaking_v2.py`
2. Run preprocessing: `python Scripts/preprocessing/preprocess.py`
3. Train models: `python Scripts/training/train_success_model.py` and `python Scripts/training/train_cf.py`
4. Launch UI: `streamlit run streamlit_app.py`

---

## 📚 Documentation Links

- **Full Structure Guide**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Setup Instructions**: [SETUP_GUIDE_V2.md](SETUP_GUIDE_V2.md)
- **Feature Upgrades**: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)
- **Main README**: [README.md](README.md)

---

**🚀 Happy Recommending!**
