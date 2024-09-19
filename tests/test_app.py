import pytest
import json
from app import app, get_food_trucks, search_by_applicant, search_by_street, search_by_location
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Mock response data for testing
MOCK_TRUCKS = [
    {
        'applicant': 'Test Truck A',
        'address': '123 Main St',
        'status': 'APPROVED',
        'latitude': '37.7749',
        'longitude': '-122.4194'
    },
    {
        'applicant': 'Test Truck B',
        'address': '456 Elm St',
        'status': 'APPROVED',
        'latitude': '37.7896',
        'longitude': '-123.4567'
    },
    {
        'applicant': 'Test Truck CC',
        'address': '789 San St',
        'status': 'SUSPENDED',
        'latitude': '40.0000',
        'longitude': '-125.1674'
    }
]

@patch('app.get_food_trucks', return_value=MOCK_TRUCKS)
def test_get_all_trucks(mock_get_food_trucks, client):
    """Test /get_all_trucks endpoint"""
    response = client.get('/get_all_trucks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 3

@patch('app.get_food_trucks', return_value=MOCK_TRUCKS)
def test_search_by_applicant(mock_get_food_trucks, client):
    """Test /search/applicant endpoint"""
    response = client.get('/search/applicant?name=Test Truck A')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['applicant'] == 'Test Truck A'

@patch('app.get_food_trucks', return_value=MOCK_TRUCKS)
def test_search_by_street(mock_get_food_trucks, client):
    """Test /search/street endpoint"""
    response = client.get('/search/street?address=Main')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['address'] == '123 Main St'

@patch('app.get_food_trucks', return_value=MOCK_TRUCKS)
def test_search_by_location(mock_get_food_trucks, client):
    """Test /search/location endpoint"""
    # Assuming we search near Test Truck A's location
    response = client.get('/search/location?latitude=37.7749&longitude=-122.4194')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]['applicant'] == 'Test Truck A'
    assert data[1]['applicant'] == 'Test Truck B'
