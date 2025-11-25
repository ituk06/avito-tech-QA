import pytest
import random
import requests
import re

BASE_URL = "https://qa-internship.avito.com"

@pytest.fixture(scope="session")
def unique_seller_id():
    return random.randint(111111, 999999)

def extract_id(status_text):
    match = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", status_text)
    return match.group() if match else None


@pytest.fixture(scope="session")
def base_url():
    return "https://qa-internship.avito.com"




@pytest.fixture
def item_data(unique_seller_id):
    return {
        "sellerID": unique_seller_id,
        "name": "Test item",
        "price": 100,
        "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
    }


@pytest.fixture
def created_item_id(base_url, item_data):
    url = f"{base_url}/api/1/item"
    response = requests.post(url, json=item_data)
    assert response.status_code == 200
    status_text = response.json()["status"]
    item_id = extract_id(status_text)
    assert item_id is not None, "ID не найден в ответе"
    yield item_id
    delete_resp = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert delete_resp.status_code in [200, 404], f"Не удалось удалить элемент {item_id}"

