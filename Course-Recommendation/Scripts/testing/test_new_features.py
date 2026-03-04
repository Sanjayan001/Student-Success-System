#!/usr/bin/env python3
"""
test_new_features.py
Quick test script to verify new features work correctly.
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed."""
    print("="*60)
    print("🔍 Testing Imports")
    print("="*60)
    
    tests = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("sklearn", "scikit-learn"),
        ("joblib", "joblib"),
        ("shap", "shap"),
        ("lime", "lime"),
        ("google.generativeai", "google-generativeai"),
    ]
    
    results = []
    for module, package in tests:
        try:
            __import__(module)
            print(f"✅ {package}")
            results.append(True)
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            print(f"   Run: pip install {package}")
            results.append(False)
    
    return all(results)


def test_folder_structure():
    """Test if folder structure is correct."""
    print("\n" + "="*60)
    print("📁 Testing Folder Structure")
    print("="*60)
    
    folders = ["Models", "Scripts"]
    results = []
    
    for folder in folders:
        exists = os.path.exists(folder)
        print(f"{'✅' if exists else '❌'} {folder}/")
        results.append(exists)
    
    if not all(results):
        print("\n⚠️ Missing folders. Run:")
        print("   mkdir Models Scripts")
    
    return all(results)


def test_new_modules():
    """Test if new modules can be imported."""
    print("\n" + "="*60)
    print("🧪 Testing New Modules")
    print("="*60)
    
    modules = [
        ("shap_lime_explainer.py", "shap_lime_explainer"),
        ("random_student_predictor.py", "random_student_predictor"),
    ]
    
    results = []
    for filename, module_name in modules:
        if not os.path.exists(filename):
            print(f"❌ {filename} - NOT FOUND")
            results.append(False)
            continue
        
        try:
            __import__(module_name)
            print(f"✅ {filename}")
            results.append(True)
        except Exception as e:
            print(f"⚠️ {filename} - Import error: {e}")
            results.append(False)
    
    return all(results)


def test_dataset():
    """Test if dataset exists and has realistic courses."""
    print("\n" + "="*60)
    print("📊 Testing Dataset")
    print("="*60)
    
    dataset_file = "sri_lanka_course_recommendation_dataset.csv"
    
    if not os.path.exists(dataset_file):
        print(f"❌ {dataset_file} not found")
        print("   Run: python Scripts/datasetMaking_v2.py")
        return False
    
    try:
        import pandas as pd
        df = pd.read_csv(dataset_file, nrows=100)  # Read first 100 rows only
        
        print(f"✅ Dataset found: {dataset_file}")
        print(f"   Columns: {len(df.columns)}")
        print(f"\n📚 Sample Course Names:")
        
        unique_courses = df['course_name'].unique()[:10]
        for course in unique_courses:
            print(f"   • {course}")
        
        # Check if we have realistic names (not generic)
        realistic = any("Learning" in str(c) or "Processing" in str(c) 
                       for c in unique_courses)
        
        if realistic:
            print("\n✅ Dataset has realistic course names!")
        else:
            print("\n⚠️ Dataset might have old generic names")
            print("   Consider regenerating with: python Scripts/datasetMaking_v2.py")
        
        return True
    
    except Exception as e:
        print(f"❌ Error reading dataset: {e}")
        return False


def test_shap_lime():
    """Test SHAP/LIME functionality."""
    print("\n" + "="*60)
    print("🔬 Testing SHAP/LIME")
    print("="*60)
    
    try:
        import numpy as np
        from sklearn.linear_model import LogisticRegression
        from shap_lime_explainer import SHAPLIMEExplainer
        
        # Create dummy model and data
        X_train = np.random.rand(100, 4)
        y_train = np.random.randint(0, 2, 100)
        
        model = LogisticRegression()
        model.fit(X_train, y_train)
        
        # Test explainer
        explainer = SHAPLIMEExplainer(
            model,
            feature_names=['feature1', 'feature2', 'feature3', 'feature4']
        )
        
        # Initialize
        explainer.initialize_shap(X_train)
        explainer.initialize_lime(X_train)
        
        # Test explanation
        test_instance = X_train[0:1]
        explanation = explainer.explain(test_instance, method='both')
        
        if explanation.get('summary'):
            print("✅ SHAP/LIME explainer working!")
            print("\n📝 Sample explanation:")
            print(explanation['summary'][:200] + "...")
            return True
        else:
            print("⚠️ SHAP/LIME initialized but no explanation generated")
            return False
    
    except Exception as e:
        print(f"❌ SHAP/LIME test failed: {e}")
        return False


def test_random_student():
    """Test random student predictor."""
    print("\n" + "="*60)
    print("🎓 Testing Random Student Predictor")
    print("="*60)
    
    # Check if models exist
    success_model = "Models/logreg_success.pkl"
    
    if not os.path.exists(success_model):
        print(f"⚠️ Models not found in Models/ folder")
        print("   Run training first: python Scripts/train_success_model_v2.py")
        return False
    
    try:
        from random_student_predictor import calculate_risk_score
        
        # Test risk calculation
        risk = calculate_risk_score(gpa=3.2, attendance_rate=0.85)
        
        print(f"✅ Random student predictor loaded")
        print(f"   Test risk score (GPA 3.2, Attendance 85%): {risk}")
        
        if 0 <= risk <= 1:
            print("✅ Risk calculation working correctly!")
            return True
        else:
            print("⚠️ Risk score out of range")
            return False
    
    except Exception as e:
        print(f"❌ Random student predictor test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "╔"+"="*58+"╗")
    print("║" + " "*15 + "SYSTEM VALIDATION TEST" + " "*20 + "║")
    print("╚"+"="*58+"╝\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("Folder Structure", test_folder_structure),
        ("New Modules", test_new_modules),
        ("Dataset", test_dataset),
        ("SHAP/LIME", test_shap_lime),
        ("Random Student", test_random_student),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:12} {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n🎯 Score: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📝 Next steps:")
        print("   1. Generate dataset: python Scripts/datasetMaking_v2.py")
        print("   2. Train models: python Scripts/master_training_script.py")
        print("   3. Test predictions: python random_student_predictor.py")
    else:
        print("\n⚠️ Some tests failed. Please fix the issues above.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
