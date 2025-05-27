import pytest
from api.routes import url_service
from app import app

@pytest.fixture(autouse=True)
def reset_state():
    url_service.reset()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_shorten_url(client):
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')

    assert response.status_code == 201
    data = response.get_json()
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) >= 6

def test_shorten_existing_url(client):
    url = 'https://www.example.com'

    response1 = client.post('/shortener/shorten',
        json={'url': url},
        content_type='application/json')
    data1 = response1.get_json()

    response2 = client.post('/shortener/shorten',
        json={'url': url},
        content_type='application/json')
    data2 = response2.get_json()

    assert response2.status_code == 200
    assert data1['short_code'] == data2['short_code']

def test_redirect(client):
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')
    short_code = response.get_json()['short_code']

    response = client.get(f'/shortener/{short_code}')
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://www.example.com'

def test_stats(client):
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')
    short_code = response.get_json()['short_code']

    client.get(f'/shortener/{short_code}')
    client.get(f'/shortener/{short_code}')

    response = client.get(f'/shortener/stats/{short_code}')
    assert response.status_code == 200
    stats = response.get_json()
    assert stats['url'] == 'https://www.example.com'
    assert stats['visits'] == 2

def test_invalid_short_code(client):
    response = client.get('/shortener/invalid_code')
    assert response.status_code == 404
    assert response.get_json()['message'] == "Short code not found"

    response = client.get('/shortener/stats/invalid_code')
    assert response.status_code == 404
    assert response.get_json()['message'] == "Short code not found"

def test_short_code_format(client):
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')
    short_code = response.get_json()['short_code']
    assert len(short_code) >= 6
    assert short_code.isalnum()

def test_shorten_invalid_url(client):
    response = client.post('/shortener/shorten',
        json={'url': 'not_a_url'},
        content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    print(data)
    assert data['message'] == "URL invalid"