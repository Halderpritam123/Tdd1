import pytest
import os
import sys
import json

# Add the project's root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, weather_data

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    with app.test_client() as client:
        yield client

def test_get_weather_existing_city(client):
    response = client.get('/weather/San Francisco')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data == weather_data['San Francisco']

def test_get_weather_non_existing_city(client):
    response = client.get('/weather/Chicago')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data == {}

def test_add_weather(client):
    new_weather_data = {'city': 'London', 'temperature': 18, 'weather': 'Rainy'}
    response = client.post('/weather', json=new_weather_data)

    assert response.status_code == 201
    assert 'Weather data added successfully.' in str(response.data)

def test_add_weather_invalid_data(client):
    invalid_weather_data = {'city': 'Paris', 'temperature': 0}
    response = client.post('/weather', json=invalid_weather_data)

    assert response.status_code == 400
    assert 'City, temperature, and weather fields are required.' in str(response.data)

def test_update_weather_existing_city(client):
    updated_weather_data = {'temperature': 25, 'weather': 'Sunny'}
    response = client.put('/weather/San Francisco', json=updated_weather_data)

    assert response.status_code == 200
    assert 'Weather data updated successfully.' in str(response.data)

def test_update_weather_non_existing_city(client):
    updated_weather_data = {'temperature': 25}
    response = client.put('/weather/New York', json=updated_weather_data)

    assert response.status_code == 404
    assert 'City "New York" not found.' in str(response.data)

def test_delete_weather_existing_city(client):
    response = client.delete('/weather/San Francisco')

    assert response.status_code == 200
    assert 'Weather data deleted successfully.' in str(response.data)



def test_delete_weather_non_existing_city(client):
    response = client.delete('/weather/Chicago')

    assert response.status_code == 404
    assert 'City "Chicago" not found.' in str(response.data)


