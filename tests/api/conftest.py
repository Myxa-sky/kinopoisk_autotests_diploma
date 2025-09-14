# tests/api/conftest.py
import pytest
import os


def pytest_collection_modifyitems(items):
    """Отключаем фикстуры браузера для API тестов"""
    for item in items:
        # Убираем фикстуру browser и reset_state для API тестов
        item.fixturenames = [fixture for fixture in item.fixturenames
                           if fixture not in ['browser', 'reset_state']]


@pytest.fixture(scope="class", autouse=True)
def check_api_key():
    """Проверяет наличие API ключа перед запуском API тестов"""
    if not os.getenv("KINOPOISK_API_KEY"):
        pytest.skip("KINOPOISK_API_KEY не установлен. Пропускаем API тесты")
