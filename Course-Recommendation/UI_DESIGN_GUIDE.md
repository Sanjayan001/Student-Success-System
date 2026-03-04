# 🎨 User Interface Design Guide
## Course Recommendation System with Gemini XAI

---

## 📋 Part 1: USER INPUTS (What Students Enter)

### **Minimal Required Inputs** (Authentication & Basic)

```
1. Student ID / Login Credentials
   - Input Type: Text field
   - Example: "S01290"
   - Purpose: Identify student, load their profile
   - Validation: Must exist in database

2. Number of Recommendations
   - Input Type: Slider or dropdown
   - Range: 5-20 courses
   - Default: 10
   - Purpose: Control result size
```

**Why Minimal?**  
Your system already has all student data in `dataset_processed_for_modeling.csv`:
- GPA, attendance, risk score, past courses, interests
- No need to re-enter what you already know!

---

### **Optional Advanced Filters** (User Preferences)

```
3. Course Domain Filter
   - Input Type: Multi-select checkboxes
   - Options: [ ] AI  [ ] Data Science  [ ] Cybersecurity
             [ ] Networking  [ ] Healthcare  [ ] Finance
             [ ] Engineering  [ ] Law  [ ] Agriculture
   - Default: All selected
   - Purpose: Focus recommendations on preferred areas

4. Difficulty Level Preference
   - Input Type: Range slider
   - Range: Easy (0.0) ←→ Hard (1.0)
   - Default: 0.3 - 0.7 (moderate)
   - Purpose: Match student comfort level

5. Job Market Priority
   - Input Type: Dropdown
   - Options: "Job Demand Focus", "Interest Focus", "Balanced"
   - Default: Balanced
   - Purpose: Adjust W_JOB weight in hybrid scoring

6. Semester/Year Filter
   - Input Type: Dropdown
   - Options: "All", "Current Semester Only", "Next Semester"
   - Purpose: Show only available courses

7. Exclude Already Taken
   - Input Type: Checkbox (checked by default)
   - Purpose: Don't recommend completed courses
```

---

## 📤 Part 2: SYSTEM OUTPUTS (What Students See)

### **Primary Output: Recommendation List**

```
┌─────────────────────────────────────────────────────────────────┐
│  📚 Your Top 10 Personalized Course Recommendations             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1️⃣  [★★★★★ 0.784] Data Science Fundamentals 191               │
│      📊 Domain: Data Science  |  📈 Difficulty: 72%             │
│      💼 Job Demand (2035): 89.6%  |  ✅ Success Rate: 73%       │
│                                                                  │
│      💬 AI Advisor Says:                                        │
│      "Given your solid 3.2 GPA and consistent 85% attendance,   │
│       you're well-positioned to excel in this course. Students  │
│       with similar profiles rated this highly (71% match), and  │
│       it aligns perfectly with the booming data science job     │
│       market for 2035!"                                         │
│                                                                  │
│      [📄 View Details] [⭐ Add to Wishlist] [✉️ Ask Advisor]    │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  2️⃣  [★★★★☆ 0.775] Finance Fundamentals 25                    │
│      💰 Domain: Finance  |  📈 Difficulty: 45%                  │
│      💼 Job Demand (2035): 43.3%  |  ✅ Success Rate: 74%       │
│                                                                  │
│      💬 AI Advisor Says:                                        │
│      "This course is an excellent match! With a 100% similarity │
│       to successful students and a 74% predicted success rate,  │
│       we're confident you'll do great here..."                  │
│                                                                  │
│      [📄 View Details] [⭐ Add to Wishlist] [✉️ Ask Advisor]    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

       [🔄 Refresh Recommendations] [⚙️ Adjust Filters]
```

### **Output Components Breakdown**

#### **For Each Recommendation, Show:**

1. **Rank & Score**
   - Position: 1, 2, 3...
   - Visual: Star rating (★★★★★)
   - Numerical: 0.784 / 1.0
   - Color code: Green (>0.7), Yellow (0.5-0.7), Red (<0.5)

2. **Course Information**
   - Course Name: "Data Science Fundamentals 191"
   - Course ID: "C191" (smaller text)
   - Domain: Icon + text (📊 Data Science)
   - Difficulty: Progress bar + percentage

3. **Key Metrics (Icon + Percentage)**
   - 💼 Job Market Demand 2035: 89.6%
   - ✅ Success Probability: 73%
   - 🎯 Content Match: 91% (CBF score)
   - 👥 Similar Students: 71% (CF score)

4. **Gemini XAI Explanation**
   - Natural language, 2-3 sentences
   - Personalized to student
   - Encouraging tone
   - Evidence-based

