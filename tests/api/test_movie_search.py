# tests/api/test_movie_search.py
import allure
import pytest
from tests.api import KinopoiskAPIBase


class TestMovieSearch(KinopoiskAPIBase):

    @allure.title("Поиск фильма по названию 'Вверх'")
    def test_search_movie_by_title(self):
        endpoint = "/movie/search"
        params = {
            "page": 1,
            "limit": 10,
            "query": "Вверх"
        }

        response = self.make_get_request(endpoint, params)
        assert response.status_code == 200

        data = response.json()
        assert len(data["docs"]) > 0, "Фильм 'Вверх' не найден"

    @allure.title("Поиск несуществующего фильма по названию")
    def test_nonexistent_movie_by_title(self):
        endpoint = "/movie/search"
        params = {
            "page": 1,
            "limit": 10,
            "query": "одпордародлрло"
        }

        response = self.make_get_request(endpoint, params)
        assert response.status_code == 200

        data = response.json()
        assert len(data["docs"]) == 0, "Найдены фильмы по несуществующему запросу"
