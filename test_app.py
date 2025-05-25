import pytest
import json
from app import app, url_store, url_to_code

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
    # Cleanup after each test
    url_store.clear()
    url_to_code.clear()

def test_shorten_url(client):
    # Test creating a new shortened URL
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')

    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'short_code' in data
    assert 'short_url' in data
    assert len(data['short_code']) >= 6

def test_shorten_existing_url(client):
    # Test creating with an already existing URL
    url = 'https://www.example.com'

    # First creation
    response1 = client.post('/shortener/shorten',
        json={'url': url},
        content_type='application/json')
    data1 = json.loads(response1.data)

    # Second creation with same URL
    response2 = client.post('/shortener/shorten',
        json={'url': url},
        content_type='application/json')
    data2 = json.loads(response2.data)

    assert response2.status_code == 200
    assert data1['short_code'] == data2['short_code']

def test_redirect(client):
    # First create a shortened URL
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')
    data = json.loads(response.data)
    short_code = data['short_code']

    # Test redirection
    response = client.get(f'/{short_code}')
    assert response.status_code == 302
    assert response.headers['Location'] == 'https://www.example.com'

def test_stats(client):
    # Create a shortened URL
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')
    data = json.loads(response.data)
    short_code = data['short_code']

    # Make some visits
    client.get(f'/{short_code}')
    client.get(f'/{short_code}')

    # Check statistics
    response = client.get(f'/shortener/stats/{short_code}')
    assert response.status_code == 200
    stats = json.loads(response.data)
    assert stats['url'] == 'https://www.example.com'
    assert stats['visits'] == 2

def test_invalid_short_code(client):
    # Test redirection with invalid code
    response = client.get('/invalid_code')
    assert response.status_code == 404

    # Test stats with invalid code
    response = client.get('/shortener/stats/invalid_code')
    assert response.status_code == 404

def test_short_code_format(client):
    # Verify format of generated short code
    response = client.post('/shortener/shorten',
        json={'url': 'https://www.example.com'},
        content_type='application/json')
    data = json.loads(response.data)
    short_code = data['short_code']

    assert len(short_code) >= 6
    assert short_code.isalnum()  # Verify code is alphanumeric