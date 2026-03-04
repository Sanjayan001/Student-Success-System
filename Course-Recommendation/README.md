# 🎓 Sri Lankan University Course Recommendation System
## AI-Powered Course & Specialization Recommender with Explainable AI

**Version:** 1.0 FINAL  
**Date:** December 26, 2025  
**Accuracy:** Success Model 80% | Specialization Model 39%

---

## 📋 Project Overview

A complete end-to-end machine learning system that helps Sri Lankan university students choose the best courses and specializations based on their performance, interests, and future job market demands. The system uses hybrid AI algorithms and Google Gemini for explainable recommendations.

### **Key Features:**
✅ **Hybrid Recommendation Engine** - Combines 3 ML algorithms (Content-Based + Collaborative + Success Prediction)  
✅ **Success Prediction** - 80% accuracy in predicting pass/fail  
✅ **Specialization Guidance** - 39% accuracy (6x better than random)  
✅ **Explainable AI** - Natural language explanations via Google Gemini  
✅ **Job Market Forecasting** - Recommendations aligned with 2035 job demand  
✅ **Interactive Web UI** - Streamlit dashboard for easy access  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     WEB INTERFACE                           │
│                   (streamlit_app.py)                        │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  RECOMMENDATION  │    │   GEMINI XAI     │
│  ENGINE          │───▶│   EXPLAINER      │
│ (hybrid_infer.py)│    │(gemini_explainer)│
└────────┬─────────┘    └──────────────────┘
         │
    ┌────┴─────────────────┐
    ▼                      ▼
┌──────────┐      ┌──────────────┐
│ ML MODELS│      │   DATASETS   │
├──────────┤      ├──────────────┤
│ CBF      │      │ Student Data │
│ CF (SVD) │      │ Course Data  │
│ Success  │      │ Interactions │
│ Spec v2  │      │ Features     │
└──────────┘      └──────────────┘
```

---

## 📊 Performance Metrics

### **1. Success Prediction Model**
- **Algorithm:** Logistic Regression
- **Accuracy:** 79.75%
- **AUC-ROC:** 89.29% ⭐ (Excellent!)
- **Use Case:** Predicts if a student will pass/fail a course

### **2. Specialization Model (v2 - FINAL)**
- **Algorithm:** XGBoost
- **Accuracy:** 39.05% (vs 6.67% random baseline)
- **Improvement:** 6x better than random
- **Use Case:** Recommends best specialization path
- **Note:** Uses domain-based features and logical label generation

### **3. Recommendation System**
- **Hybrid Score:** Weighted combination of:
  - Collaborative Filtering (40%)
  - Content-Based Filtering (35%)
  - Success Prediction (20%)
  - Job Market Demand (5%)

---

## 📁 Project Structure

### **Core Files:**
```
├── streamlit_app.py                    # Web UI (Streamlit)
├── hybrid_infer.py                     # Recommendation engine
├── gemini_explainer.py                 # AI explanations
├── preprocess.py                       # Data preprocessing
├── requirements.txt                    # Dependencies
```

### **Training Scripts:**
```
├── train_success_model.py              # Train pass/fail predictor
├── train_specialization_model.py       # Train specialization model
├── train_cbf.py                        # Train content-based filtering
├── train_cf.py                         # Train collaborative filtering
├── datasetMaking.py                    # Generate synthetic data
├── create_student_level_labels.py      # Create student features
```

### **Models (Trained & Ready):**
```
├── logreg_success.pkl                  # Success prediction (80% acc)
├── success_scaler.pkl                  # Feature scaler
├── spec_model_v2.pkl                   # Specialization model (39% acc) ⭐
├── spec_feature_cols_v2.pkl            # Feature definitions
├── spec_label_map_v2.pkl               # Label mappings
├── tfidf_course.pkl                    # TF-IDF vectorizer
├── cf_alt_svd_model.pkl                # SVD collaborative filtering
├── cf_alt_*.npy                        # Matrix factorization data
├── *_encoder.pkl                       # Various encoders
```

### **Data Files:**
```
├── dataset_processed_for_modeling.csv  # Main processed dataset (250k rows)
├── student_level_labeled.csv           # Student-level features
├── student_domain_features_logical_labels.csv  # Domain features for spec
├── dataset_clean.csv                   # Cleaned raw data
├── sri_lanka_course_recommendation_dataset.csv  # Original data
```

### **Documentation:**
```
├── README.md                           # This file
├── QUICK_START_GUIDE.md               # How to use the system
├── RUN_UI_GUIDE.md                    # How to run the web app
├── INPUTS_OUTPUTS_SUMMARY.md          # API documentation
├── UI_DESIGN_GUIDE.md                 # UI design specs
├── GEMINI_XAI_IMPLEMENTATION_SUMMARY.md
├── GEMINI_XAI_EXAMPLE_ANALYSIS.md
```

### **Visualizations:**
```
├── visualize_model_accuracy.py         # Generate accuracy graphs
├── success_model_accuracy_graphs.png   # Success model metrics
├── specialization_model_accuracy_graphs.png  # Spec model metrics
```

---

## 🚀 Quick Start

### **1. Installation**
```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Run Web Application**
```bash
streamlit run streamlit_app.py
```

