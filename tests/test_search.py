import pytest
import json
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "Star Wars API"

def test_search_with_valid_params(client):
    response = client.get("/api/starwars/search?type=people&name=luke")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "data" in data
    assert "pagination" in data
    assert isinstance(data["data"], list)

def test_search_without_type(client):
    response = client.get("/api/starwars/search")
    assert response.status_code == 400
    
    data = response.get_json()
    assert "error" in data
    assert "type" in data["error"].lower()

def test_search_with_invalid_resource(client):
    response = client.get("/api/starwars/search?type=invalid")
    assert response.status_code == 400
    
    data = response.get_json()
    assert "error" in data
    assert "validation" in data["error"].lower() or "invalid" in data["error"].lower()

def test_search_with_filters(client):
    response = client.get("/api/starwars/search?type=people&filter_field=gender&filter_value=male")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "filters_applied" in data
    assert data["filters_applied"]["field_filter"] == "gender=male"

def test_search_with_sorting(client):
    response = client.get("/api/starwars/search?type=people&sort=name&order=desc")
    assert response.status_code == 200
    
    data = response.get_json()
    if len(data["data"]) > 1:
        names = [item["name"] for item in data["data"]]
        assert names == sorted(names, reverse=True)

def test_search_pagination(client):
    """Testa paginação"""
    response = client.get("/api/starwars/search?type=people&page=1&per_page=5")
    assert response.status_code == 200
    
    data = response.get_json()
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 5
    assert len(data["data"]) <= 5

def test_search_invalid_pagination(client):
    """Testa paginação inválida"""
    response = client.get("/api/starwars/search?type=people&page=0&per_page=5")
    assert response.status_code == 400

def test_film_characters_valid_id(client):
    """Testa endpoint de personagens por filme com ID válido"""
    response = client.get("/api/starwars/films/1/characters")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "characters" in data
    assert "film_id" in data
    assert data["film_id"] == 1
    assert isinstance(data["characters"], list)

def test_film_characters_invalid_id(client):
    """Testa endpoint de personagens por filme com ID inválido"""
    response = client.get("/api/starwars/films/999/characters")
    assert response.status_code == 404
    
    data = response.get_json()
    assert "error" in data
    assert "not found" in data["error"].lower()

def test_list_resources(client):
    """Testa endpoint que lista recursos disponíveis"""
    response = client.get("/api/starwars/resources")
    assert response.status_code == 200
    
    data = response.get_json()
    assert "resources" in data
    assert "count" in data
    assert isinstance(data["resources"], list)
    assert len(data["resources"]) == 6 
 