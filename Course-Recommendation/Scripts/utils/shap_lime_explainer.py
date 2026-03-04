#!/usr/bin/env python3
"""
shap_lime_explainer.py
Provides model-intrinsic explanations using SHAP (SHapley Additive exPlanations) 
and LIME (Local Interpretable Model-agnostic Explanations).

This complements Gemini explanations with mathematical feature importance.
"""

import numpy as np
import pandas as pd
import shap
from lime.lime_tabular import LimeTabularExplainer
import warnings
warnings.filterwarnings('ignore')

class SHAPLIMEExplainer:
    """
    Unified explainer for ML models using SHAP and LIME.
    Provides feature importance and contribution analysis.
    """
    
    def __init__(self, model, feature_names, model_type='classification'):
        """
        Initialize explainer with trained model.
        
        Args:
            model: Trained sklearn model (e.g., LogisticRegression, XGBoost)
            feature_names: List of feature names
            model_type: 'classification' or 'regression'
        """
        self.model = model
        self.feature_names = feature_names
        self.model_type = model_type
        self.shap_explainer = None
        self.lime_explainer = None
        
    def initialize_shap(self, background_data):
        """
        Initialize SHAP explainer with background data.
        
        Args:
            background_data: Sample of training data (numpy array or pandas DataFrame)
        """
        try:
            # Use Tree explainer for tree-based models, otherwise use Kernel explainer
            if hasattr(self.model, 'tree_') or 'XGB' in str(type(self.model)):
                self.shap_explainer = shap.TreeExplainer(self.model)
            else:
                # For linear models like LogisticRegression
                self.shap_explainer = shap.LinearExplainer(self.model, background_data)
            return True
        except Exception as e:
            print(f"⚠️ SHAP initialization failed: {e}")
            # Fallback to KernelExplainer (slower but works for any model)
            try:
                self.shap_explainer = shap.KernelExplainer(
                    self.model.predict_proba if self.model_type == 'classification' else self.model.predict,
                    shap.sample(background_data, 100)
                )
                return True
            except:
                return False
    
    def initialize_lime(self, training_data, class_names=None):
        """
        Initialize LIME explainer with training data.
        
        Args:
            training_data: Training data (numpy array)
            class_names: List of class names (for classification)
        """
        try:
            mode = 'classification' if self.model_type == 'classification' else 'regression'
            self.lime_explainer = LimeTabularExplainer(
                training_data=training_data,
                feature_names=self.feature_names,
                class_names=class_names or ['Fail', 'Pass'],
                mode=mode,
                random_state=42
            )
            return True
        except Exception as e:
            print(f"⚠️ LIME initialization failed: {e}")
            return False
    
    def explain_with_shap(self, instance):
        """
        Generate SHAP explanation for a single instance.
        
        Args:
            instance: Single data point (1D array or DataFrame row)
            
        Returns:
            dict with SHAP values and feature contributions
        """
        if self.shap_explainer is None:
            return None
        
        try:
            # Ensure instance is 2D array
            if len(instance.shape) == 1:
                instance = instance.reshape(1, -1)
            
            # Get SHAP values
            shap_values = self.shap_explainer.shap_values(instance)
            
            # For binary classification, take positive class
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # Positive class
            
            # Convert to 1D if needed
            if len(shap_values.shape) > 1:
                shap_values = shap_values[0]
            
            # Create feature contributions
            contributions = []
            for i, (feature, value) in enumerate(zip(self.feature_names, instance[0])):
                contributions.append({
                    'feature': feature,
                    'value': float(value),
                    'contribution': float(shap_values[i]),
                    'abs_contribution': abs(float(shap_values[i]))
                })
            
            # Sort by absolute contribution
            contributions.sort(key=lambda x: x['abs_contribution'], reverse=True)
            
            return {
                'shap_values': shap_values.tolist(),
                'feature_contributions': contributions,
                'top_positive': [c for c in contributions if c['contribution'] > 0][:3],
                'top_negative': [c for c in contributions if c['contribution'] < 0][:3]
            }
        
        except Exception as e:
            print(f"⚠️ SHAP explanation failed: {e}")
            return None
    
    def explain_with_lime(self, instance, num_features=5):
        """
        Generate LIME explanation for a single instance.
        
        Args:
            instance: Single data point (1D array)
            num_features: Number of top features to include
            
        Returns:
            dict with LIME explanation
        """
        if self.lime_explainer is None:
            return None
        
        try:
            # Ensure instance is 1D
            if len(instance.shape) > 1:
                instance = instance[0]
            
            # Generate explanation
            if self.model_type == 'classification':
                exp = self.lime_explainer.explain_instance(
                    instance,
                    self.model.predict_proba,
                    num_features=num_features
                )
                # Get feature importances for positive class (class 1)
                lime_values = dict(exp.as_list())
            else:
                exp = self.lime_explainer.explain_instance(
                    instance,
                    self.model.predict,
                    num_features=num_features
                )
                lime_values = dict(exp.as_list())
            
            # Parse feature contributions
            contributions = []
            for feature_desc, weight in lime_values.items():
                # Extract feature name (before <= or > symbols)
                feature_name = feature_desc.split('<=')[0].split('>')[0].strip()
                contributions.append({
                    'feature': feature_name,
                    'description': feature_desc,
                    'weight': float(weight),
                    'abs_weight': abs(float(weight))
                })
            
            contributions.sort(key=lambda x: x['abs_weight'], reverse=True)
            
            return {
                'lime_explanation': lime_values,
                'feature_weights': contributions,
                'top_positive': [c for c in contributions if c['weight'] > 0][:3],
                'top_negative': [c for c in contributions if c['weight'] < 0][:3]
            }
        
        except Exception as e:
            print(f"⚠️ LIME explanation failed: {e}")
            return None
    
    def explain(self, instance, method='both'):
        """
        Generate comprehensive explanation using SHAP and/or LIME.
        
        Args:
            instance: Single data point
            method: 'shap', 'lime', or 'both'
            
        Returns:
            dict with explanations
        """
        result = {
            'method': method,
            'shap': None,
            'lime': None,
            'summary': None
        }
        
        if method in ['shap', 'both']:
            result['shap'] = self.explain_with_shap(instance)
        
        if method in ['lime', 'both']:
            result['lime'] = self.explain_with_lime(instance)
        
        # Generate human-readable summary
        result['summary'] = self._generate_summary(result)
        
        return result
    
    def _generate_summary(self, explanation):
        """Generate human-readable text summary from explanations."""
        summary = []
        
        # SHAP summary
        if explanation.get('shap') and explanation['shap'].get('feature_contributions'):
            top_features = explanation['shap']['feature_contributions'][:3]
            summary.append("🔍 **SHAP Analysis (Feature Impact):**")
            for feat in top_features:
                direction = "increases" if feat['contribution'] > 0 else "decreases"
                summary.append(
                    f"  • **{feat['feature']}** = {feat['value']:.2f} "
                    f"({direction} prediction by {abs(feat['contribution']):.4f})"
                )
        
        # LIME summary
        if explanation.get('lime') and explanation['lime'].get('feature_weights'):
            top_weights = explanation['lime']['feature_weights'][:3]
            summary.append("\n🔬 **LIME Analysis (Local Explanation):**")
            for feat in top_weights:
                direction = "supports" if feat['weight'] > 0 else "opposes"
                summary.append(
                    f"  • {feat['description']} "
                    f"({direction} the prediction, weight: {abs(feat['weight']):.4f})"
                )
        
        return "\n".join(summary) if summary else "No explanation available"


