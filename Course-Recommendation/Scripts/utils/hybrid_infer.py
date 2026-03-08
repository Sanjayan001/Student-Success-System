# hybrid_infer_improved.py
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from gemini_explainer import generate_explanation
from template_explainer import generate_template_explanation
from new_user_explainer import generate_new_user_explanation
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine_similarity

# Paths - ORGANIZED VERSION
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DF_PATH = os.path.join(BASE_DIR, "dataset", "dataset_processed_for_modeling.csv")
TFIDF_PATH = os.path.join(BASE_DIR, "Models", "tfidf_course.pkl")
COURSE_INDEX_MAP_PATH = os.path.join(BASE_DIR, "Models", "course_index_map.pkl")
CF_STUDENT_FACTORS = os.path.join(BASE_DIR, "Models", "cf_alt_student_factors.npy")
CF_COURSE_FACTORS = os.path.join(BASE_DIR, "Models", "cf_alt_course_factors.npy")
CF_STUDENT_IDS = os.path.join(BASE_DIR, "Models", "cf_alt_student_ids.npy")
CF_COURSE_IDS = os.path.join(BASE_DIR, "Models", "cf_alt_course_ids.npy")
SUCCESS_MODEL = os.path.join(BASE_DIR, "Models", "logreg_success.pkl")
SUCCESS_SCALER = os.path.join(BASE_DIR, "Models", "success_scaler.pkl")
SPEC_MODEL = os.path.join(BASE_DIR, "Models", "spec_model_v2.pkl")  # Improved 39% accuracy model
SPEC_FEATURES = os.path.join(BASE_DIR, "Models", "spec_feature_cols_v2.pkl")
SPEC_LABELS = os.path.join(BASE_DIR, "Models", "spec_label_map_v2.pkl")
META_LR_MODEL = os.path.join(BASE_DIR, "Models", "meta_learner.pkl")
META_LR_WEIGHTS = os.path.join(BASE_DIR, "Models", "meta_learner_weights.pkl")
META_DEEP_MODEL = os.path.join(BASE_DIR, "Models", "meta_learner_deep.pkl")
META_DEEP_SCALER = os.path.join(BASE_DIR, "Models", "meta_learner_deep_scaler.pkl")

# Fusion weights (baseline - validated via evaluation)
W_CF = 0.40
W_CBF = 0.35
W_P = 0.20
W_JOB = 0.05

# Degree program → allowed course domains (for domain_restrict mode)
DEGREE_TO_DOMAINS = {
    "Artificial Intelligence":    ["AI", "Data Science", "Software Engineering"],
    "Computer Science":           ["Software Engineering", "AI", "Data Science", "Networking", "Cybersecurity"],
    "Information Technology":     ["Software Engineering", "Networking", "Cybersecurity", "AI"],
    "Data Science":               ["Data Science", "AI", "Software Engineering"],
    "Cybersecurity":              ["Cybersecurity", "Networking", "Software Engineering"],
    "Mechanical Engineering":     ["Mechanical", "Electrical", "Energy"],
    "Electrical Engineering":     ["Electrical", "Mechanical", "Energy", "Networking"],
    "Business Management":        ["Management", "Finance", "Law", "Ethics"],
    "Finance":                    ["Finance", "Management", "Law"],
    "Law":                        ["Law", "Ethics", "Management"],
    "Medicine":                   ["Healthcare", "Ethics"],
    "Nursing":                    ["Healthcare", "Ethics"],
    "Agriculture":                ["Agriculture", "Energy", "Ethics"],
    "Tourism and Hospitality":    ["Tourism", "Management"],
    "Renewable Energy":           ["Energy", "Electrical", "Mechanical"],
}