Then open: http://localhost:8501

### **3. Generate Recommendations (Python API)**
```python
from hybrid_infer import recommend

# Get recommendations for a student
recommendations = recommend("S01290", top_n=10)

# View results
print(recommendations[['course_name', 'final_score', 'explanation']])
```

---

## 🔧 Model Training

### **Re-train Success Model:**
```bash
python train_success_model.py
```
- Input: `dataset_processed_for_modeling.csv`
- Output: `logreg_success.pkl`, `success_scaler.pkl`
- Expected Accuracy: ~80%

### **Re-train Specialization Model:**
```bash
# First: Create domain features with logical labels
python create_student_level_labels.py

# Train model
python train_specialization_model.py
```
- Input: `student_domain_features_logical_labels.csv`
- Output: `spec_model_v2.pkl`, `spec_feature_cols_v2.pkl`, `spec_label_map_v2.pkl`
- Expected Accuracy: ~39%

### **Re-train Recommendation Models:**
```bash
python train_cbf.py  # Content-based filtering
python train_cf.py   # Collaborative filtering
```

---

## 📊 Accuracy Visualization

Generate comprehensive accuracy graphs:
```bash
python visualize_model_accuracy.py
```

This creates:
- Confusion matrices
- ROC curves
- Precision-Recall curves
- Feature importance charts
- Per-class performance metrics

---

## 🎯 Unique Features

### **1. Triple-Hybrid Algorithm**
Unlike typical recommenders that use one approach, this system combines three:
- **Collaborative Filtering:** "Students like you also took..."
- **Content-Based:** "Based on your interests..."
- **Predictive:** "You have 85% chance to pass..."

### **2. Sri Lanka-Specific Context**
- 15 specialized domains (Agriculture, Tourism, Renewable Energy, etc.)
- Job market predictions for **2035**
- Localized course catalog and specializations

### **3. Explainable AI with Gemini**
Every recommendation includes:
- **Why** it's recommended
- **Success probability**
- **Career relevance**
- **Natural language explanation**

Example:
> "You excel in AI courses (avg 82%) and show strong interest in Machine Learning. This course aligns with high job demand (95%) in 2035 and matches your career goals in Data Science."

### **4. Risk-Aware Recommendations**
- Identifies at-risk students
- Adjusts difficulty levels
- Prevents overload scenarios

### **5. Future Job Market Integration**
- Predictions based on 2035 employment trends
- Emerging fields prioritization
- Skills gap analysis

---

## 📈 Dataset Information

### **Main Dataset:**
- **Records:** 249,999 course enrollments
- **Students:** 10,000 unique students
- **Courses:** 500+ unique courses
- **Domains:** 15 specialization areas
- **Features:** 29 columns including:
  - Student demographics (age, gender, university)
  - Academic performance (GPA, grades, attendance)
  - Course metadata (difficulty, interest, skills)
  - Job market data (employability, demand)
  - Risk scores