5. **Action Buttons**
   - "View Details" → Full course page
   - "Add to Wishlist" → Save for later
   - "Ask Advisor" → Human consultation
   - "Enroll Now" → Registration (if open)

---

### **Secondary Outputs**

#### **Student Dashboard (Top of Page)**

```
┌─────────────────────────────────────────────────────────────────┐
│  👤 Welcome, Student S01290!                                     │
│                                                                  │
│  📊 Your Academic Profile:                                      │
│  • GPA: 3.2 / 4.0  (Good Standing)                             │
│  • Attendance: 85%  (Excellent)                                │
│  • Risk Score: 0.26  (Low Risk)                                │
│  • Completed Courses: 24                                       │
│  • Current Year: 3                                             │
│                                                                  │
│  🎯 Recommended Specialization: Computer Science               │
│     (Confidence: 87%)                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### **Visualization Panel (Optional)**

```
┌─────────────────────────────────────────────────────────────────┐
│  📈 Your Recommendation Breakdown                               │
│                                                                  │
│  [Pie Chart]                                                    │
│   40% Collaborative Filtering (similar students)               │
│   35% Content Match (your interests)                           │
│   20% Success Prediction (your profile)                        │
│    5% Job Market Trends                                        │
│                                                                  │
│  [Bar Chart: Top Domains]                                      │
│   AI & Data Science:  ████████████ (5 courses)                │
│   Finance:            ██████ (2 courses)                       │
│   Engineering:        ████ (3 courses)                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### **Comparison View (When Multiple Courses Selected)**

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚖️ Compare Courses Side-by-Side                                │
├──────────────────┬──────────────────┬──────────────────────────┤
│                  │ Data Science 191 │ Finance 25               │
├──────────────────┼──────────────────┼──────────────────────────┤
│ Overall Score    │ ★★★★★ 0.78      │ ★★★★☆ 0.77              │
│ Difficulty       │ 72% (Moderate)   │ 45% (Easy)               │
│ Success Rate     │ 73%              │ 74%                      │
│ Job Demand       │ 89.6% (High)     │ 43.3% (Moderate)         │
│ Prerequisites    │ Intro to Data    │ None                     │
│ Workload         │ 12 hrs/week      │ 8 hrs/week               │
└──────────────────┴──────────────────┴──────────────────────────┘
```

#### **Export Options**

- 📄 **Download PDF Report**: Detailed recommendations with explanations
- 📧 **Email to Advisor**: Share with academic counselor
- 💾 **Save to Profile**: Bookmark for later
- 📱 **Share Link**: Get shareable URL

---

## 🖥️ Part 3: IMPLEMENTATION EXAMPLES

### **Option A: Simple Web Form (HTML/CSS/JS)**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Course Recommender</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 50px auto; }
        .input-group { margin: 20px 0; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 100%; padding: 10px; font-size: 16px; }
        button { background: #4CAF50; color: white; padding: 15px 30px; 
                 border: none; cursor: pointer; font-size: 18px; }
        .recommendation { border: 1px solid #ddd; padding: 20px; margin: 15px 0; 
                         border-radius: 8px; }
        .score { color: #4CAF50; font-size: 24px; font-weight: bold; }
        .explanation { background: #f0f8ff; padding: 15px; border-radius: 5px; 
                      margin-top: 10px; }
    </style>
</head>
<body>
    <h1>🎓 Course Recommendation System</h1>
    
    <!-- INPUT FORM -->
    <form id="recommenderForm">
        <div class="input-group">
            <label>Student ID:</label>
            <input type="text" id="studentId" placeholder="e.g., S01290" required>
        </div>
        
        <div class="input-group">
            <label>Number of Recommendations:</label>
            <select id="numRecs">
                <option value="5">5 courses</option>
                <option value="10" selected>10 courses</option>
                <option value="15">15 courses</option>
                <option value="20">20 courses</option>
            </select>
        </div>
        
        <div class="input-group">
            <label>Preferred Domains (select multiple):</label>
            <select id="domains" multiple style="height: 150px;">
                <option value="AI" selected>Artificial Intelligence</option>
                <option value="Data Science" selected>Data Science</option>
                <option value="Cybersecurity">Cybersecurity</option>
                <option value="Finance">Finance</option>
                <option value="Healthcare">Healthcare</option>
                <option value="Engineering">Engineering</option>
            </select>
        </div>
        
        <button type="submit">🔍 Get Recommendations</button>
    </form>
    
    <!-- OUTPUT AREA -->
    <div id="results" style="margin-top: 40px;"></div>
    
    <script>
        document.getElementById('recommenderForm').onsubmit = async (e) => {
            e.preventDefault();
            
            const studentId = document.getElementById('studentId').value;
            const numRecs = document.getElementById('numRecs').value;
            const domains = Array.from(document.getElementById('domains').selectedOptions)
                                .map(opt => opt.value);
            
            // Call backend API
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({studentId, numRecs, domains})
            });
            
            const data = await response.json();
            displayResults(data);
        };
        
        function displayResults(recommendations) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h2>📚 Your Personalized Recommendations</h2>';
            
            recommendations.forEach((rec, idx) => {
                resultsDiv.innerHTML += `
                    <div class="recommendation">
                        <h3>${idx + 1}. ${rec.course_name}</h3>
                        <p class="score">★ ${rec.final_score.toFixed(3)} / 1.0</p>
                        <p><strong>Domain:</strong> ${rec.course_domain || 'General'}</p>
                        <p><strong>Success Rate:</strong> ${(rec.p_success * 100).toFixed(1)}%</p>
                        <p><strong>Job Market Demand:</strong> ${(rec.job_market * 100).toFixed(1)}%</p>
                        <div class="explanation">
                            <strong>💬 AI Advisor Says:</strong><br>
                            ${rec.explanation}
                        </div>
                        <button onclick="viewDetails('${rec.course_id}')">View Details</button>
                        <button onclick="addToWishlist('${rec.course_id}')">Add to Wishlist</button>
                    </div>
                `;
            });
        }
        
        function viewDetails(courseId) {
            alert('Viewing details for ' + courseId);
            // Navigate to course detail page
        }
        
        function addToWishlist(courseId) {
            alert('Added ' + courseId + ' to wishlist!');
            // Save to user's wishlist
        }
    </script>
</body>
</html>
```