def load_artifacts():
    df = pd.read_csv(DF_PATH)
    tfidf = joblib.load(TFIDF_PATH)
    course_index_map = joblib.load(COURSE_INDEX_MAP_PATH)
    student_factors = np.load(CF_STUDENT_FACTORS)
    course_factors = np.load(CF_COURSE_FACTORS)
    student_ids = np.load(CF_STUDENT_IDS, allow_pickle=True)
    course_ids = np.load(CF_COURSE_IDS, allow_pickle=True)
    # optionally load success model
    try:
        clf = joblib.load(SUCCESS_MODEL)
        scaler = joblib.load(SUCCESS_SCALER)
    except Exception:
        clf = None
        scaler = None
    # optionally load meta-learner
    meta_model = None
    meta_weights = None
    meta_deep_model = None
    meta_deep_scaler = None
    try:
        if os.path.exists(META_LR_MODEL):
            meta_model = joblib.load(META_LR_MODEL)
        if os.path.exists(META_LR_WEIGHTS):
            meta_weights = joblib.load(META_LR_WEIGHTS)
        if os.path.exists(META_DEEP_MODEL):
            meta_deep_model = joblib.load(META_DEEP_MODEL)
        if os.path.exists(META_DEEP_SCALER):
            meta_deep_scaler = joblib.load(META_DEEP_SCALER)
    except Exception:
        meta_model = None
        meta_weights = None
        meta_deep_model = None
        meta_deep_scaler = None
    return (
        df,
        tfidf,
        course_index_map,
        student_factors,
        course_factors,
        student_ids,
        course_ids,
        clf,
        scaler,
        meta_model,
        meta_weights,
        meta_deep_model,
        meta_deep_scaler,
    )

def build_student_profile(df, student_id, tfidf, course_index_map, course_text_map=None):
    """Build a TF-IDF weighted student interest profile.

    Optimizations:
    - Use a pre-built course_text_map to avoid repeated DataFrame filtering.
    - Minimize per-row Python overhead.
    """
    rows = df[df["student_id"] == student_id]
    if rows.empty:
        return None
    # Collect course texts and weights
    texts = []
    weights = []
    for cid, fg in zip(rows["course_id"].tolist(), rows["final_grade"].tolist()):
        if cid in course_index_map:
            txt = (
                course_text_map[cid]
                if course_text_map and cid in course_text_map
                else rows.loc[rows["course_id"] == cid, "course_text"].iloc[0]
            )
            texts.append(txt)
            weights.append(fg if not pd.isna(fg) else 1.0)
    if not texts:
        return None
    mat = tfidf.transform(texts)
    w = np.array(weights, dtype=float)
    s = w.sum()
    if s <= 0:
        w = np.ones_like(w)
        s = w.sum()
    w = w / s
    profile = (mat.multiply(w[:, None])).sum(axis=0)
    prof = np.asarray(profile).ravel()
    nrm = np.linalg.norm(prof)
    if nrm > 0:
        prof = prof / nrm
    return prof

def get_cf_scores(student_id, student_ids, student_factors, course_factors):
    if student_id not in student_ids:
        return None
    u_idx = int(np.where(student_ids == student_id)[0][0])
    user_vec = student_factors[u_idx]
    preds = np.dot(user_vec, course_factors.T)
    # normalize to 0-1
    minp, maxp = preds.min(), preds.max()
    norm = (preds - minp) / (maxp - minp + 1e-9)
    return norm, preds

def compute_p_success(clf, scaler, student_row, course_row):
    # Build a one-row feature vector: previous_GPA, attendance_rate, course_difficulty, course_interest, job_market_demand_2035, risk_score
    X = pd.DataFrame([{
        'previous_GPA': student_row.get('previous_GPA', 0),
        'attendance_rate': student_row.get('attendance_rate', 0),
        'course_difficulty': course_row.get('course_difficulty', 0),
        'course_interest': student_row.get('course_interest', 0),
        'job_market_demand_2035': course_row.get('job_market_demand_2035', 0),
        'risk_score': student_row.get('risk_score', 0)
    }])
    if clf is None or scaler is None:
        # fallback heuristic
        gpa = X['previous_GPA'].iloc[0]
        diff = X['course_difficulty'].iloc[0]
        return 0.7 * gpa + 0.3 * (1 - diff)
    Xs = scaler.transform(X)
    prob = clf.predict_proba(Xs)[0,1]
    return float(prob)

