# tests/api/test_reviews.py
import allure
import pytest
from tests.api import KinopoiskAPIBase


class TestReviews(KinopoiskAPIBase):

    @allure.title("Поиск негативных отзывов для фильма")
    def test_search_negative_reviews(self):
        endpoint = "/review"
        params = {
            "page": 1,
            "limit": 10,
            "movieId": 325381,
            "type": "Негативный"
        }

        response = self.make_get_request(endpoint, params)
        assert response.status_code == 200

        data = response.json()
        assert "docs" in data
