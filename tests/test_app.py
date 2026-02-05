import json


def test_health_live(client):
    """Test liveness endpoint."""
    response = client.get('/health/live')
    assert response.status_code == 200
    assert response.json['status'] == 'alive'


def test_health_ready(client):
    """Test readiness endpoint."""
    response = client.get('/health/ready')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'


def test_shorten_url_success(client):
    """Test creating a short URL."""
    response = client.post('/shorten',
                           data=json.dumps({'url': 'https://www.example.com'}),
                           content_type='application/json'
                           )
    assert response.status_code == 201
    data = response.json
    assert 'short_code' in data
    assert data['original_url'] == 'https://www.example.com'
    assert len(data['short_code']) == 6


def test_shorten_url_missing_url(client):
    """Test error when URL is missing."""
    response = client.post('/shorten',
                           data=json.dumps({}),
                           content_type='application/json'
                           )
    assert response.status_code == 400
    assert 'error' in response.json


def test_shorten_url_invalid_format(client):
    """Test error when URL format is invalid."""
    response = client.post('/shorten',
                           data=json.dumps({'url': 'not-a-valid-url'}),
                           content_type='application/json'
                           )
    assert response.status_code == 400


def test_redirect_success(client):
    """Test redirect to original URL."""
    # First create a short URL
    create_response = client.post('/shorten',
                                  data=json.dumps(
                                      {'url': 'https://www.example.com'}),
                                  content_type='application/json'
                                  )
    short_code = create_response.json['short_code']

    # Then try to access it
    redirect_response = client.get(f'/{short_code}')
    assert redirect_response.status_code == 302
    assert redirect_response.location == 'https://www.example.com'


def test_redirect_not_found(client):
    """Test 404 for non-existent short code."""
    response = client.get('/nonexistent')
    assert response.status_code == 404


def test_stats_endpoint(client):
    """Test getting stats for a URL."""
    # Create a short URL
    create_response = client.post('/shorten',
                                  data=json.dumps(
                                      {'url': 'https://www.example.com'}),
                                  content_type='application/json'
                                  )
    short_code = create_response.json['short_code']

    # Access it once
    client.get(f'/{short_code}')

    # Check stats
    stats_response = client.get(f'/stats/{short_code}')
    assert stats_response.status_code == 200
    assert stats_response.json['clicks'] == 1


def test_list_urls(client):
    """Test listing all URLs."""
    # Create some URLs
    client.post('/shorten',
                data=json.dumps({'url': 'https://www.example1.com'}),
                content_type='application/json'
                )
    client.post('/shorten',
                data=json.dumps({'url': 'https://www.example2.com'}),
                content_type='application/json'
                )

    # List all
    response = client.get('/urls')
    assert response.status_code == 200
    assert len(response.json) == 2