def compute_mmr_rerank(scores, vectors, top_n=10, diversity_lambda=0.05):
    """
    Maximal Marginal Relevance (MMR) re-ranking.
    Balances relevance and diversity by greedily selecting courses that are
    high-scoring but dissimilar from already-selected ones.
    
    Args:
        scores: list of relevance scores (0-1)
        vectors: list of course vectors (for similarity)
        top_n: number of courses to select
        diversity_lambda: weight for diversity penalty (0=pure relevance, 1=pure diversity)
    
    Returns:
        list of indices in MMR order
    """
    n = len(scores)
    if n == 0:
        return []
    
    selected_indices = []
    remaining_indices = set(range(n))
    
    # Normalize scores
    max_score = max(scores) if scores else 1.0
    norm_scores = [s / max_score if max_score > 0 else 0 for s in scores]
    
    # Greedy selection
    for _ in range(min(top_n, n)):
        best_idx = None
        best_mmr = -float('inf')
        
        for idx in remaining_indices:
            relevance = norm_scores[idx]
            
            # Diversity penalty: average similarity to already-selected
            diversity_penalty = 0.0
            if selected_indices and vectors is not None:
                try:
                    selected_vecs = [vectors[i] for i in selected_indices]
                    current_vec = vectors[idx]
                    # Compute average cosine similarity
                    sims = [sklearn_cosine_similarity(
                        current_vec.reshape(1, -1),
                        vec.reshape(1, -1)
                    )[0, 0] for vec in selected_vecs]
                    diversity_penalty = np.mean(sims) if sims else 0.0
                except Exception:
                    # Fallback if vector ops fail
                    diversity_penalty = 0.0
            
            # MMR score = relevance - diversity_lambda * similarity
            mmr_score = relevance - diversity_lambda * diversity_penalty
            
            if mmr_score > best_mmr:
                best_mmr = mmr_score
                best_idx = idx
        
        if best_idx is not None:
            selected_indices.append(best_idx)
            remaining_indices.remove(best_idx)
    
    return selected_indices


def _compute_final_score(cf, cbf, p_succ, job, risk, weights):
    """Compute final score using provided weights dict.
    weights keys: cf, cbf, p, job
    """
    return (
        weights["cf"] * cf
        + weights["cbf"] * cbf
        + weights["p"] * p_succ
        + weights["job"] * (job * (1 - risk))
    )


