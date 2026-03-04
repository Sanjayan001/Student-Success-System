# train_specialization_model.py
"""
Train specialization classifier.
Input: student_level_labeled.csv
Outputs:
 - spec_model.pkl           (trained model, LightGBM or RandomForest)
 - spec_feature_cols.pkl    (feature column order)
 - spec_label_map.pkl       (index -> label mapping)
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT = os.path.join(BASE_DIR, "dataset", "student_level_labeled.csv")
MODEL_OUT = os.path.join(BASE_DIR, "Models", "spec_model.pkl")
FEATURES_OUT = os.path.join(BASE_DIR, "Models", "spec_feature_cols.pkl")
LABELMAP_OUT = os.path.join(BASE_DIR, "Models", "spec_label_map.pkl")

def main():
    print("Loading:", INPUT)
    df = pd.read_csv(INPUT)
    print("Rows (students):", len(df))

    # Basic feature columns (expand as available in your file)
    numeric_feats = ['previous_GPA','attendance_rate','avg_course_grade','avg_course_interest','avg_job_demand','avg_risk','n_courses']
    # plus any domain count columns (domain_cnt_*)
    domain_cols = [c for c in df.columns if c.startswith('domain_cnt_')]
    feature_cols = numeric_feats + domain_cols
    feature_cols = [c for c in feature_cols if c in df.columns]

    print("Using feature columns:", feature_cols)

    X = df[feature_cols].fillna(0)
    y_raw = df['chosen_specialization'].astype(str).fillna("Unknown")
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    label_map = {i: label for i, label in enumerate(le.classes_)}
    joblib.dump(label_map, LABELMAP_OUT)
    print("Saved label map:", LABELMAP_OUT, "classes:", len(label_map))

    # train/val split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Try LightGBM, fallback to RandomForest
    use_lgb = False
    try:
        import lightgbm as lgb
        use_lgb = True
    except Exception as e:
        print("LightGBM not available or failed to import, falling back to RandomForest. Error:", e)

    if use_lgb:
        print("Training LightGBM multiclass classifier...")
        train_data = lgb.Dataset(X_train, label=y_train)
        val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
        params = {
            'objective':'multiclass',
            'num_class': len(le.classes_),
            'metric': 'multi_logloss',
            'learning_rate': 0.05,
            'num_leaves': 31,
            'verbosity': -1,
            'seed': 42
        }
        bst = lgb.train(params, train_data, valid_sets=[val_data], num_boost_round=1000, early_stopping_rounds=30, verbose_eval=50)
        # Wrap model predict interface into joblib save
        model = bst
    else:
        print("Training RandomForestClassifier (fallback)...")
        from sklearn.ensemble import RandomForestClassifier
        rf = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        rf.fit(X_train, y_train)
        model = rf

    # Evaluate
    if use_lgb:
        preds_proba = model.predict(X_val)
        preds = np.argmax(preds_proba, axis=1)
    else:
        preds = model.predict(X_val)

    print("Accuracy:", round(accuracy_score(y_val, preds),4))
    print("Classification report:")
    print(classification_report(y_val, preds, target_names=le.classes_, zero_division=0))

    # Save model and feature list
    joblib.dump(model, MODEL_OUT)
    joblib.dump(feature_cols, FEATURES_OUT)
    joblib.dump(le.classes_.tolist(), LABELMAP_OUT)
    print("Saved model to", MODEL_OUT)
    print("Saved feature list to", FEATURES_OUT)
    print("Saved label list to", LABELMAP_OUT)

if __name__ == "__main__":
    main()