### **Student-Level Features:**
- **Records:** 10,000 students
- **Features:** 56 engineered features including:
  - Domain-specific grades
  - Domain course counts
  - Interest levels per domain
  - Best performing domain
  - Performance trends

---

## 🛠️ Technology Stack

**Languages:** Python 3.12  
**ML Libraries:** scikit-learn, XGBoost, LightGBM  
**Data:** Pandas, NumPy  
**UI:** Streamlit  
**Visualization:** Matplotlib, Seaborn, Plotly  
**AI:** Google Gemini API  
**NLP:** TF-IDF, Word embeddings  

---

## 📊 Model Comparison

| Model | Old Version | New Version | Improvement |
|-------|-------------|-------------|-------------|
| **Success Model** | 79.75% | 79.75% | ✅ Stable |
| **Specialization** | 6.30% | **39.05%** | 🚀 **+520%** |

---

## 🎓 Use Cases

### **For Students:**
1. **Course Selection** - Find best courses for next semester
2. **Specialization Decision** - Choose the right major
3. **Risk Assessment** - Understand pass/fail probability
4. **Career Planning** - Align education with 2035 job market

### **For Universities:**
1. **Academic Advising** - Data-driven guidance
2. **Student Success** - Early intervention for at-risk students
3. **Curriculum Planning** - Identify popular/needed courses
4. **Resource Allocation** - Optimize course offerings

### **For Researchers:**
1. **Educational Data Mining** - Student behavior patterns
2. **Recommendation Systems** - Hybrid algorithm research
3. **XAI Applications** - Explainable AI in education
4. **Predictive Analytics** - Success forecasting models

---

## 🔒 API Configuration

### **Google Gemini API:**
Set your API key in `gemini_explainer.py`:
```python
GEMINI_API_KEY = "your-api-key-here"
```

Or set environment variable:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 📝 Key Improvements in V2

### **Specialization Model:**
✅ **Feature Engineering:** Added 54 domain-specific features  
✅ **Label Generation:** Fixed random labels with logic-based approach  
✅ **Algorithm:** Switched to XGBoost for better performance  
✅ **Accuracy:** Improved from 6.3% to 39.05% (6x improvement)  

### **System Optimization:**
✅ **Code Cleanup:** Removed 19+ temporary files  
✅ **Model Consolidation:** Using spec_model_v2.pkl (final version)  
✅ **Documentation:** Complete README and guides  

---

## 🏆 Results Summary

### **Success Metrics:**
- ✅ **80% accuracy** in pass/fail prediction
- ✅ **89% AUC** (excellent discrimination)
- ✅ **39% accuracy** in specialization (6x random)
- ✅ **Hybrid recommendations** with explainable AI
- ✅ **Production-ready** web application

### **Deliverables:**
- ✅ Trained ML models
- ✅ Web interface (Streamlit)
- ✅ Complete documentation
- ✅ Accuracy visualizations
- ✅ API for integration

---

## 🚀 Future Enhancements

**Model Improvements:**
- Add deep learning for specialization (target: 50-60%)
- Incorporate course sequences and prerequisites
- Add peer influence features
- Real-time model updates

**System Features:**
- Mobile application
- Email notifications for recommendations
- Integration with university systems
- A/B testing framework

**Data:**
- Collect real student data
- Add more domains/courses
- Historical trend analysis
- Feedback loop for continuous improvement

---

## 👥 Contact & Support

For questions, issues, or contributions, please refer to:
- **Documentation:** See QUICK_START_GUIDE.md
- **API Guide:** See INPUTS_OUTPUTS_SUMMARY.md
- **UI Guide:** See RUN_UI_GUIDE.md

---

## 📄 License

This is a research project for educational purposes.

---

## 🎉 Acknowledgments

- **Google Gemini AI** for explainable AI capabilities
- **Sri Lankan Education System** for domain context
- **Open-source ML libraries** (scikit-learn, XGBoost, LightGBM)

---

**Built with ❤️ for Sri Lankan Students**

*Empowering better educational decisions through AI*
