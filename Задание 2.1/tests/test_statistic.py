import pytest
import requests


@pytest.mark.xfail(reason="Баг: некорректное тело ответа")
def test_get_item_statistic(base_url, create_test_item_for_delete):
    """Проверяет получение статистики конкретного элемента по его ID.

    Шаги теста:
    1. Создается тестовый элемент для удаления.
    2. Выполняется GET-запрос к /api/2/statistic/{item_id}.
    3. Проверяется, что код ответа 200.
    4. Проверяется, что в ответе присутствуют ключи: 'likes', 'viewCount', 'contacts'.
    """
    item_id = create_test_item_for_delete["id"]
    response = requests.get(f"{base_url}/api/2/statistic/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert all(k in data for k in {"likes", "viewCount", "contacts"})


@pytest.mark.negative
def test_get_statistic_nonexistent_item(base_url, random_uuid):
    """Проверяет получение статистики для несуществующего элемента.

    Шаги теста:
    1. Выполняется GET-запрос к /api/2/statistic/{random_uuid}.
    2. Проверяется, что код ответа 404.
    """
    response = requests.get(f"{base_url}/api/2/statistic/{random_uuid}")
    assert response.status_code == 404


@pytest.mark.xfail(reason="Баг: API возвращает 404 вместо 404")
def test_get_statistic_invalid_id(base_url):
    """Проверяет поведение API при передаче некорректного ID элемента.

    Шаги теста:
    1. Выполняется GET-запрос к /api/2/statistic/invalid_id.
    2. Проверяется, что код ответа 400.
    """
    response = requests.get(f"{base_url}/api/2/statistic/invalid_id")
    assert response.status_code == 400
