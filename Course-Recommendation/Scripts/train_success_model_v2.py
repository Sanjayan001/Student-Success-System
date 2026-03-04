# train_success_model_v2.py
# Updated version that saves models to Models/ folder
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score

# Updated paths
DF = "dataset_processed_for_modeling.csv"
MODEL_DIR = "Models"
MODEL_OUT = os.path.join(MODEL_DIR, "logreg_success.pkl")
SCALER_OUT = os.path.join(MODEL_DIR, "success_scaler.pkl")

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
    return X, y, feats

def main():
    # Ensure Models directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print("📂 Loading dataset...")
    df = pd.read_csv(DF)
    
    print("🔧 Preparing features...")
    X, y, feature_names = load_and_prepare(df)
    
    print(f"📊 Dataset: {len(X)} samples, {X.shape[1]} features")
    print(f"   Classes: {y.value_counts().to_dict()}")
    
    # Train/val split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n🔄 Training set: {len(X_train)} | Validation set: {len(X_val)}")
    
    # Scale features
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_val_s = scaler.transform(X_val)

    # Train Logistic Regression
    print("\n🤖 Training Logistic Regression model...")
    clf = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=42)
    clf.fit(X_train_s, y_train)

    # Evaluation
    print("\n📈 Evaluating model...")
    probs = clf.predict_proba(X_val_s)[:,1]
    preds = (probs >= 0.5).astype(int)
    
    auc = roc_auc_score(y_val, probs)
    acc = accuracy_score(y_val, preds)
    prec = precision_score(y_val, preds)
    rec = recall_score(y_val, preds)
    
    print(f"\n✅ Model Performance:")
    print(f"   AUC-ROC: {auc:.4f}")
    print(f"   Accuracy: {acc:.4f}")
    print(f"   Precision: {prec:.4f}")
    print(f"   Recall: {rec:.4f}")
    
    # Feature importance (coefficients)
    print(f"\n🔍 Top Feature Importances:")
    coefs = clf.coef_[0]
    feat_importance = sorted(zip(feature_names, coefs), key=lambda x: abs(x[1]), reverse=True)
    for feat, coef in feat_importance[:5]:
        print(f"   {feat}: {coef:.4f}")

    # Save models
    print(f"\n💾 Saving models to {MODEL_DIR}/...")
    joblib.dump(clf, MODEL_OUT)
    joblib.dump(scaler, SCALER_OUT)
    
    print(f"   ✅ {MODEL_OUT}")
    print(f"   ✅ {SCALER_OUT}")
    
    print("\n✨ Success model training complete!")

if __name__ == "__main__":
    main()
