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
