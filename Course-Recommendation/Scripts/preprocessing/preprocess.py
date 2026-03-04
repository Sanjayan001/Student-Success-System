#!/usr/bin/env python3
"""
preprocess.py
Load the synthetic Sri Lanka dataset, clean it, create TF-IDF course vectors,
encode ids, scale numeric features, and save artifacts for modeling.
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

# CONFIG - ORGANIZED VERSION
import os as _os
BASE_DIR = _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
INPUT_CSV = _os.path.join(BASE_DIR, "dataset", "sri_lanka_course_recommendation_dataset.csv")
OUTPUT_CLEAN = _os.path.join(BASE_DIR, "dataset", "dataset_clean.csv")
SCALER_PATH = _os.path.join(BASE_DIR, "Models", "scaler.pkl")
TFIDF_PATH = _os.path.join(BASE_DIR, "Models", "tfidf_course.pkl")
COURSE_INDEX_MAP_PATH = _os.path.join(BASE_DIR, "Models", "course_index_map.pkl")
STUDENT_ENCODER_PATH = _os.path.join(BASE_DIR, "Models", "student_encoder.pkl")
COURSE_ENCODER_PATH = _os.path.join(BASE_DIR, "Models", "course_encoder.pkl")

# Columns expected (the generator created these)
EXPECTED_COLS = [
    "student_id","gender","age","university","degree_program","current_year",
    "course_id","course_name","course_domain","course_difficulty",
    "previous_GPA","attendance_rate","risk_score","final_grade",
    "course_interest","job_market_demand_2035","employability_relevance","course_skills","recommended"
]

def safe_read_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Input CSV not found: {path}")
    return pd.read_csv(path)

def main():
    print(">> Loading dataset:", INPUT_CSV)
    df = safe_read_csv(INPUT_CSV)
    print("Initial shape:", df.shape)

    # quick info
    print("\n-- Column types and missing values --")
    print(df.dtypes)
    print(df.isna().sum())

    # keep only expected columns if extras exist
    cols_keep = [c for c in EXPECTED_COLS if c in df.columns]
    df = df[cols_keep]
    print("\nKeeping columns:", cols_keep)

    # Drop exact duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"Dropped duplicates: {before - len(df)} rows")

    # Fill missing course_name/course_skills/course_domain with placeholders
    df['course_name'] = df['course_name'].fillna("Unknown Course")
    df['course_skills'] = df['course_skills'].fillna("")
    df['course_domain'] = df['course_domain'].fillna("General")

    # For numeric columns, fillna with medians (but keep mask columns)
    num_cols = ['previous_GPA','attendance_rate','course_difficulty','job_market_demand_2035','course_interest','final_grade','risk_score']
    for c in num_cols:
        if c in df.columns:
            mask_col = f"{c}_was_nan"
            df[mask_col] = df[c].isna()
            df[c] = df[c].fillna(df[c].median())

    # Clip numeric ranges to reasonable values
    if 'previous_GPA' in df.columns:
        df['previous_GPA'] = df['previous_GPA'].clip(0,4)
    if 'attendance_rate' in df.columns:
        df['attendance_rate'] = df['attendance_rate'].clip(0,1)
    if 'course_difficulty' in df.columns:
        df['course_difficulty'] = df['course_difficulty'].clip(0,1)
    if 'job_market_demand_2035' in df.columns:
        df['job_market_demand_2035'] = df['job_market_demand_2035'].clip(0,1)
    if 'course_interest' in df.columns:
        df['course_interest'] = df['course_interest'].clip(0,1)
    if 'risk_score' in df.columns:
        df['risk_score'] = df['risk_score'].clip(0,1)
    if 'final_grade' in df.columns:
        df['final_grade'] = df['final_grade'].clip(0,100)

    # Create composite text column for TF-IDF
    df['course_text'] = (df['course_name'].astype(str) + ' ' +
                         df['course_skills'].astype(str) + ' ' +
                         df['course_domain'].astype(str))

    # Save cleaned CSV early
    df.to_csv(OUTPUT_CLEAN, index=False)
    print("Saved cleaned dataset to:", OUTPUT_CLEAN)

    # Scale numeric features with MinMaxScaler
    scaler_cols = [c for c in ['previous_GPA','attendance_rate','course_difficulty','job_market_demand_2035','course_interest'] if c in df.columns]
    print("Scaling columns:", scaler_cols)
    scaler = MinMaxScaler()
    df[scaler_cols] = scaler.fit_transform(df[scaler_cols])
    joblib.dump(scaler, SCALER_PATH)
    print("Saved scaler to:", SCALER_PATH)

    # Build TF-IDF on unique courses (avoid duplicates)
    print("Building TF-IDF vectors for course_text...")
    courses_df = df[['course_id','course_text']].drop_duplicates().set_index('course_id')
    tfidf = TfidfVectorizer(max_features=3000, ngram_range=(1,2), min_df=2, stop_words='english')
    course_tfidf = tfidf.fit_transform(courses_df['course_text'])
    joblib.dump(tfidf, TFIDF_PATH)
    print("Saved TF-IDF vectorizer to:", TFIDF_PATH)

    # create course_index_map: course_id -> index in TF-IDF matrix
    course_index_map = {cid: idx for idx, cid in enumerate(courses_df.index)}
    joblib.dump(course_index_map, COURSE_INDEX_MAP_PATH)
    print("Saved course_index_map to:", COURSE_INDEX_MAP_PATH, " (courses:", len(course_index_map), ")")

    # Label encode student_id and course_id for CF model later
    print("Encoding student_id and course_id to indices...")
    student_encoder = LabelEncoder()
    course_encoder = LabelEncoder()
    # Fit on full df to capture all ids
    df['student_idx'] = student_encoder.fit_transform(df['student_id'])
    df['course_idx'] = course_encoder.fit_transform(df['course_id'])
    joblib.dump(student_encoder, STUDENT_ENCODER_PATH)
    joblib.dump(course_encoder, COURSE_ENCODER_PATH)
    print("Saved student_encoder and course_encoder.")

    # Save final processed CSV for modeling step
    processed_out = _os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
    df.to_csv(processed_out, index=False)
    print("Saved processed dataset for modeling to:", processed_out)

    # Print small sample and summary stats
    print("\n-- Sample rows --")
    print(df.head(5).T)
    print("\n-- Dataset summary --")
    print(df.describe(include='all').T)

    print("\nPreprocessing finished. Artifacts created:")
    for p in [OUTPUT_CLEAN, processed_out, SCALER_PATH, TFIDF_PATH, COURSE_INDEX_MAP_PATH, STUDENT_ENCODER_PATH, COURSE_ENCODER_PATH]:
        print(" -", p)

if __name__ == "__main__":
    main()
