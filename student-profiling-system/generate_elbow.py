import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import os

# 1. Load the data
print("Loading cleaned_data.csv...")
df = pd.read_csv("C:\\Users\\anman\\Desktop\\final project\\Student-Success-System\\student-profiling-system\\data\\interim\\cleaned_data.csv")

# 2. Automatically select all numeric behavioral features
features = df.select_dtypes(include=[np.number]).columns.tolist()
X = df[features].fillna(df[features].median())

# 3. Scale the data (Crucial for K-Means)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 4. Calculate WCSS (Within-Cluster Sum of Squares) for k=1 through k=10
wcss = []
K_RANGE = range(1, 11)

print("Calculating Mathematical Distances (Inertia)...")
for k in K_RANGE:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

# 5. Create a beautiful, professional Plotly Graph
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(K_RANGE), 
    y=wcss, 
    mode='lines+markers',
    name='WCSS',
    line=dict(color='#3B82F6', width=3),
    marker=dict(size=10, color='#10B981')
))

# Highlight the "Elbow" at k=3
fig.add_vline(x=3, line_dash="dash", line_color="#EF4444", annotation_text="Optimal k=3 (The Elbow)")

fig.update_layout(
    title="Mathematical Proof of Clusters: The Elbow Method",
    xaxis_title="Number of Clusters (k)",
    yaxis_title="Within-Cluster Sum of Squares (WCSS / Inertia)",
    template="plotly_dark",
    font=dict(size=14)
)

# 6. Save the graph as an interactive HTML file
output_file = "elbow_proof.html"
fig.write_html(output_file)
print(f"✅ Success! Open '{output_file}' in your web browser to see the proof.")