def generate_success_explanation(model, scaler, student_data, course_data, 
                                  background_data=None, use_shap=True, use_lime=True):
    """
    Generate SHAP/LIME explanation for success prediction model.
    
    Args:
        model: Trained success prediction model
        scaler: Fitted StandardScaler
        student_data: Student profile dict
        course_data: Course profile dict
        background_data: Sample training data for SHAP initialization
        use_shap: Whether to use SHAP
        use_lime: Whether to use LIME
        
    Returns:
        dict with explanations
    """
    # Prepare feature vector
    features = ['previous_GPA', 'attendance_rate', 'course_difficulty', 
                'course_interest', 'job_market_demand_2035', 'risk_score']
    
    X = pd.DataFrame([{
        'previous_GPA': student_data.get('previous_GPA', 0),
        'attendance_rate': student_data.get('attendance_rate', 0),
        'course_difficulty': course_data.get('course_difficulty', 0),
        'course_interest': student_data.get('course_interest', 0),
        'job_market_demand_2035': course_data.get('job_market_demand_2035', 0),
        'risk_score': student_data.get('risk_score', 0)
    }])
    
    # Scale
    X_scaled = scaler.transform(X)
    
    # Get prediction
    prob = model.predict_proba(X_scaled)[0, 1]
    
    # Initialize explainer
    explainer = SHAPLIMEExplainer(model, features, model_type='classification')
    
    method = 'both' if (use_shap and use_lime) else ('shap' if use_shap else 'lime')
    
    # Initialize SHAP
    if use_shap and background_data is not None:
        explainer.initialize_shap(background_data)
    
    # Initialize LIME
    if use_lime and background_data is not None:
        explainer.initialize_lime(background_data)
    
    # Generate explanation
    explanation = explainer.explain(X_scaled, method=method)
    explanation['prediction_probability'] = float(prob)
    explanation['prediction_class'] = 'Pass' if prob >= 0.5 else 'Fail'
    
    return explanation


if __name__ == "__main__":
    print("✅ SHAP/LIME Explainer Module Ready")
    print("📊 Provides mathematical feature importance alongside Gemini explanations")
