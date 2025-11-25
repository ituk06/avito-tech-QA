import pytest
import requests


@pytest.mark.positive
def test_get_user_items(base_url, seller_id, create_test_item):
    """Проверяет получение списка элементов пользователя.

    Шаги теста:
    1. Создается тестовый элемент для пользователя.
    2. Выполняется GET-запрос к /api/1/{seller_id}/item.
    3. Проверяется, что код ответа 200.
    4. Проверяется, что все элементы в ответе принадлежат указанному seller_id.
    """
    create_test_item["id"]
    response = requests.get(f"{base_url}/api/1/{seller_id}/item")
    assert response.status_code == 200
    data = response.json()
    assert all(item["sellerId"] == seller_id for item in data)


@pytest.mark.positive
def test_get_user_no_items(base_url, seller_id_no_items):
    """Проверяет получение пустого списка элементов для пользователя без товаров.

    Шаги теста:
    1. Выполняется GET-запрос к /api/1/{seller_id_no_items}/item.
    2. Проверяется, что код ответа 200.
    3. Проверяется, что возвращается пустой список.
    """
    response = requests.get(f"{base_url}/api/1/{seller_id_no_items}/item")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.negative
def test_get_user_invalid_id(base_url):
    """Проверяет поведение API при передаче некорректного ID пользователя.

    Шаги теста:
    1. Выполняется GET-запрос к /api/1/invalid_id/item.
    2. Проверяется, что код ответа 400.
    """
    response = requests.get(f"{base_url}/api/1/invalid_id/item")
    assert response.status_code == 400
