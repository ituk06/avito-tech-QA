import pytest
import requests


@pytest.mark.positive
def test_get_existing_item(base_url, create_test_item):
    """Проверяет получение существующего элемента по его ID.

    Шаги теста:
    1. Получается ID тестового элемента.
    2. Выполняется GET-запрос к /api/1/item/{item_id}.
    3. Проверяется, что код ответа 200.
    """
    item_id = create_test_item["id"]
    response = requests.get(f"{base_url}/api/1/item/{item_id}")
    print(item_id)
    assert response.status_code == 200


@pytest.mark.xfail(reason="Баг: API возвращает массив вместо одного объекта")
def test_get_item_returns_single_object_not_array(base_url, create_test_item):
    """Проверяет, что API возвращает один объект элемента, а не массив.

    Шаги теста:
    1. Получается ID тестового элемента.
    2. Выполняется GET-запрос к /api/1/item/{item_id}.
    3. Проверяется, что код ответа 200.
    4. Проверяется, что возвращаемый объект имеет правильный ID.
    """
    item_id = create_test_item["id"]
    response = requests.get(f"{base_url}/api/1/item/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id


@pytest.mark.negative
def test_get_nonexistent_item(base_url, random_uuid):
    """Проверяет получение несуществующего элемента.

    Шаги теста:
    1. Выполняется GET-запрос к /api/1/item/{random_uuid}.
    2. Проверяется, что код ответа 404.
    """
    response = requests.get(f"{base_url}/api/1/item/{random_uuid}")
    assert response.status_code == 404


@pytest.mark.negative
def test_get_item_invalid_id(base_url):
    """Проверяет поведение API при передаче некорректного ID элемента.

    Шаги теста:
    1. Выполняется GET-запрос к /api/1/item/invalid_id.
    2. Проверяется, что код ответа 400.
    """
    response = requests.get(f"{base_url}/api/1/item/invalid_id")
    assert response.status_code == 400
