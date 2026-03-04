#!/usr/bin/env python3
"""
master_training_script.py
Orchestrates the complete training pipeline:
1. Generate realistic dataset
2. Preprocess data
3. Train all models
4. Save to Models/ folder

Run this script to retrain the entire system with new realistic course names.
"""

import os
import sys
import subprocess
import time

def run_script(script_path, description):
    """Run a Python script and report status."""
    print("\n" + "="*60)
    print(f"🚀 {description}")
    print("="*60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        elapsed = time.time() - start_time
        print(f"✅ Completed in {elapsed:.2f}s")
        print(result.stdout)
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("\n" + "╔"+"="*58+"╗")
    print("║" + " "*10 + "SMART COURSE RECOMMENDER - TRAINING PIPELINE" + " "*10 + "║")
    print("╚"+"="*58+"╝")
    
    # Ensure folders exist
    os.makedirs("Models", exist_ok=True)
    os.makedirs("Scripts", exist_ok=True)
    
    # Define training pipeline
    pipeline = [
        ("Scripts/datasetMaking_v2.py", "Step 1: Generate Realistic Dataset"),
        ("preprocess.py", "Step 2: Preprocess Dataset"),
        ("Scripts/train_success_model_v2.py", "Step 3: Train Success Prediction Model"),
        ("Scripts/train_cbf_v2.py", "Step 4: Train Content-Based Filtering"),
        ("Scripts/train_cf_v2.py", "Step 5: Train Collaborative Filtering"),
        ("Scripts/train_specialization_model_v2.py", "Step 6: Train Specialization Model"),
    ]
    
    # Check which scripts exist
    print("\n📋 Checking pipeline scripts...")
    missing_scripts = []
    
    for script, desc in pipeline:
        if os.path.exists(script):
            print(f"   ✅ {script}")
        else:
            print(f"   ⚠️  {script} (missing - will skip)")
            missing_scripts.append(script)
    
    if missing_scripts:
        print(f"\n⚠️  Warning: {len(missing_scripts)} script(s) not found. They will be skipped.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Execute pipeline
    print("\n" + "="*60)
    print("🔄 Starting Training Pipeline...")
    print("="*60)
    
    start_total = time.time()
    results = []
    
    for script, description in pipeline:
        if not os.path.exists(script):
            print(f"\n⏭️  Skipping {script} (not found)")
            results.append((description, "SKIPPED"))
            continue
        
        success = run_script(script, description)
        results.append((description, "SUCCESS" if success else "FAILED"))
        
        if not success:
            response = input("\n❓ Continue to next step? (y/n): ")
            if response.lower() != 'y':
                print("Pipeline stopped.")
                break
    
    # Summary
    total_time = time.time() - start_total
    
    print("\n" + "="*60)
    print("📊 TRAINING PIPELINE SUMMARY")
    print("="*60)
    
    for description, status in results:
        status_icon = "✅" if status == "SUCCESS" else ("⏭️" if status == "SKIPPED" else "❌")
        print(f"{status_icon} {description}: {status}")
    
    print(f"\n⏱️  Total time: {total_time/60:.2f} minutes")
    
    # Check models folder
    if os.path.exists("Models"):
        models = [f for f in os.listdir("Models") if f.endswith(('.pkl', '.npy'))]
        print(f"\n📦 Models in Models/ folder: {len(models)}")
        for model in sorted(models)[:10]:  # Show first 10
            print(f"   • {model}")
        if len(models) > 10:
            print(f"   ... and {len(models)-10} more")
    
    print("\n" + "="*60)
    print("✨ Pipeline Complete!")
    print("="*60)


if __name__ == "__main__":
    main()
