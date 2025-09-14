# tests/api/test_movie_by_id.py
import allure
import pytest
from tests.api import KinopoiskAPIBase


class TestMovieById(KinopoiskAPIBase):

    @allure.title("Поиск фильма по ID")
    def test_search_movie_by_id(self):
        endpoint = "/movie/666"

        response = self.make_get_request(endpoint)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == 666

    @allure.title("Поиск несуществующего фильма по ID")
    def test_nonexistent_movie_by_id(self):
        endpoint = "/movie/256"

        response = self.make_get_request(endpoint)
        # Может возвращать 200 с пустыми данными или 404
        if response.status_code == 200:
            data = response.json()
            assert not data.get("name"), "Найден несуществующий фильм"

    @allure.title("Поиск с невалидным ID фильма")
    def test_invalid_movie_id(self):
        endpoint = "/movie/ghdhd"

        response = self.make_get_request(endpoint)
        assert response.status_code in [400, 404]
