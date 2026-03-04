# Model Training & Improvement Roadmap

## Current State (Post-Evaluation)

### Metrics Baseline
- **Precision@10:** 0.7778 (77.78% of top-10 are relevant)
- **Recall@10:** 0.4518 (we capture ~45% of relevant courses)
- **NDCG@10:** 0.9195 (ranking quality is excellent)
- **Coverage:** 0.9600 (96% of courses get recommended)
- **Diversity:** 0.1301 (low – recommendations are similar within top-10)

---

## Implemented Improvements (Jan 2, 2026)

### 1. ✅ Maximal Marginal Relevance (MMR) Re-ranking
- **File:** `hybrid_infer.py`
- **What:** Greedy re-ranking that balances relevance and diversity
- **Formula:** `MMR_score = relevance − λ × avg_similarity_to_selected`
- **Parameter:** `diversity_lambda` (default: 0.05)
- **Expected Gain:** +5–10% diversity, minimal precision loss
- **Usage:** `recommend(sid, diversity_lambda=0.05)` or `0.10` for more diversity

### 2. ✅ Fusion Weight Meta-Learner
- **File:** `meta_learner.py`
- **What:** Ridge regression learns optimal weights from historical outcomes
- **Current Fixed Weights:**
  - CF: 0.40, CBF: 0.35, Success: 0.20, Job: 0.05
- **Learned Weights:** Run `python meta_learner.py` to discover optimal blend
- **Expected Gain:** +3–7% overall score quality if learned weights differ significantly

### 3. ✅ Contextual Fusion Weights
- **File:** `hybrid_infer.py`
- **What:** Adapts weights based on `job_priority` preference
  - **"Interest First":** CBF ↑ 0.38, Job ↓ 0.02
  - **"Balanced":** CF 0.40, CBF 0.35, Success 0.20, Job 0.05
  - **"Job Market First":** Job ↑ 0.10, CBF ↓ 0.30
- **Expected Gain:** +2–4% relevance for user-aligned recommendations

### 4. ✅ Secure API & Optional Explanations
- **File:** `gemini_explainer.py`, `hybrid_infer.py`
- **What:** Load API key from environment; skip explanations for speed (`explain=False`)
- **Usage:** `recommend(sid, explain=False)` for fast batch evaluation

---

## Planned Improvements (Next Steps)

### Phase 1: Enhance Individual Models (2–3 days)

#### A. Success Prediction Model (Logistic Regression)
**Current:** 80% accuracy, 89% AUC-ROC (good baseline)  
**Goal:** Calibrate probabilities + domain-specific thresholds → +2–3% practical improvement

**Actions:**
1. Add feature interactions: `GPA×difficulty`, `attendance×risk`
2. Calibrate probabilities (Platt scaling or isotonic regression)
3. Tune pass/fail threshold per domain (not global 0.5)
4. Validation: stratified 5-fold CV with proper stratification on domains

**Expected Gain:** Better calibration + fewer false positives in high-risk domains

**Implementation:**
```python
# In train_success_model.py
from sklearn.calibration import CalibratedClassifierCV

# Add interactions
X['gpa_x_difficulty'] = X['previous_GPA'] * X['course_difficulty']
X['att_x_risk'] = X['attendance_rate'] * X['risk_score']

# Calibrate after training
clf_calibrated = CalibratedClassifierCV(clf, method='isotonic', cv=5)
clf_calibrated.fit(X_train_s, y_train)
```

---

#### B. Specialization Model (XGBoost v2)
**Current:** 39% accuracy (6x random baseline)  
**Goal:** Better feature engineering + hyperparameter tuning → 50%+ accuracy

**Actions:**
1. **Feature Engineering (High Impact):**
   - Recency-weighted domain counts (recent courses weighted higher)
   - Skill embeddings: TFIDF on course_skills → 10D reduction via PCA → average per domain
   - Progression signals: (year 4 courses) − (year 1 courses) to capture specialization path
   - Domain transition matrix: encode how students move between domains

2. **Hyperparameter Tuning:**
   - Random search or Optuna on: `learning_rate` [0.01, 0.3], `max_depth` [4, 10], `n_estimators` [100, 500], `subsample` [0.7, 1.0], `colsample_bytree` [0.6, 1.0]
   - Early stopping on validation set
   - Class weights if imbalanced

3. **Interpretability & Pruning:**
   - SHAP analysis to identify top 10 features
   - Drop low-impact features to reduce noise

4. **Validation:**
   - Stratified k-fold on domains to avoid data leakage

**Expected Gain:** 39% → 50%+ (10–20% relative improvement)

**Implementation sketch:**
```python
# In train_specialization_model.py
import optuna

def objective(trial):
    lr = trial.suggest_float('learning_rate', 0.01, 0.3)
    max_depth = trial.suggest_int('max_depth', 4, 10)
    # ... train and return validation accuracy
    return accuracy

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=50)
best_params = study.best_params
```

---

#### C. Collaborative Filtering (CF)
**Current:** TruncatedSVD (60 factors)  
**Goal:** Implicit ALS with confidence weighting → better handle sparse interactions

**Actions:**
1. Switch to `implicit` library (ALS with confidence)
2. Confidence weights: `c = 1 + α × grade` (higher grades = higher confidence)
3. Tune factors, alpha, regularization
4. Offline eval: Recall@K on held-out users

**Expected Gain:** Better coverage of long-tail courses; +2–5% Recall@K

**Implementation:**
```python
import implicit

# Build interaction matrix with confidence weights
confidences = data['final_grade'].values / 100.0  # 0-1 range
matrix = csr_matrix((confidences, (users, items)), shape=(n_users, n_items))

# Train
model = implicit.als.AlternatingLeastSquares(factors=60, regularization=0.05)
model.fit(matrix)
```

