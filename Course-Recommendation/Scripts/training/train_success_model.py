# train_success_model.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DF = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
MODEL_OUT = os.path.join(BASE_DIR, "Models", "logreg_success.pkl")
SCALER_OUT = os.path.join(BASE_DIR, "Models", "success_scaler.pkl")

def load_and_prepare(df):
    # Choose features available in processed dataset
    feats = [
        'previous_GPA','attendance_rate','course_difficulty',
        'course_interest','job_market_demand_2035','risk_score'
    ]
    # Keep only rows with final_grade (drop rows where it's NaN)
    df = df.dropna(subset=['final_grade'])
    X = df[feats].copy()
    y = (df['final_grade'] >= 60).astype(int)
    return X, y

def main():
    df = pd.read_csv(DF)
    X, y = load_and_prepare(df)
    # Train/val split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_val_s = scaler.transform(X_val)

    # Logistic regression (fast)
    clf = LogisticRegression(max_iter=1000, class_weight='balanced')
    clf.fit(X_train_s, y_train)

    # Eval
    probs = clf.predict_proba(X_val_s)[:,1]
    preds = (probs >= 0.5).astype(int)
    print("AUC:", round(roc_auc_score(y_val, probs), 4))
    print("Acc:", round(accuracy_score(y_val, preds),4), "Prec:", round(precision_score(y_val,preds),4), "Rec:", round(recall_score(y_val,preds),4))

    # Save
    joblib.dump(clf, MODEL_OUT)
    joblib.dump(scaler, SCALER_OUT)
    print("Saved model:", MODEL_OUT, "and scaler:", SCALER_OUT)

if __name__ == "__main__":
    main()