def recommend(
    student_id,
    top_n=10,
    job_priority="Balanced",
    explain=True,
    diversity_lambda=0.05,
    scoring_mode: str = "auto",
    domain_restrict: bool = False,
):
    (
        df,
        tfidf,
        course_index_map,
        student_factors,
        course_factors,
        student_ids,
        course_ids,
        clf,
        scaler,
        meta_model,
        meta_weights,
        meta_deep_model,
        meta_deep_scaler,
    ) = load_artifacts()

    # Precompute course text map and vectors for speed
    course_rows = df.drop_duplicates("course_id").set_index("course_id")
    course_text_map = course_rows["course_text"].to_dict()
    course_domain_map = (
        course_rows["course_domain"].to_dict() if "course_domain" in course_rows.columns else {}
    )
    course_difficulty_map = (
        course_rows["course_difficulty"].to_dict() if "course_difficulty" in course_rows.columns else {}
    )
    job_market_map = (
        course_rows["job_market_demand_2035"].to_dict()
        if "job_market_demand_2035" in course_rows.columns
        else {}
    )

    # Build student profile
    stud_prof = build_student_profile(df, student_id, tfidf, course_index_map, course_text_map)
    cf_norm, cf_raw = get_cf_scores(student_id, student_ids, student_factors, course_factors)
    # Prepare arrays for per-course cbf scores (vectorized-ish)
    cbf_list = []
    for cid in course_ids:
        txt = course_text_map.get(cid, "")
        course_vec = tfidf.transform([txt]).toarray()[0]
        if stud_prof is None or np.linalg.norm(course_vec) == 0:
            cbf_list.append(0.0)
        else:
            s = cosine_similarity(stud_prof.reshape(1, -1), course_vec.reshape(1, -1)).flatten()[0]
            cbf_list.append((s + 1) / 2.0)
    cbf_arr = np.array(cbf_list)
    # normalize cbf_arr 0-1 (min-max) to avoid skew
    if cbf_arr.max() - cbf_arr.min() > 0:
        cbf_arr = (cbf_arr - cbf_arr.min()) / (cbf_arr.max() - cbf_arr.min())

    results = []
    # We will compute p_success per course using student averages (take first student's aggregate)
    student_rows = df[df['student_id'] == student_id]
    # if empty, fall back to global means
    if student_rows.empty:
        student_ref = df.iloc[0].to_dict()
    else:
        student_ref = student_rows.iloc[0].to_dict()

    # Domain restriction setup
    allowed_domains = None
    if domain_restrict:
        student_degree = student_ref.get('degree_program', None)
        if student_degree and student_degree in DEGREE_TO_DOMAINS:
            allowed_domains = set(DEGREE_TO_DOMAINS[student_degree])

    # Adapt fusion weights based on job priority
    jp = (job_priority or "Balanced").strip().lower()
    W_CF_eff, W_CBF_eff, W_P_eff, W_JOB_eff = W_CF, W_CBF, W_P, W_JOB
    if jp == "job market first":
        W_JOB_eff = 0.10
        W_CBF_eff = 0.30
    elif jp == "interest first":
        W_JOB_eff = 0.02
        W_CBF_eff = 0.38

    # Determine scoring mode
    # - "auto": prefer deep-learner if available, else meta-model/weights, else weighted
    # - "deep": force deep learning model
    # - "meta": force LogisticRegression meta-model/weights
    # - "weighted": fixed weights
    mode = scoring_mode or "auto"
    use_meta_deep = False
    use_meta_model = False
    use_meta_weights = False
    
    if mode == "auto":
        use_meta_deep = meta_deep_model is not None and meta_deep_scaler is not None
        if not use_meta_deep:
            use_meta_model = meta_model is not None
            use_meta_weights = (meta_weights is not None) and (not use_meta_model)
    elif mode == "deep":
        use_meta_deep = meta_deep_model is not None and meta_deep_scaler is not None
        if not use_meta_deep:
            use_meta_model = meta_model is not None
            use_meta_weights = (meta_weights is not None) and (not use_meta_model)
    elif mode == "meta":
        use_meta_model = meta_model is not None
        use_meta_weights = (meta_weights is not None) and (not use_meta_model)
    else:
        use_meta_deep = False
        use_meta_model = False
        use_meta_weights = False

    learned_weights = {
        "cf": W_CF_eff,
        "cbf": W_CBF_eff,
        "p": W_P_eff,
        "job": W_JOB_eff,
    }
    if use_meta_weights:
        # Expect structure {"coef": [w_cf, w_cbf, w_p, w_job], "intercept": b}
        try:
            coefs = meta_weights.get("coef", None)
            if coefs is not None and len(coefs) >= 4:
                learned_weights = {
                    "cf": float(coefs[0]),
                    "cbf": float(coefs[1]),
                    "p": float(coefs[2]),
                    "job": float(coefs[3]),
                }
        except Exception:
            pass

    for idx, cid in enumerate(course_ids):
        # Domain restriction filter
        if allowed_domains is not None:
            if course_domain_map.get(cid, '') not in allowed_domains:
                continue
        job = float(job_market_map.get(cid, 0.0))
        risk = float(student_ref.get('risk_score', 0))
        cbf_score = float(cbf_arr[idx])
        cf_score = float(cf_norm[idx]) if (cf_norm is not None) else 0.0
        # Build course_row lightweight dict for success predictor
        course_row = {
            'course_difficulty': float(course_difficulty_map.get(cid, 0.5)),
            'course_interest': float(student_ref.get('course_interest', 0.5)),
            'job_market_demand_2035': job,
        }
        p_success = compute_p_success(clf, scaler, student_ref, course_row)
        p_success = max(0.0, min(1.0, p_success))

        if use_meta_deep:
            # Deep learning fusion
            X = np.array([[cf_score, cbf_score, p_success, job, risk]], dtype=float)
            try:
                X_scaled = meta_deep_scaler.transform(X)
                final_score = float(meta_deep_model.predict_proba(X_scaled)[:, 1][0])
            except Exception:
                final_score = _compute_final_score(cf_score, cbf_score, p_success, job, risk, learned_weights)
        elif use_meta_model:
            # LogisticRegression fusion
            X = np.array([[cf_score, cbf_score, p_success, job, risk]], dtype=float)
            try:
                if hasattr(meta_model, 'predict_proba'):
                    final_score = float(meta_model.predict_proba(X)[:, 1][0])
                else:
                    final_score = float(meta_model.predict(X)[0])
            except Exception:
                final_score = _compute_final_score(cf_score, cbf_score, p_success, job, risk, learned_weights)
        else:
            final_score = _compute_final_score(cf_score, cbf_score, p_success, job, risk, learned_weights)

        cname = course_rows.loc[cid, 'course_name'] if 'course_name' in course_rows.columns and cid in course_rows.index else cid
        results.append({
            "course_id": cid,
            "course_name": cname,
            "final_score": final_score,
            "cf_score": cf_score,
            "cbf_score": cbf_score,
            "p_success": p_success,
            "job_market": job,
            "risk_score": risk,
            "explanation": ""
        })
    
    # Sort by score first
    out = pd.DataFrame(results)
    out = out.sort_values("final_score", ascending=False).head(top_n * 2)  # Get 2x for re-ranking
    
    # Apply MMR re-ranking to improve diversity
    if diversity_lambda > 0 and len(out) > 0:
        # Build simple course text vectors for diversity computation
        course_vectors = []
        for idx, row in out.iterrows():
            cid = row['course_id']
            course_row = df[df['course_id'] == cid]
            if not course_row.empty:
                course_text = course_row['course_text'].iloc[0]
                # Quick: use TF-IDF to get a vector
                try:
                    vec = tfidf.transform([course_text]).toarray().ravel()
                    if np.linalg.norm(vec) > 0:
                        vec = vec / np.linalg.norm(vec)
                    course_vectors.append(vec)
                except Exception:
                    course_vectors.append(None)
            else:
                course_vectors.append(None)
        
        scores_for_mmr = out['final_score'].tolist()
        mmr_indices = compute_mmr_rerank(
            scores_for_mmr,
            course_vectors,
            top_n=top_n,
            diversity_lambda=diversity_lambda
        )
        out = out.iloc[mmr_indices].reset_index(drop=True)
    else:
        out = out.head(top_n)
    
    # Generate explanations: optional for speed/evaluation
    if explain:
        explanations = []
        print(f"🤖 Generating explanations (AI for top 3, templates for rest)...")
        for idx, row in out.iterrows():
            rank = len(explanations) + 1
            student_data = {
                'student_id': student_id,
                'previous_GPA': student_ref.get('previous_GPA', 0),
                'attendance_rate': student_ref.get('attendance_rate', 0),
                'risk_score': row['risk_score']
            }
            cid = row['course_id']
            course_data = {
                'course_name': row['course_name'],
                'course_domain': course_domain_map.get(cid, 'General'),
                'course_difficulty': course_difficulty_map.get(cid, 0.5),
                'job_market': row['job_market']
            }
            scores = {
                'cf_score': row['cf_score'],
                'cbf_score': row['cbf_score'],
                'p_success': row['p_success'],
                'final_score': row['final_score']
            }
            if rank <= 3:
                try:
                    explanation = generate_explanation(student_data, course_data, scores)
                except Exception:
                    explanation = generate_template_explanation(student_data, course_data, scores)
            else:
                explanation = generate_template_explanation(student_data, course_data, scores)
            explanations.append(explanation)
        out['explanation'] = explanations
    else:
        out['explanation'] = [""] * len(out)
    
    # Save CSV
    out.to_csv(f"recommendations_{student_id}.csv", index=False)
    return out