---

### **Option B: Flask Backend API**

```python
# app.py
from flask import Flask, render_template, request, jsonify
from hybrid_infer import recommend
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    student_id = data.get('studentId')
    num_recs = int(data.get('numRecs', 10))
    domains = data.get('domains', [])
    
    # Generate recommendations
    recs = recommend(student_id, top_n=num_recs)
    
    # Filter by domains if specified
    if domains and len(domains) > 0:
        recs = recs[recs['course_domain'].isin(domains)]
    
    # Convert to JSON
    result = recs.to_dict('records')
    return jsonify(result)

@app.route('/api/student/<student_id>/profile')
def get_student_profile(student_id):
    # Load student data
    df = pd.read_csv('dataset_processed_for_modeling.csv')
    student_data = df[df['student_id'] == student_id].iloc[0]
    
    return jsonify({
        'student_id': student_id,
        'gpa': float(student_data['previous_GPA']),
        'attendance': float(student_data['attendance_rate']),
        'risk_score': float(student_data['risk_score']),
        'courses_taken': int(df[df['student_id'] == student_id].shape[0])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

### **Option C: Streamlit Dashboard (Fastest to Build)**

```python
# streamlit_app.py
import streamlit as st
import pandas as pd
from hybrid_infer import recommend
import plotly.express as px

st.set_page_config(page_title="Course Recommender", page_icon="🎓", layout="wide")

# Title
st.title("🎓 AI-Powered Course Recommendation System")
st.markdown("*Powered by Hybrid ML + Gemini XAI*")

# Sidebar - Inputs
st.sidebar.header("📋 Your Preferences")

student_id = st.sidebar.text_input("Student ID", "S01290")
num_recs = st.sidebar.slider("Number of Recommendations", 5, 20, 10)

domains = st.sidebar.multiselect(
    "Preferred Domains",
    ["AI", "Data Science", "Cybersecurity", "Finance", "Healthcare", 
     "Engineering", "Law", "Agriculture"],
    default=["AI", "Data Science"]
)

difficulty_range = st.sidebar.slider(
    "Difficulty Range",
    0.0, 1.0, (0.3, 0.7),
    help="Select your comfort zone"
)

# Generate Button
if st.sidebar.button("🔍 Get Recommendations", type="primary"):
    with st.spinner("Generating personalized recommendations..."):
        # Call recommendation system
        recs = recommend(student_id, top_n=num_recs)
        
        # Filter by preferences
        if domains:
            recs = recs[recs['course_domain'].isin(domains)]
        
        recs = recs[
            (recs['course_difficulty'] >= difficulty_range[0]) & 
            (recs['course_difficulty'] <= difficulty_range[1])
        ]
        
        # Store in session state
        st.session_state['recommendations'] = recs
        st.session_state['student_id'] = student_id

