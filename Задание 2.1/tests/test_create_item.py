import pytest
import requests

@pytest.mark.positive
def test_create_item_returns_success_status(base_url, seller_id, random_item_name):
    payload = {
        "sellerId": seller_id,
        "name": random_item_name,
        "price": 500,
        "statistics": {"likes": 100, "viewCount": 100, "contacts": 100}
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 200

@pytest.mark.xfail(reason="Баг: API возвращает строку вместо JSON объекта")
def test_create_item_returns_proper_structure(base_url, seller_id, random_item_name):
    payload = {
        "sellerId": seller_id,
        "name": random_item_name,
        "price": 500,
        "statistics": {"likes": 100, "viewCount": 100, "contacts": 100}
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "sellerId" in data
    assert data["sellerId"] == seller_id
    assert data["name"] == random_item_name
    assert "createdAt" in data

@pytest.mark.negative
@pytest.mark.parametrize("payload", [
    {"name": "test", "price": 500},
    {"sellerId": 123, "price": 500},
    {"sellerId": 123, "name": "test"},
])
def test_create_item_missing_fields(base_url, payload):
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400

@pytest.mark.negative
def test_create_item_invalid_data(base_url):
    payload = {
        "sellerId": "invalid_id",
        "name": "test",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 150, "contacts": 10}
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400