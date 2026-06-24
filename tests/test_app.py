# tests/test_app.py
import app as flask_app


def make_client():
    flask_app.app.config['TESTING'] = True
    return flask_app.app.test_client()


def test_index_returns_200_and_form():
    client = make_client()
    resp = client.get('/')
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'KlasterID' in body
    assert 'Jalankan' in body  # tombol submit


def test_result_post_renders_dashboard():
    client = make_client()
    resp = client.post('/result', data={'k': '3', 'features': 'keduanya'})
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert 'Silhouette' in body
    assert 'Profil Cluster' in body
    assert 'plotly' in body.lower()  # chart ter-embed


def test_result_box_features_only_skips_ipm_box():
    client = make_client()
    resp = client.post('/result', data={'k': '3', 'features': 'kemiskinan'})
    assert resp.status_code == 200


def test_result_handles_invalid_k():
    client = make_client()
    resp = client.post('/result', data={'k': 'abc', 'features': 'keduanya'})
    assert resp.status_code == 200


def test_result_handles_unknown_feature_group():
    client = make_client()
    resp = client.post('/result', data={'k': '3', 'features': 'banana'})
    assert resp.status_code == 200


def test_result_handles_k_too_small():
    client = make_client()
    resp = client.post('/result', data={'k': '1', 'features': 'ipm'})
    assert resp.status_code == 200


def test_result_handles_k_too_large():
    client = make_client()
    resp = client.post('/result', data={'k': '999', 'features': 'kemiskinan'})
    assert resp.status_code == 200
