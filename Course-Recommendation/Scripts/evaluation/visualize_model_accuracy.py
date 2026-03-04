"""
Visualize Model Accuracy and Performance
Generates comprehensive accuracy graphs for trained models.
"""
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix, classification_report, 
    roc_curve, auc, precision_recall_curve,
    accuracy_score, precision_score, recall_score, f1_score
)
import warnings
warnings.filterwarnings("ignore")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

def visualize_success_model():
    """Visualize Success Prediction Model (Binary Classification)"""
    print("=" * 60)
    print("SUCCESS MODEL VISUALIZATION")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv("dataset_processed_for_modeling.csv")
    feats = ['previous_GPA','attendance_rate','course_difficulty',
             'course_interest','job_market_demand_2035','risk_score']
    df = df.dropna(subset=['final_grade'])
    X = df[feats].copy()
    y = (df['final_grade'] >= 60).astype(int)
    
    # Split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Load model and scaler
    model = joblib.load("logreg_success.pkl")
    scaler = joblib.load("success_scaler.pkl")
    X_val_s = scaler.transform(X_val)
    
    # Predictions
    y_proba = model.predict_proba(X_val_s)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Confusion Matrix
    ax1 = plt.subplot(2, 3, 1)
    cm = confusion_matrix(y_val, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax1)
    ax1.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax1.set_ylabel('True Label')
    ax1.set_xlabel('Predicted Label')
    ax1.set_xticklabels(['Fail', 'Pass'])
    ax1.set_yticklabels(['Fail', 'Pass'])
    
    # 2. ROC Curve
    ax2 = plt.subplot(2, 3, 2)
    fpr, tpr, thresholds = roc_curve(y_val, y_proba)
    roc_auc = auc(fpr, tpr)
    ax2.plot(fpr, tpr, color='darkorange', lw=2, 
             label=f'ROC curve (AUC = {roc_auc:.3f})')
    ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('False Positive Rate', fontsize=11)
    ax2.set_ylabel('True Positive Rate', fontsize=11)
    ax2.set_title('ROC Curve', fontsize=14, fontweight='bold')
    ax2.legend(loc="lower right")
    ax2.grid(True, alpha=0.3)
    
    # 3. Precision-Recall Curve
    ax3 = plt.subplot(2, 3, 3)
    precision, recall, _ = precision_recall_curve(y_val, y_proba)
    ax3.plot(recall, precision, color='blue', lw=2)
    ax3.set_xlabel('Recall', fontsize=11)
    ax3.set_ylabel('Precision', fontsize=11)
    ax3.set_title('Precision-Recall Curve', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim([0.0, 1.0])
    ax3.set_ylim([0.0, 1.05])
    
    # 4. Feature Importance
    ax4 = plt.subplot(2, 3, 4)
    importance = np.abs(model.coef_[0])
    importance_df = pd.DataFrame({
        'Feature': feats,
        'Importance': importance
    }).sort_values('Importance', ascending=True)
    ax4.barh(importance_df['Feature'], importance_df['Importance'], color='steelblue')
    ax4.set_xlabel('Absolute Coefficient', fontsize=11)
    ax4.set_title('Feature Importance', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='x')
    
    # 5. Metrics Summary
    ax5 = plt.subplot(2, 3, 5)
    ax5.axis('off')
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)
    recall = recall_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)
    
    metrics_text = f"""
    PERFORMANCE METRICS
    {'='*40}
    
    Accuracy:     {accuracy:.4f} ({accuracy*100:.2f}%)
    Precision:    {precision:.4f} ({precision*100:.2f}%)
    Recall:       {recall:.4f} ({recall*100:.2f}%)
    F1-Score:     {f1:.4f}
    ROC AUC:      {roc_auc:.4f}
    
    {'='*40}
    
    Sample Size:  {len(y_val)} students
    Pass Rate:    {y_val.sum()/len(y_val)*100:.1f}%
    Fail Rate:    {(1-y_val.sum()/len(y_val))*100:.1f}%
    """
    
    ax5.text(0.1, 0.9, metrics_text, fontsize=11, family='monospace',
             verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='lightblue', alpha=0.3))
    
    # 6. Prediction Distribution
    ax6 = plt.subplot(2, 3, 6)
    ax6.hist(y_proba[y_val == 0], bins=30, alpha=0.5, label='Actual Fail', color='red')
    ax6.hist(y_proba[y_val == 1], bins=30, alpha=0.5, label='Actual Pass', color='green')
    ax6.axvline(x=0.5, color='black', linestyle='--', linewidth=2, label='Threshold')
    ax6.set_xlabel('Predicted Probability', fontsize=11)
    ax6.set_ylabel('Frequency', fontsize=11)
    ax6.set_title('Prediction Distribution', fontsize=14, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.suptitle('Success Model - Comprehensive Accuracy Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.savefig('success_model_accuracy_graphs.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved: success_model_accuracy_graphs.png")
    plt.show()
    
    return accuracy, precision, recall, f1, roc_auc


def visualize_specialization_model():
    """Visualize Specialization Model (Multi-class Classification)"""
    print("\n" + "=" * 60)
    print("SPECIALIZATION MODEL VISUALIZATION")
    print("=" * 60)
    
    # Load data
    df = pd.read_csv("student_domain_features_logical_labels.csv")
    
    # Load model and feature columns
    model = joblib.load("spec_model_v2.pkl")
    feature_cols = joblib.load("spec_feature_cols_v2.pkl")
    label_map = joblib.load("spec_label_map_v2.pkl")
    
    X = df[feature_cols].fillna(0)
    y = df['chosen_specialization']  # The actual column name in the CSV
    
    # Split
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Load model
    model = joblib.load("spec_model.pkl")
    
    # Predictions
    try:
        # LightGBM
        y_proba = model.predict(X_val)
        y_pred = np.argmax(y_proba, axis=1)
    except:
        # RandomForest
        y_pred = model.predict(X_val)
        y_proba = model.predict_proba(X_val)
    
    # Create figure
    fig = plt.figure(figsize=(16, 10))
    
    # 1. Confusion Matrix
    ax1 = plt.subplot(2, 3, 1)
    cm = confusion_matrix(y_val, y_pred)
    
    # Get class names from label_map (reverse mapping)
    class_names = sorted(set(label_map.values()))
    
    sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrRd', cbar=True, ax=ax1,
                xticklabels=class_names, yticklabels=class_names)
    ax1.set_title('Confusion Matrix', fontsize=14, fontweight='bold')
    ax1.set_ylabel('True Specialization')
    ax1.set_xlabel('Predicted Specialization')
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    
    # 2. Per-Class Accuracy
    ax2 = plt.subplot(2, 3, 2)
    class_accuracy = []
    for i, class_name in enumerate(class_names):
        mask = y_val == i
        if mask.sum() > 0:
            acc = accuracy_score(y_val[mask], y_pred[mask])
            class_accuracy.append(acc)
        else:
            class_accuracy.append(0)
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(class_names)))
    ax2.barh(class_names, class_accuracy, color=colors)
    ax2.set_xlabel('Accuracy', fontsize=11)
    ax2.set_title('Per-Class Accuracy', fontsize=14, fontweight='bold')
    ax2.set_xlim([0, 1])
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. Feature Importance (top 15)
    ax3 = plt.subplot(2, 3, 3)
    try:
        # Try to get feature importance
        if hasattr(model, 'feature_importance'):
            importance = model.feature_importance()
        elif hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        else:
            importance = np.zeros(len(feature_cols))
        
        importance_df = pd.DataFrame({
            'Feature': feature_cols,
            'Importance': importance
        }).sort_values('Importance', ascending=False).head(15)
        
        ax3.barh(importance_df['Feature'][::-1], importance_df['Importance'][::-1], 
                color='coral')
        ax3.set_xlabel('Importance', fontsize=11)
        ax3.set_title('Top 15 Features', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='x')
    except:
        ax3.text(0.5, 0.5, 'Feature importance not available', 
                ha='center', va='center')
        ax3.axis('off')
    
    # 4. Classification Report Heatmap
    ax4 = plt.subplot(2, 3, 4)
    report = classification_report(y_val, y_pred, target_names=le.classes_, 
                                   output_dict=True, zero_division=0)
    report_df = pd.DataFrame(report).T.iloc[:-3, :3]  # Skip avg rows
    sns.heatmap(report_df, annot=True, fmt='.2f', cmap='RdYlGn', 
               vmin=0, vmax=1, ax=ax4, cbar_kws={'label': 'Score'})
    ax4.set_title('Classification Report', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Specialization')
    
    # 5. Overall Metrics
    ax5 = plt.subplot(2, 3, 5)
    ax5.axis('off')
    overall_acc = accuracy_score(y_val, y_pred)
    
    # Get macro averages
    macro_precision = precision_score(y_val, y_pred, average='macro', zero_division=0)
    macro_recall = recall_score(y_val, y_pred, average='macro', zero_division=0)
    macro_f1 = f1_score(y_val, y_pred, average='macro', zero_division=0)
    
    metrics_text = f"""
    OVERALL METRICS
    {'='*40}
    
    Overall Accuracy:    {overall_acc:.4f}
                        ({overall_acc*100:.2f}%)
    
    Macro Precision:     {macro_precision:.4f}
    Macro Recall:        {macro_recall:.4f}
    Macro F1-Score:      {macro_f1:.4f}
    
    {'='*40}
    
    Total Samples:       {len(y_val)} students
    Number of Classes:   {len(le.classes_)}
    """
    
    ax5.text(0.1, 0.9, metrics_text, fontsize=11, family='monospace',
             verticalalignment='top', bbox=dict(boxstyle='round', 
             facecolor='lightgreen', alpha=0.3))
    
    # 6. Prediction Confidence Distribution
    ax6 = plt.subplot(2, 3, 6)
    confidence = np.max(y_proba, axis=1)
    ax6.hist(confidence, bins=30, color='purple', alpha=0.7, edgecolor='black')
    ax6.axvline(x=confidence.mean(), color='red', linestyle='--', 
               linewidth=2, label=f'Mean: {confidence.mean():.3f}')
    ax6.set_xlabel('Prediction Confidence', fontsize=11)
    ax6.set_ylabel('Frequency', fontsize=11)
    ax6.set_title('Model Confidence Distribution', fontsize=14, fontweight='bold')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    
    plt.suptitle('Specialization Model - Comprehensive Accuracy Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout(rect=[0, 0, 1, 0.99])
    plt.savefig('specialization_model_accuracy_graphs.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved: specialization_model_accuracy_graphs.png")
    plt.show()
    
    return overall_acc, macro_precision, macro_recall, macro_f1


def main():
    """Generate all accuracy visualizations"""
    print("\n🎯 GENERATING MODEL ACCURACY GRAPHS\n")
    
    try:
        # Success Model
        success_metrics = visualize_success_model()
        print(f"\n✓ Success Model - Accuracy: {success_metrics[0]:.4f}, AUC: {success_metrics[4]:.4f}")
    except Exception as e:
        print(f"\n✗ Error with Success Model: {e}")
    
    try:
        # Specialization Model  
        spec_metrics = visualize_specialization_model()
        print(f"\n✓ Specialization Model - Accuracy: {spec_metrics[0]:.4f}")
    except Exception as e:
        print(f"\n✗ Error with Specialization Model: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL GRAPHS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nCheck these files:")
    print("  📊 success_model_accuracy_graphs.png")
    print("  📊 specialization_model_accuracy_graphs.png")
    print()


if __name__ == "__main__":
    main()
