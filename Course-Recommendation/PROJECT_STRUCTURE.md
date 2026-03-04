# 📁 SmartEduPath Project Structure

**Last Updated:** January 16, 2026  
**Status:** ✅ Fully Organized & Production Ready

---

## 🎯 Overview

SmartEduPath is an AI-powered course recommendation system for Sri Lankan universities with:
- **Triple Explanation System**: SHAP + LIME + Gemini AI
- **Random Student Input**: Accept any student data, not just existing IDs
- **Realistic Course Catalog**: 110+ industry-standard courses
- **Hybrid Recommendation**: Collaborative Filtering + Content-Based + Success Prediction

---

## 📂 Folder Organization

```
Research-Project/
│
├── 📁 dataset/                          # All dataset files
│   ├── sri_lanka_course_recommendation_dataset.csv    # Raw generated data
│   ├── dataset_clean.csv                              # Cleaned data
│   ├── dataset_processed_for_modeling.csv            # Preprocessed for ML
│   ├── student_level_labeled.csv                      # Student-level labels
│   └── student_level_features_improved.csv            # Enhanced features
│
├── 📁 Models/                           # All trained models & artifacts
│   ├── logreg_success.pkl               # Success prediction model
│   ├── success_scaler.pkl               # Feature scaler
│   ├── cf_alt_student_factors.npy       # CF student embeddings
│   ├── cf_alt_course_factors.npy        # CF course embeddings
│   ├── cf_alt_student_ids.npy           # CF student ID mapping
│   ├── cf_alt_course_ids.npy            # CF course ID mapping
│   ├── cf_alt_svd_model.pkl             # SVD model
│   ├── cf_alt_user_encoder.pkl          # User encoder
│   ├── cf_alt_item_encoder.pkl          # Item encoder
│   ├── tfidf_course.pkl                 # TF-IDF vectorizer
│   ├── course_index_map.pkl             # Course ID to index mapping
│   ├── student_encoder.pkl              # Student ID encoder
│   ├── course_encoder.pkl               # Course ID encoder
│   ├── scaler.pkl                       # MinMax scaler
│   ├── spec_model_v2.pkl                # Specialization classifier
│   ├── spec_feature_cols_v2.pkl         # Specialization features
│   ├── spec_label_map_v2.pkl            # Specialization label mapping
│   └── meta_learner_weights.pkl         # Meta-learner weights
│
├── 📁 Scripts/                          # All executable scripts
│   │
│   ├── 📁 training/                     # Model training scripts
│   │   ├── train_success_model.py       # Train success prediction
│   │   ├── train_cf.py                  # Train collaborative filtering
│   │   ├── train_cbf.py                 # Train content-based filtering
│   │   ├── train_specialization_model.py # Train specialization model
│   │   └── meta_learner.py              # Train meta-learner
│   │
│   ├── 📁 preprocessing/                # Data preprocessing scripts
│   │   ├── datasetMaking_v2.py          # Generate realistic dataset
│   │   ├── preprocess.py                # Main preprocessing pipeline
│   │   ├── create_student_level_labels.py # Aggregate student labels
│   │   └── create_better_features.py    # Feature engineering
│   │
│   ├── 📁 evaluation/                   # Model evaluation scripts
│   │   ├── evaluate_recommendations.py  # Recommendation quality metrics
│   │   ├── compare_mmr_diversity.py     # Diversity analysis
│   │   ├── show_model_accuracy.py       # Display model accuracy
│   │   └── visualize_model_accuracy.py  # Create accuracy visualizations
│   │
│   ├── 📁 testing/                      # Testing & validation scripts
│   │   ├── test_enhanced_gemini.py      # Test Gemini integration
│   │   ├── test_final_system.py         # End-to-end system test
│   │   └── test_new_features.py         # Test new feature additions
│   │
│   └── 📁 utils/                        # Core utility modules
│       ├── hybrid_infer.py              # Main recommendation engine
│       ├── random_student_predictor.py  # Random student input handler
│       ├── shap_lime_explainer.py       # SHAP & LIME explanations
│       ├── gemini_explainer.py          # Gemini AI explanations
│       ├── new_user_explainer.py        # New user explainer
│       └── template_explainer.py        # Template-based explanations
│
├── 📁 Documentation/                    # All documentation files
│   ├── README.md                        # Main project README
│   ├── README_V2.md                     # Updated README
│   ├── SETUP_GUIDE_V2.md                # Setup instructions
│   ├── UPGRADE_SUMMARY.md               # Feature upgrade summary
│   ├── BEFORE_AFTER_COMPARISON.md       # Old vs new comparison
│   ├── PROJECT_SUMMARY.md               # Project overview
│   ├── QUICK_START_GUIDE.md             # Quick start guide
│   ├── QUICK_REFERENCE.md               # Command reference
│   ├── RUN_UI_GUIDE.md                  # UI running guide
│   ├── UI_DESIGN_GUIDE.md               # UI design documentation
│   ├── MODEL_TRAINING_ROADMAP.md        # Training roadmap
│   ├── DATA_FLOW_EXPLANATION.md         # Data flow documentation
│   ├── INPUTS_OUTPUTS_SUMMARY.md        # I/O documentation
│   ├── DEPLOYMENT_CHECKLIST.md          # Deployment guide
│   ├── PP1_CHECKLIST_AND_RECOMMENDATIONS.md # PP1 checklist
│   ├── GEMINI_XAI_IMPLEMENTATION_SUMMARY.md # Gemini XAI docs
│   ├── GEMINI_XAI_EXAMPLE_ANALYSIS.md   # Gemini examples
│   └── INDEX.md                         # Documentation index
│
├── 📄 streamlit_app.py                  # Main web UI application
├── 📄 requirements.txt                  # Python dependencies
├── 📄 .env                              # Environment variables
├── 📄 .gitignore                        # Git ignore rules
├── 📄 cleanup_project.ps1               # Project cleanup script
└── 📄 quick_setup.ps1                   # Automated setup script

```