# Display Results
if 'recommendations' in st.session_state:
    recs = st.session_state['recommendations']
    
    # Student Profile Card
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("GPA", "3.2 / 4.0", delta="0.3")
    with col2:
        st.metric("Attendance", "85%", delta="5%")
    with col3:
        st.metric("Risk Level", "Low", delta="-10%")
    with col4:
        st.metric("Courses Taken", "24")
    
    st.divider()
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        # Score breakdown pie chart
        fig1 = px.pie(
            names=['CF (40%)', 'CBF (35%)', 'Success (20%)', 'Job (5%)'],
            values=[0.4, 0.35, 0.2, 0.05],
            title="Recommendation Algorithm Breakdown"
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Domain distribution
        domain_counts = recs['course_domain'].value_counts()
        fig2 = px.bar(x=domain_counts.index, y=domain_counts.values,
                     title="Recommendations by Domain")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # Recommendation Cards
    st.header("📚 Your Personalized Recommendations")
    
    for idx, rec in recs.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(f"{idx + 1}. {rec['course_name']}")
                st.markdown(f"**Domain:** {rec['course_domain']} | **ID:** {rec['course_id']}")
                
                # Metrics
                mcol1, mcol2, mcol3 = st.columns(3)
                mcol1.metric("Success Rate", f"{rec['p_success']*100:.1f}%")
                mcol2.metric("Job Demand", f"{rec['job_market']*100:.1f}%")
                mcol3.metric("Difficulty", f"{rec['course_difficulty']*100:.0f}%")
                
                # Gemini Explanation
                st.info(f"💬 **AI Advisor Says:** {rec['explanation']}")
            
            with col2:
                st.markdown(f"### ⭐ {rec['final_score']:.3f}")
                st.progress(rec['final_score'])
                
                if st.button("View Details", key=f"view_{idx}"):
                    st.success("Opening course details...")
                
                if st.button("Add to Wishlist", key=f"wish_{idx}"):
                    st.success("Added to wishlist!")
            
            st.divider()
    
    # Export
    csv = recs.to_csv(index=False)
    st.download_button(
        "📄 Download Report (CSV)",
        csv,
        f"recommendations_{st.session_state['student_id']}.csv",
        "text/csv"
    )

else:
    st.info("👈 Enter your Student ID and click 'Get Recommendations' to start!")
```

**Run with:**
```bash
pip install streamlit plotly
streamlit run streamlit_app.py
```

---

## 📱 Part 4: MOBILE APP INPUTS/OUTPUTS

### **Mobile UI Considerations**

**Inputs (Mobile-Optimized):**
- Large touch-friendly buttons
- Swipe gestures for filters
- Voice input for Student ID
- Biometric login (fingerprint/face)

**Outputs (Mobile-Optimized):**
- Card-based swipe interface (Tinder-style)
- Swipe Right → Add to wishlist
- Swipe Left → Not interested
- Tap → View details
- Simplified metrics (top 3 only)
- Shorter explanations (1 sentence)

---

## 🎯 Part 5: RECOMMENDED WORKFLOW

### **User Journey Map:**

```
1. Login → 2. Dashboard → 3. Get Recommendations → 4. Review Cards
                ↓                                        ↓
5. Filter/Refine ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ┘
                ↓
6. Compare Courses → 7. Add to Wishlist → 8. Consult Advisor
                                                 ↓
                                         9. Enroll in Course
```

### **What Data to Store:**

**Input History:**
- Search queries
- Filter preferences
- Number of times student requested recs

**Output Tracking:**
- Which recommendations clicked
- Which added to wishlist
- Which enrolled in
- Success rate of predictions (feedback loop)

---

## 🚀 Quick Start: Choose Your Stack

### **Fast & Simple:** Streamlit
- **Time:** 1-2 hours to build
- **Best for:** Academic demo, quick prototype
- **Users:** Small (< 1000 students)

### **Professional:** Flask + React
- **Time:** 1-2 weeks to build
- **Best for:** Production deployment
- **Users:** Medium (1,000-10,000 students)

### **Enterprise:** Django + Mobile App
- **Time:** 1-2 months to build
- **Best for:** University-wide deployment
- **Users:** Large (10,000+ students)

---

## 📊 Summary Table

| Input | Type | Required? | Purpose |
|-------|------|-----------|---------|
| Student ID | Text | ✅ Yes | Authentication |
| # of Recs | Number | ✅ Yes | Control output size |
| Domain Filter | Multi-select | ❌ Optional | Focus interests |
| Difficulty | Range | ❌ Optional | Match ability |
| Job Priority | Dropdown | ❌ Optional | Adjust weights |

| Output | Format | Essential? | Purpose |
|--------|--------|------------|---------|
| Course List | Cards | ✅ Yes | Main recommendations |
| Gemini Explanation | Text | ✅ Yes | Build trust/understanding |
| Score Breakdown | Metrics | ✅ Yes | Transparency |
| Visualizations | Charts | ❌ Optional | Engagement |
| Comparison | Table | ❌ Optional | Decision support |

---

**Next Step:** Choose Option C (Streamlit) for fastest implementation! Want me to create the full Streamlit app now?
