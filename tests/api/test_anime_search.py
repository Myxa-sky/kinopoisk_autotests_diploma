# tests/api/test_anime_search.py
import allure
import pytest
from tests.api import KinopoiskAPIBase


class TestAnimeSearch(KinopoiskAPIBase):

    @allure.title("Поиск аниме 2023 года с рейтингом IMDB 6-10")
    @allure.feature("Поиск фильмов")
    @allure.story("Поиск по типу и году")
    def test_search_anime_2023(self):
        endpoint = "/movie"
        params = {
            "page": 1,
            "limit": 10,
            "type": "anime",
            "year": 2023,
            "rating.imdb": "6-10"
        }

        response = self.make_get_request(endpoint, params)
        assert response.status_code == 200

        data = response.json()
        assert "docs" in data
        assert len(data["docs"]) > 0, "Аниме 2023 года не найдены"
