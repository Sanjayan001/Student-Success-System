# 📑 PROJECT INDEX
## Sri Lankan Course Recommendation System - File Navigator

**Quick Links to Essential Files**

---

## 🚀 START HERE

1. **[README.md](README.md)** - Complete project overview and guide
2. **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick start card (1 page)
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Detailed technical report

---

## 💻 TO RUN THE SYSTEM

### **Web Application:**
- **[streamlit_app.py](streamlit_app.py)** - Main web interface
- Command: `streamlit run streamlit_app.py`

### **Python API:**
- **[hybrid_infer.py](hybrid_infer.py)** - Recommendation engine
- Usage: `from hybrid_infer import recommend`

### **AI Explanations:**
- **[gemini_explainer.py](gemini_explainer.py)** - Google Gemini integration

---

## 🤖 MODELS (Production-Ready)

### **Primary Models:**
- ⭐ **[spec_model_v2.pkl](spec_model_v2.pkl)** - Specialization (39% accuracy - FINAL)
- ⭐ **[logreg_success.pkl](logreg_success.pkl)** - Success prediction (80% accuracy)

### **Supporting Models:**
- **[cf_alt_svd_model.pkl](cf_alt_svd_model.pkl)** - Collaborative filtering
- **[tfidf_course.pkl](tfidf_course.pkl)** - Content-based filtering

### **Model Configuration:**
- **[spec_feature_cols_v2.pkl](spec_feature_cols_v2.pkl)** - Feature definitions
- **[spec_label_map_v2.pkl](spec_label_map_v2.pkl)** - Label mappings
- **[success_scaler.pkl](success_scaler.pkl)** - Feature scaler

### **Matrix Factorization:**
- [cf_alt_student_factors.npy](cf_alt_student_factors.npy) - Student embeddings
- [cf_alt_course_factors.npy](cf_alt_course_factors.npy) - Course embeddings
- [cf_alt_student_ids.npy](cf_alt_student_ids.npy) - Student ID mapping
- [cf_alt_course_ids.npy](cf_alt_course_ids.npy) - Course ID mapping

### **Encoders:**
- [student_encoder.pkl](student_encoder.pkl)
- [course_encoder.pkl](course_encoder.pkl)
- [cf_alt_user_encoder.pkl](cf_alt_user_encoder.pkl)
- [cf_alt_item_encoder.pkl](cf_alt_item_encoder.pkl)
- [course_index_map.pkl](course_index_map.pkl)

---

## 📊 DATASETS

### **Primary Data:**
- ⭐ **[dataset_processed_for_modeling.csv](dataset_processed_for_modeling.csv)** - Main dataset (250k rows)
- ⭐ **[student_domain_features_logical_labels.csv](student_domain_features_logical_labels.csv)** - Student features with logical labels

### **Supporting Data:**
- **[student_level_labeled.csv](student_level_labeled.csv)** - Student-level aggregated data
- **[dataset_clean.csv](dataset_clean.csv)** - Cleaned raw data
- **[sri_lanka_course_recommendation_dataset.csv](sri_lanka_course_recommendation_dataset.csv)** - Original synthetic data

---

## 🔧 TRAINING SCRIPTS

### **Model Training:**
- **[train_success_model.py](train_success_model.py)** - Train success predictor (→ 80% accuracy)
- **[train_specialization_model.py](train_specialization_model.py)** - Train specialization model (→ 39% accuracy)
- **[train_cbf.py](train_cbf.py)** - Train content-based filtering
- **[train_cf.py](train_cf.py)** - Train collaborative filtering

### **Data Processing:**
- **[datasetMaking.py](datasetMaking.py)** - Generate synthetic dataset
- **[preprocess.py](preprocess.py)** - Data preprocessing
- **[create_student_level_labels.py](create_student_level_labels.py)** - Feature engineering

### **Analysis:**
- **[visualize_model_accuracy.py](visualize_model_accuracy.py)** - Generate accuracy graphs

---

## 📚 DOCUMENTATION

