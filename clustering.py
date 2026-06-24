# clustering.py
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

FEATURE_GROUPS = {
    'kemiskinan': ['Miskin_2023', 'Miskin_2024', 'Miskin_2025'],
    'ipm': ['IPM_2023', 'IPM_2024', 'IPM_2025'],
    'keduanya': ['Miskin_2023', 'Miskin_2024', 'Miskin_2025',
                 'IPM_2023', 'IPM_2024', 'IPM_2025'],
}


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
