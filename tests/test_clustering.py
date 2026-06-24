# tests/test_clustering.py
import data_loader
import clustering


def test_feature_groups_keys():
    assert set(clustering.FEATURE_GROUPS) == {'kemiskinan', 'ipm', 'keduanya'}


def test_prepare_features_ipm_keeps_all_provinces():
    data = data_loader.load_data()
    clean, features = clustering.prepare_features(data, 'ipm')
    assert features == ['IPM_2023', 'IPM_2024', 'IPM_2025']
    assert len(clean) == 38  # IPM lengkap untuk semua provinsi


def test_prepare_features_kemiskinan_drops_papua_baru():
    data = data_loader.load_data()
    clean, features = clustering.prepare_features(data, 'kemiskinan')
    assert len(clean) == 34  # 4 provinsi Papua baru ter-drop


def test_run_clustering_adds_cluster_column():
    data = data_loader.load_data()
    clean, features = clustering.prepare_features(data, 'keduanya')
    result, sil = clustering.run_clustering(clean, features, k=3)
    assert 'Cluster' in result.columns
    assert set(result['Cluster'].unique()) == {0, 1, 2}
    assert -1.0 <= sil <= 1.0


def test_compute_elbow_lengths():
    data = data_loader.load_data()
    clean, features = clustering.prepare_features(data, 'keduanya')
    ks, inertias, sils = clustering.compute_elbow(clean, features)
    assert list(ks) == [2, 3, 4, 5, 6]
    assert len(inertias) == 5 and len(sils) == 5
