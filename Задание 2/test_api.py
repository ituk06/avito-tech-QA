from conftest import extract_id
import requests
import re
import pytest


class TestApi:

    def test_create_item_returns_200(self, base_url, item_data):
        response = requests.post(f"{base_url}/api/1/item", json=item_data)
        assert response.status_code == 200

    def test_create_item_returns_valid_id(self, base_url, item_data):
        response = requests.post(f"{base_url}/api/1/item", json=item_data)
        assert response.status_code == 200
        status_text = response.json()["status"]
        item_id = extract_id(status_text)
        assert item_id is not None

    def test_created_item_can_be_fetched_by_id(self, base_url, created_item_id):
        response = requests.get(f"{base_url}/api/1/item/{created_item_id}")
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 1
        item = items[0]
        assert item["id"] == created_item_id

    def test_new_item_appears_in_seller_list(self, base_url, unique_seller_id, created_item_id):
        response = requests.get(f"{base_url}/api/1/{unique_seller_id}/item")
        assert response.status_code == 200
        items = response.json()
        ids = [item["id"] for item in items]
        assert created_item_id in ids

    def test_statistics_are_retrievable(self, base_url, created_item_id):
        response = requests.get(f"{base_url}/api/1/statistic/{created_item_id}")
        assert response.status_code == 200
        stats = response.json()[0]
        assert stats["likes"] > 0
        assert stats["viewCount"] > 0
        assert stats["contacts"] > 0

    def test_statistics_v1_and_v2_are_identical(self, base_url, created_item_id):
        v1 = requests.get(f"{base_url}/api/1/statistic/{created_item_id}").json()[0]
        v2 = requests.get(f"{base_url}/api/2/statistic/{created_item_id}").json()[0]
        assert v1["likes"] == v2["likes"]
        assert v1["contacts"] == v2["contacts"]

    def test_delete_item_works(self, base_url, created_item_id):
        response = requests.delete(f"{base_url}/api/2/item/{created_item_id}")
        assert response.status_code == 200

        response = requests.get(f"{base_url}/api/1/item/{created_item_id}")
        assert response.status_code == 404

    def test_get_unknown_item_returns_404(self, base_url):
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{base_url}/api/1/item/{fake_id}")
        assert response.status_code == 404

    def test_create_with_text_sellerid_fails(self, base_url):
        data = {
            "sellerID": "abc",
            "name": "Bad sellerID",
            "price": 100,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400

    def test_create_without_price_fails(self, base_url, unique_seller_id):
        data = {
            "sellerID": unique_seller_id,
            "name": "No price",
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400

    def test_negative_price_is_accepted_and_saved(self, base_url, unique_seller_id):
        data = {
            "sellerID": unique_seller_id,
            "name": "Negative price",
            "price": -50,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 200
        item_id = extract_id(response.json()["status"])
        assert item_id is not None
        item = requests.get(f"{base_url}/api/1/item/{item_id}").json()[0]
        assert item["price"] == -50


        delete_resp = requests.delete(f"{base_url}/api/2/item/{item_id}")
        assert delete_resp.status_code in [200, 404]

    def test_zero_likes_not_allowed(self, base_url, unique_seller_id):
        data = {
            "sellerID": unique_seller_id,
            "name": "Zero likes",
            "price": 100,
            "statistics": {"likes": 0, "viewCount": 1, "contacts": 1}
        }
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 400

    def test_long_name_is_accepted_and_saved(self, base_url, unique_seller_id):
        long_name = "A" * 600
        data = {
            "sellerID": unique_seller_id,
            "name": long_name,
            "price": 100,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }
        response = requests.post(f"{base_url}/api/1/item", json=data)
        assert response.status_code == 200
        item_id = extract_id(response.json()["status"])
        assert item_id is not None
        item = requests.get(f"{base_url}/api/1/item/{item_id}").json()[0]
        assert item["name"] == long_name

        delete_resp = requests.delete(f"{base_url}/api/2/item/{item_id}")
        assert delete_resp.status_code in [200, 404]

    def test_can_create_two_identical_items(self, base_url, unique_seller_id):
        data = {
            "sellerID": unique_seller_id,
            "name": "Same item",
            "price": 99,
            "statistics": {"likes": 1, "viewCount": 1, "contacts": 1}
        }

        resp1 = requests.post(f"{base_url}/api/1/item", json=data)
        resp2 = requests.post(f"{base_url}/api/1/item", json=data)
        assert resp1.status_code == 200
        assert resp2.status_code == 200


        items = requests.get(f"{base_url}/api/1/{unique_seller_id}/item").json()
        duplicates = [item for item in items if item["name"] == "Same item"]
        assert len(duplicates) >= 2


        for item in duplicates:
            delete_resp = requests.delete(f"{base_url}/api/2/item/{item['id']}")
            assert delete_resp.status_code in [200, 404]

    def test_new_seller_returns_empty_list(self, base_url):
        new_seller_id = 99999999999
        response = requests.get(f"{base_url}/api/1/{new_seller_id}/item")
        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        assert len(items) == 0

    def test_invalid_json_returns_400(self, base_url):
        broken_json = '{"sellerID": 123, "name": Broken, "price": 100}'
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{base_url}/api/1/item",
            data=broken_json,
            headers=headers
        )
        assert response.status_code == 400