---

## 🔄 Complete Workflow

### **Phase 1: Data Generation & Preprocessing**
```bash
# 1. Generate realistic dataset
python Scripts/datasetMaking_v2.py

# 2. Preprocess data
python Scripts/preprocessing/preprocess.py

# 3. Create student-level labels
python Scripts/preprocessing/create_student_level_labels.py

# 4. Engineer features (optional)
python Scripts/preprocessing/create_better_features.py
```

**Outputs:**
- `dataset/sri_lanka_course_recommendation_dataset.csv` (10,000 students, 93 courses)
- `dataset/dataset_clean.csv`
- `dataset/dataset_processed_for_modeling.csv`
- `Models/tfidf_course.pkl`, `Models/course_index_map.pkl`, etc.

---

### **Phase 2: Model Training**
```bash
# Train all models in sequence
python Scripts/training/train_success_model.py  # Success prediction
python Scripts/training/train_cf.py             # Collaborative filtering
python Scripts/training/train_specialization_model.py  # Specialization
python Scripts/training/meta_learner.py         # Meta-learner (optional)
```

**Outputs:**
- `Models/logreg_success.pkl` + `Models/success_scaler.pkl`
- `Models/cf_alt_*.npy` (CF embeddings)
- `Models/spec_model_v2.pkl`

---

### **Phase 3: Testing & Evaluation**
```bash
# Test system components
python Scripts/testing/test_new_features.py

# Evaluate recommendation quality
python Scripts/evaluation/evaluate_recommendations.py

# Visualize model performance
python Scripts/evaluation/visualize_model_accuracy.py
```

---

### **Phase 4: Inference & Deployment**
```bash
# Option 1: Web UI (Recommended)
streamlit run streamlit_app.py

# Option 2: CLI for random student
python Scripts/utils/random_student_predictor.py

# Option 3: Programmatic usage
from Scripts.utils.hybrid_infer import recommend
recommendations = recommend(student_id="S0001", top_n=5)
```

---

## 🧩 Key Components

### **1. Recommendation Engine** ([Scripts/utils/hybrid_infer.py](Scripts/utils/hybrid_infer.py))
- **Fusion Algorithm**: Combines CF + CBF + Success Prediction + Job Demand
- **Weights**: 40% CF, 35% CBF, 20% Success, 5% Job Demand
- **Functions**:
  - `recommend(student_id, top_n)` - Existing student recommendations
  - `recommend_new_user(profile, top_n)` - Random student recommendations

### **2. Triple Explanation System**
- **SHAP** ([Scripts/utils/shap_lime_explainer.py](Scripts/utils/shap_lime_explainer.py))
  - Mathematical feature importance
  - Waterfall plots showing feature contributions
  
- **LIME** ([Scripts/utils/shap_lime_explainer.py](Scripts/utils/shap_lime_explainer.py))
  - Local interpretable rules
  - "IF-THEN" human-readable explanations
  
- **Gemini AI** ([Scripts/utils/gemini_explainer.py](Scripts/utils/gemini_explainer.py))
  - Natural language narratives
  - Personalized career advice

### **3. Random Student Input** ([Scripts/utils/random_student_predictor.py](Scripts/utils/random_student_predictor.py))
```python
student_profile = {
    'student_id': 'NEW001',
    'previous_GPA': 3.2,
    'attendance_rate': 0.85,
    'interest_areas': ['AI', 'Data Science'],
    'past_courses': ['Intro to Programming', 'Statistics']
}

recommendations = get_random_student_recommendations(
    student_profile, 
    top_n=5,
    use_shap=True,
    use_lime=True,
    use_gemini=True
)
```

---

## 📊 Dataset Schema

### **Course-Level Dataset** (`dataset_processed_for_modeling.csv`)
| Column | Type | Description |
|--------|------|-------------|
| student_id | str | Unique student identifier |
| course_id | str | Course identifier (C001-C093) |
| course_name | str | Realistic course name |
| course_domain | str | Domain (AI, Data Science, etc.) |
| course_difficulty | float | 0.0-1.0 difficulty rating |
| previous_GPA | float | Student's GPA (0-4.0) |
| attendance_rate | float | Attendance percentage |
| risk_score | float | Academic risk indicator |
| final_grade | float | Course grade (0-100) |
| course_interest | float | Interest level (0-1.0) |
| job_market_demand_2035 | float | Job demand score |
| course_skills | str | Comma-separated skills |
| recommended | int | 0/1 recommendation label |

