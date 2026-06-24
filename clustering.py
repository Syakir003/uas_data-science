# clustering.py
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

FEATURE_GROUPS = {
    'kemiskinan': ['Miskin_2023', 'Miskin_2024', 'Miskin_2025'],
    'ipm': ['IPM_2023', 'IPM_2024', 'IPM_2025'],
    'keduanya': ['Miskin_2023', 'Miskin_2024', 'Miskin_2025',
                 'IPM_2023', 'IPM_2024', 'IPM_2025'],
}

CLUSTER_COLORS = ['#4361ee', '#f72585', '#4cc9f0', '#f9c74f', '#90be6d', '#577590']

SCATTER_AXES = {
    'kemiskinan': ('Miskin_2023', 'Kemiskinan 2023 (%)', 'Miskin_2025', 'Kemiskinan 2025 (%)'),
    'ipm': ('IPM_2023', 'IPM 2023', 'IPM_2025', 'IPM 2025'),
    'keduanya': ('IPM_2025', 'IPM 2025', 'Miskin_2025', 'Kemiskinan 2025 (%)'),
}

_HTML_KW = dict(full_html=False, include_plotlyjs=False)


def prepare_features(data, feature_group):
    features = FEATURE_GROUPS[feature_group]
    clean = data.dropna(subset=features).reset_index(drop=True)
    return clean, features


def run_clustering(clean, features, k):
    X_scaled = StandardScaler().fit_transform(clean[features].values)
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = model.fit_predict(X_scaled)
    result = clean.copy()
    result['Cluster'] = labels.astype(int)
    sil = float(silhouette_score(X_scaled, labels))
    return result, sil


def compute_elbow(clean, features, k_range=range(2, 7)):
    X_scaled = StandardScaler().fit_transform(clean[features].values)
    ks, inertias, sils = [], [], []
    for k in k_range:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = model.fit_predict(X_scaled)
        ks.append(k)
        inertias.append(float(model.inertia_))
        sils.append(float(silhouette_score(X_scaled, labels)))
    return ks, inertias, sils


def make_elbow_chart(ks, inertias):
    fig = go.Figure(go.Scatter(x=list(ks), y=inertias, mode='lines+markers',
                               line=dict(color='#4361ee', width=3),
                               marker=dict(size=10)))
    fig.update_layout(template='plotly_white', title='Metode Elbow',
                      xaxis_title='Jumlah Cluster (k)', yaxis_title='Inertia',
                      margin=dict(l=40, r=20, t=50, b=40))
    return fig.to_html(**_HTML_KW)


def make_scatter_chart(result, feature_group):
    xcol, xlab, ycol, ylab = SCATTER_AXES[feature_group]
    fig = px.scatter(result, x=xcol, y=ycol, color=result['Cluster'].astype(str),
                     hover_name='Provinsi',
                     color_discrete_sequence=CLUSTER_COLORS,
                     labels={'color': 'Cluster', xcol: xlab, ycol: ylab})
    fig.update_traces(marker=dict(size=12, line=dict(width=1, color='white')))
    fig.update_layout(template='plotly_white', title='Sebaran Provinsi per Cluster',
                      xaxis_title=xlab, yaxis_title=ylab,
                      margin=dict(l=40, r=20, t=50, b=40))
    return fig.to_html(**_HTML_KW)


def make_boxplot(result, column, title):
    fig = px.box(result, x=result['Cluster'].astype(str), y=column,
                 color=result['Cluster'].astype(str),
                 color_discrete_sequence=CLUSTER_COLORS)
    fig.update_layout(template='plotly_white', title=title,
                      xaxis_title='Cluster', yaxis_title=column,
                      showlegend=False, margin=dict(l=40, r=20, t=50, b=40))
    return fig.to_html(**_HTML_KW)


def cluster_profile(result, features):
    grouped = result.groupby('Cluster')[features].mean().round(2).reset_index()
    return grouped.to_dict('records')


def provinces_by_cluster(result):
    mapping = {}
    for cluster_id, group in result.groupby('Cluster'):
        mapping[int(cluster_id)] = sorted(group['Provinsi'].tolist())
    return mapping