### **Essential Guides:**
- ⭐ **[README.md](README.md)** - Complete project guide (comprehensive)
- ⭐ **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick reference card (1 page)
- ⭐ **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Detailed technical report

### **Usage Guides:**
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - How to use the system
- **[RUN_UI_GUIDE.md](RUN_UI_GUIDE.md)** - How to run the web app
- **[INPUTS_OUTPUTS_SUMMARY.md](INPUTS_OUTPUTS_SUMMARY.md)** - API documentation

### **Technical Docs:**
- **[UI_DESIGN_GUIDE.md](UI_DESIGN_GUIDE.md)** - UI design specifications
- **[GEMINI_XAI_IMPLEMENTATION_SUMMARY.md](GEMINI_XAI_IMPLEMENTATION_SUMMARY.md)** - XAI implementation
- **[GEMINI_XAI_EXAMPLE_ANALYSIS.md](GEMINI_XAI_EXAMPLE_ANALYSIS.md)** - XAI examples

### **Deployment:**
- ⭐ **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Pre-deployment checklist

---

## 📈 VISUALIZATIONS

- **[success_model_accuracy_graphs.png](success_model_accuracy_graphs.png)** - Success model metrics
- **[specialization_model_accuracy_graphs.png](specialization_model_accuracy_graphs.png)** - Specialization metrics

---

## ⚙️ CONFIGURATION

- **[requirements.txt](requirements.txt)** - Python dependencies
- **[.venv/](.venv/)** - Virtual environment (auto-generated)

---

## 📊 PROJECT STATISTICS

| Category | Count | Description |
|----------|-------|-------------|
| **ML Models** | 16 | Production-ready trained models |
| **Datasets** | 5 | 250k+ total records |
| **Python Scripts** | 12 | Training, inference, UI |
| **Documentation** | 10 | Comprehensive guides |
| **Visualizations** | 2 | Accuracy graphs |
| **Total Files** | 45 | Complete system |

---

## 🎯 FILE IMPORTANCE GUIDE

### ⭐⭐⭐ CRITICAL (Must Have)
- `streamlit_app.py` - Web interface
- `hybrid_infer.py` - Core recommendation engine
- `spec_model_v2.pkl` - Latest specialization model
- `logreg_success.pkl` - Success prediction model
- `dataset_processed_for_modeling.csv` - Main data
- `README.md` - Documentation

### ⭐⭐ IMPORTANT (Needed for Full Functionality)
- All encoder `.pkl` files
- Matrix factorization `.npy` files
- `gemini_explainer.py` - AI explanations
- Training scripts
- Other documentation files

### ⭐ SUPPLEMENTARY (Optional)
- Visualization scripts
- Example graphs
- Analysis tools
- Additional datasets

---

## 🔍 QUICK FIND

**Looking for...** | **Go to...**
---|---
How to run the system | [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
Complete documentation | [README.md](README.md)
Technical details | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
API usage | [INPUTS_OUTPUTS_SUMMARY.md](INPUTS_OUTPUTS_SUMMARY.md)
Deployment guide | [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
Web app code | [streamlit_app.py](streamlit_app.py)
Recommendation logic | [hybrid_infer.py](hybrid_infer.py)
Best model | [spec_model_v2.pkl](spec_model_v2.pkl)
Main dataset | [dataset_processed_for_modeling.csv](dataset_processed_for_modeling.csv)

---

## 📞 HELP & SUPPORT

**New to the project?** → Start with [README.md](README.md)  
**Want to use it quickly?** → See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)  
**Need technical details?** → Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)  
**Ready to deploy?** → Check [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## ✅ PROJECT STATUS

- **Version:** 1.0 FINAL
- **Status:** ✅ PRODUCTION-READY
- **Date:** December 26, 2025
- **Total Files:** 45
- **Documentation:** Complete
- **Models:** Finalized
- **Tests:** Passed

---

**🎉 All files organized and ready for use!**

*Navigate to any file above to explore the project*