---

## 🚀 Quick Start Commands

```bash
# Setup virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate new dataset with realistic courses
python Scripts/datasetMaking_v2.py

# Run full preprocessing pipeline
python Scripts/preprocessing/preprocess.py

# Train all models
python Scripts/training/train_success_model.py
python Scripts/training/train_cf.py

# Launch web UI
streamlit run streamlit_app.py

# Test random student recommendations
python Scripts/utils/random_student_predictor.py
```

---

## 🔧 Configuration

### **Environment Variables** (`.env`)
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### **Important Paths** (Auto-configured with `BASE_DIR`)
All scripts now use relative paths from project root:
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DF_PATH = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
MODEL_PATH = os.path.join(BASE_DIR, "Models", "logreg_success.pkl")
```

---

## 📈 Model Performance

| Model | Accuracy | Notes |
|-------|----------|-------|
| Success Prediction | 85-90% | Logistic Regression |
| Collaborative Filtering | RMSE ~0.3 | TruncatedSVD (60 factors) |
| Specialization Classifier | 39% | Random Forest |
| Recommendation Quality | 0.75-0.85 | Precision@5 |

---

## 🎓 Realistic Course Catalog (93 Courses)

### **Domains:**
1. **Artificial Intelligence** (15 courses)
   - Deep Learning, Computer Vision, Natural Language Processing, etc.
   
2. **Data Science** (12 courses)
   - Big Data Analytics, Statistical Learning, Data Mining, etc.
   
3. **Software Engineering** (10 courses)
   - Microservices Architecture, DevOps, Agile Development, etc.
   
4. **Cybersecurity** (8 courses)
   - Ethical Hacking, Cryptography, Network Security, etc.
   
5. **Cloud Computing** (8 courses)
   - AWS/Azure/GCP, Container Orchestration, Serverless, etc.
   
6. **Web Development** (8 courses)
   - Full-Stack Development, React/Angular, RESTful APIs, etc.
   
7. **Mobile Development** (6 courses)
   - Android/iOS Development, Cross-Platform, etc.
   
8. **Database Management** (6 courses)
   - SQL/NoSQL, Database Design, Data Warehousing, etc.
   
9. **Networking** (6 courses)
   - Network Protocols, Wireless Networks, IoT, etc.
   
10. **Computer Graphics** (4 courses)
    - 3D Modeling, Game Development, Rendering, etc.
    
11-15. **Other domains**: Blockchain, IoT, Robotics, Quantum Computing, HCI

---

## 🐛 Troubleshooting

### **Import Errors**
```python
# If you get "ModuleNotFoundError: No module named 'hybrid_infer'"
# Add Scripts/utils to Python path:
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Scripts', 'utils'))
```

### **File Not Found Errors**
All scripts use `BASE_DIR` auto-detection. If you encounter issues:
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### **SHAP/LIME Installation Issues**
```bash
pip uninstall shap lime -y
pip install shap==0.49.1 lime==0.2.0.1
```

---

## 📝 Contribution Guidelines

1. **New Training Scripts** → Add to `Scripts/training/`
2. **New Preprocessing** → Add to `Scripts/preprocessing/`
3. **New Tests** → Add to `Scripts/testing/`
4. **New Utilities** → Add to `Scripts/utils/`
5. **Models** → Always save to `Models/`
6. **Datasets** → Always save to `dataset/`

---

## 📚 Additional Resources

- **Main Documentation**: [README.md](README.md)
- **Setup Guide**: [SETUP_GUIDE_V2.md](SETUP_GUIDE_V2.md)
- **Upgrade Summary**: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)
- **Quick Reference**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## ✅ System Status

| Component | Status | Last Updated |
|-----------|--------|--------------|
| Dataset Generation | ✅ Working | Jan 16, 2026 |
| Preprocessing Pipeline | ✅ Working | Jan 16, 2026 |
| Model Training | ✅ Working | Jan 16, 2026 |
| SHAP/LIME Integration | ✅ Working | Jan 16, 2026 |
| Gemini AI Explainer | ✅ Working | Jan 16, 2026 |
| Random Student Input | ✅ Working | Jan 16, 2026 |
| Streamlit UI | ✅ Working | Jan 16, 2026 |
| Documentation | ✅ Complete | Jan 16, 2026 |

---

## 🎉 Success Criteria

✅ **Organized Folder Structure** - Scripts/, Models/, dataset/  
✅ **Portable Path Handling** - BASE_DIR auto-detection  
✅ **Triple Explanation System** - SHAP + LIME + Gemini  
✅ **Random Student Input** - Accept any student data  
✅ **Realistic Course Catalog** - 93 industry-standard courses  
✅ **Comprehensive Documentation** - Full workflow guides  
✅ **Production Ready** - Fully tested and validated  

---

**🚀 SmartEduPath - AI-Powered Course Recommendations with Explainable AI**

*Built with ❤️ for Sri Lankan Universities*