def recommend_new_user(skills, interests, gpa, top_n=10, job_priority="Balanced", explain=False):
    """
    Cold-start recommendation for new users without student_id.
    
    Args:
        skills (str): Comma-separated skills (e.g., "Python, Machine Learning, Data Analysis")
        interests (str): Comma-separated interest areas (e.g., "AI, Software Engineering")
        gpa (float): Student's GPA (0.0-4.0 scale)
        top_n (int): Number of recommendations
        job_priority (str): "Interest First", "Balanced", or "Job Market First"
        explain (bool): Generate explanations (slower)
    
    Returns:
        DataFrame with recommended courses
    """
    df, tfidf, course_index_map, student_factors, course_factors, student_ids, course_ids, clf, scaler, _meta_model, _meta_weights, _meta_deep_model, _meta_deep_scaler = load_artifacts()
    
    # Create synthetic student profile from skills
    skills_text = skills.lower().strip()
    interests_text = interests.lower().strip()
    combined_text = f"{skills_text} {interests_text}"
    
    # Build user profile vector from input text
    user_profile_vec = tfidf.transform([combined_text]).toarray()[0]
    if np.linalg.norm(user_profile_vec) > 0:
        user_profile_vec = user_profile_vec / np.linalg.norm(user_profile_vec)
    
    # Cold-start fusion weights (no CF available)
    W_CBF_CS = 0.45  # Boost content-based
    W_P_CS = 0.30    # Success prediction important
    W_JOB_CS = 0.25  # Job market relevance
    
    # Adjust based on job priority
    jp = (job_priority or "Balanced").strip().lower()
    if jp == "job market first":
        W_CBF_CS, W_P_CS, W_JOB_CS = 0.35, 0.25, 0.40
    elif jp == "interest first":
        W_CBF_CS, W_P_CS, W_JOB_CS = 0.55, 0.30, 0.15
    
    results = []
    course_vectors = []
    
    # Create synthetic student reference for success prediction
    student_ref = {
        'previous_GPA': gpa,
        'attendance_rate': 0.85,  # Assume good attendance
        'risk_score': max(0, min(1, (4.0 - gpa) / 4.0)),  # Lower GPA = higher risk
        'study_hours_week': 15.0,
        'previous_courses_taken': 5
    }
    
    for idx, cid in enumerate(course_ids):
        row = df[df['course_id'] == cid]
        if row.empty:
            continue
        
        course_row = row.iloc[0].to_dict()
        course_text = course_row.get('course_text', '')
        course_domain = course_row.get('course_domain', '')
        
        # Filter by interests if specified
        if interests_text and course_domain:
            domain_lower = course_domain.lower()
            interest_list = [i.strip() for i in interests_text.split(',')]
            if not any(interest in domain_lower for interest in interest_list):
                continue  # Skip if not in interest areas
        
        # Compute CBF score
        course_vec = tfidf.transform([course_text]).toarray()[0]
        if np.linalg.norm(course_vec) > 0 and np.linalg.norm(user_profile_vec) > 0:
            cbf_score = cosine_similarity(user_profile_vec.reshape(1, -1), course_vec.reshape(1, -1)).flatten()[0]
            cbf_score = (cbf_score + 1) / 2.0  # Map [-1,1] to [0,1]
        else:
            cbf_score = 0.0
        
        # Compute success prediction
        p_success = compute_p_success(clf, scaler, student_ref, course_row)
        p_success = max(0.0, min(1.0, p_success))
        
        # Job market score
        job = float(course_row.get('job_market_demand_2035', 0))
        risk = student_ref['risk_score']
        
        # Cold-start fusion (no CF component)
        final_score = (
            W_CBF_CS * cbf_score +
            W_P_CS * p_success +
            W_JOB_CS * (job * (1 - risk))
        )
        
        results.append({
            'course_id': cid,
            'course_name': course_row.get('course_name', 'Unknown'),
            'course_domain': course_domain,
            'cbf_score': cbf_score,
            'p_success': p_success,
            'job_market': job,
            'risk_score': risk,
            'final_score': final_score
        })
        
        # Store course vector for MMR
        if np.linalg.norm(course_vec) > 0:
            course_vectors.append(course_vec / np.linalg.norm(course_vec))
        else:
            course_vectors.append(None)
    
    if not results:
        return pd.DataFrame()
    
    out = pd.DataFrame(results)
    out = out.sort_values('final_score', ascending=False).reset_index(drop=True)
    
    # Apply MMR re-ranking for diversity
    if len(out) > top_n:
        scores_for_mmr = out['final_score'].tolist()
        mmr_indices = compute_mmr_rerank(
            scores_for_mmr,
            course_vectors,
            top_n=top_n,
            diversity_lambda=0.05
        )
        out = out.iloc[mmr_indices].reset_index(drop=True)
    else:
        out = out.head(top_n)
    
    # Generate explanations if requested
    if explain:
        explanations = []
        user_profile = {
            'skills': skills,
            'interests': interests,
            'gpa': gpa
        }
        for idx, row in out.iterrows():
            rank = idx + 1
            course_data = {
                'course_name': row['course_name'],
                'course_domain': row['course_domain'],
                'course_difficulty': df[df['course_id'] == row['course_id']].iloc[0].get('course_difficulty', 0.5),
                'job_market': row['job_market']
            }
            scores = {
                'cbf_score': row['cbf_score'],
                'p_success': row['p_success'],
                'final_score': row['final_score']
            }
            # Use detailed new user explanation
            explanation = generate_new_user_explanation(user_profile, course_data, scores, rank)
            explanations.append(explanation)
        out['explanation'] = explanations
    else:
        out['explanation'] = [""] * len(out)
    
    return out


if __name__ == "__main__":
    sid = input("Enter student_id: ").strip()
    print("Computing recommendations for", sid)
    out = recommend(sid, top_n=10)
    print(out.to_string(index=False))
    print(f"Saved recommendations to recommendations_{sid}.csv")