---

#### D. Content-Based Filtering (CBF)
**Current:** TF-IDF on course text  
**Goal:** Semantic embeddings (SBERT) for better course matching

**Actions:**
1. Install: `pip install sentence-transformers`
2. Replace TF-IDF with `sentence-transformers/all-MiniLM-L6-v2`
3. Embed course text (name + skills + domain) → 384D vectors
4. Use cosine similarity (same as before, but semantically richer)

**Expected Gain:** Better matching on synonyms + semantic relevance; +3–5% CBF quality

**Implementation:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Embed each course
for cid, text in course_texts.items():
    embedding = model.encode(text)  # 384D
    course_embeddings[cid] = embedding
```

---

### Phase 2: Advanced Techniques (4–5 days)

#### E. Learned Fusion via Meta-Learner
**What:** Already implemented in `meta_learner.py`  
**Expected Gain:** +3–7% if learned weights differ from fixed

**To run:**
```bash
python meta_learner.py
```

Then in `hybrid_infer.py`:
```python
learned_result = joblib.load("meta_learner_weights.pkl")
W_CF, W_CBF, W_P, W_JOB = learned_result['weights']
```

---

#### F. Probability Calibration
**What:** Ensure success predictions map correctly to real pass rates

**Actions:**
1. Train model as usual
2. Apply Platt or isotonic calibration on held-out calibration set
3. Validate: expected calibration error (ECE) < 0.05

**Expected Gain:** Better reliability of P_success; confidence intervals more trustworthy

---

#### G. Cold-Start Handling
**What:** New students with no history

**Current Fallback:** Not optimized  
**Improvement:** Use LightFM (CF + content side features)

**Actions:**
```python
from lightfm import LightFM

model = LightFM(no_components=60, loss='warp', learning_schedule='adadelta')
model.fit(interactions, item_features=course_features, epochs=10)

# For new student, use course_features to recommend
```

**Expected Gain:** Non-zero recommendations for cold-start students

---

### Phase 3: Online Learning & Reinforcement Learning (5–6 days, optional for PP2)

#### H. Contextual Bandits (Exploration)
**What:** Incrementally improve recommendations via exploration-exploitation

**Approach:**
1. Use LinUCB or Thompson Sampling
2. Reward: click/enroll/pass outcome
3. Context: student features + course features
4. Offline evaluation: IPS (Inverse Probability Scoring) to test policies safely

**Expected Gain:** Over time, system learns which recommendations students prefer

---

## Testing & Validation

### Quick Test Script
```bash
# Run evaluation with MMR
python evaluate_recommendations.py

# Check if diversity improved
# Expected: Diversity score > 0.20 (was 0.13)
```

### Before-After Comparison
```python
# Run both:
# - diversity_lambda=0.0 (baseline)
# - diversity_lambda=0.05 (with MMR)
# Compare metrics
```

---

## Timeline for PP2 (75% Milestone)

| Phase | Task | Time | Priority |
|-------|------|------|----------|
| 1A | Success model: interactions + calibration | 1 day | 🔴 HIGH |
| 1B | Specialization: features + hyperparams | 2 days | 🔴 HIGH |
| 1C | CF: implicit ALS | 1 day | 🟡 MEDIUM |
| 1D | CBF: SBERT embeddings | 1 day | 🟡 MEDIUM |
| 2E | Meta-learner: integrate learned weights | 0.5 days | 🟢 LOW (already coded) |
| 2F | Probability calibration | 0.5 days | 🟢 LOW |
| Test | End-to-end validation | 1 day | 🔴 HIGH |
| **TOTAL** | | ~7 days | |

---

## Expected PP2 Metrics

**Conservative Estimate (Phase 1 only):**
- Precision@10: 0.78 → 0.81 (+3.8%)
- Recall@10: 0.45 → 0.50 (+11%)
- NDCG@10: 0.92 → 0.94 (+2%)
- Diversity: 0.13 → 0.22 (+69% with MMR)

**Optimistic (Phase 1 + 2):**
- Precision@10: 0.78 → 0.84 (+7.7%)
- Recall@10: 0.45 → 0.54 (+20%)
- NDCG@10: 0.92 → 0.96 (+4%)
- Diversity: 0.13 → 0.25 (+92%)

---

## Deployment & Production Considerations

### API Deprecation
- `google.generativeai` → Migrate to `google.genai` (when stable)
- Update `requirements.txt` with new package version

### Scalability
- Current: 10k students, 500 courses (CSV-based, single-machine)
- For production: PostgreSQL + Redis cache + distributed training
- Model serving: FastAPI + Docker

---

## Files to Update Next

1. `train_success_model.py` → Add interactions, calibration
2. `train_specialization_model.py` → Feature engineering, hyperparameter tuning
3. `train_cf.py` → Switch to implicit ALS
4. `train_cbf.py` → Switch to SBERT
5. `hybrid_infer.py` → Integrate learned weights from meta_learner.pkl
6. `evaluate_recommendations.py` → Add per-domain metrics, significance tests

---

## Notes

- All improvements are backward-compatible; can fall back to fixed weights if learned weights are worse.
- MMR re-ranking is lightweight (O(k²)) and can be disabled by setting `diversity_lambda=0`.
- Prioritize Phase 1A (success calibration) and 1B (specialization features) for quickest gains.

---

**Next Action:** Pick one improvement from Phase 1 and implement it fully (including tests). Recommended order: **1A → 1B → 1C → 1D**.
