import pytest
import requests

@pytest.mark.positive
def test_delete_existing_item(base_url, create_test_item_for_delete):
    item_id = create_test_item_for_delete["id"]
    response = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert response.status_code == 200

@pytest.mark.negative
def test_delete_nonexistent_item(base_url, random_uuid):
    response = requests.delete(f"{base_url}/api/2/item/{random_uuid}")
    assert response.status_code == 404

@pytest.mark.negative
def test_delete_invalid_id(base_url):
    response = requests.delete(f"{base_url}/api/2/item/invalid_id")
    assert response.status_code == 400