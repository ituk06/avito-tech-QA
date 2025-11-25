# Задание 2.1: Тестирование API микросервиса объявлений

## Описание

Микросервис позволяет:

- Создавать объявления
- Получать объявление по его `id`
- Получать все объявления по `sellerID`
- Получать статистику по `item id`


**Host**: `https://qa-internship.avito.com`
API версии: `/api/1/...` и `/api/2/...`

---
- Операционная система: **Windows**, **macOS** или **Linux**

- Python ≥ **3.8**

- `pip` 

## Установка и настройка
1. Склонируйте репозиторий
- git clone [https://github.com/KhElyus/avito-api-tests.git](https://github.com/Khelyus/avito_test_task.git)](https://github.com/Khelyus/avito_test_task.git)

2. Перейдите в директорию проекта
- cd avito_test_task

3. Установка зависимостей
- python -m venv venv
- pip install -r requirements.txt

5. Запустите тесты
- pytest test_api.py -v  

