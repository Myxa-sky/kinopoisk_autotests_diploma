# tests/api/test_negative_cases.py
import allure
import pytest
from tests.api import KinopoiskAPIBase


class TestNegativeCases(KinopoiskAPIBase):

    @allure.title("Запрос без авторизации")
    def test_request_without_auth(self):
        endpoint = "/movie/666"

        response = self.make_get_request(endpoint, use_auth=False)
        assert response.status_code in [401, 403]

    @allure.title("Поиск актера по несуществующему ID")
    def test_nonexistent_person(self):
        endpoint = "/person/2589663147"

        response = self.make_get_request(endpoint)
        # Может возвращать 200 с пустыми данными или 404
        if response.status_code == 200:
            data = response.json()
            assert not data.get("name"), "Найден несуществующий актер"
