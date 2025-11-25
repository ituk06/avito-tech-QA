import re
import pytest
import requests
import random
import string
import uuid

BASE_URL = "https://qa-internship.avito.com"
SELLER_ID = 4962657
SELLER_ID_NO_ITEMS = 4962637


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def seller_id():
    return SELLER_ID


@pytest.fixture(scope="session")
def seller_id_no_items():
    return SELLER_ID_NO_ITEMS


@pytest.fixture()
def random_uuid():
    return str(uuid.uuid4())


@pytest.fixture(scope="session")
def random_item_name():
    return "test_" + "".join(random.choices(string.ascii_letters, k=5))


def _create_test_item(base_url, seller_id, random_item_name):
    """Вспомогательная функция для создания тестового объявления.

    Шаги:
    1. Формируется payload с обязательными полями: sellerId, name, price, statistics.
    2. Выполняется POST-запрос к /api/1/item.
    3. Если API возвращает строку с UUID, извлекается ID объявления.
    4. Возвращается словарь с ключами:
       - 'id' — ID объявления
       - 'status_text' — текст статуса ответа
       - 'full_response' — полный JSON-ответ API
    5. Если API вернет нормальную структуру, возвращается JSON напрямую.
    """
    payload = {
        "sellerId": seller_id,
        "name": random_item_name,
        "price": 500,
        "statistics": {
            "likes": 100,
            "viewCount": 100,
            "contacts": 100
        }
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    response.raise_for_status()
    data = response.json()

    if "status" in data:
        status_text = data["status"]
        uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'
        match = re.search(uuid_pattern, status_text)

        if match:
            item_id = match.group(0)
            return {
                "id": item_id,
                "status_text": status_text,
                "full_response": data
            }
        else:
            raise ValueError(f"Could not extract ID from response: {status_text}")
    else:
        # Если вдруг API починят и вернут нормальную структуру
        return data


@pytest.fixture(scope="session")
def create_test_item(base_url, seller_id, random_item_name):
    return _create_test_item(base_url, seller_id, random_item_name)


@pytest.fixture(scope="session")
def create_test_item_for_delete(base_url, seller_id, random_item_name):
    return _create_test_item(base_url, seller_id, random_item_name)
