# tests/api/__init__.py
import allure
import requests
import os
from typing import Dict, Any, Optional


class KinopoiskAPIBase:
    BASE_URL = "https://api.kinopoisk.dev/v1.4"

    @property
    def api_key(self):
        # Получаем ключ из переменных окружения
        key = os.getenv("KINOPOISK_API_KEY")
        if not key:
            raise ValueError("KINOPOISK_API_KEY не установлен в переменных окружения")
        return key

    @allure.step("Выполнить GET запрос к {endpoint}")
    def make_get_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                         use_auth: bool = True) -> requests.Response:
        """Базовый метод для GET запросов"""
        headers = {
            "User-Agent": "Python-Requests/2.31.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "accept": "application/json"
        }

        if use_auth:
            headers["X-API-KEY"] = self.api_key

        response = requests.get(
            f"{self.BASE_URL}{endpoint}",
            headers=headers,
            params=params,
            timeout=30
        )

        allure.attach(f"Request: GET {endpoint}", str(params), allure.attachment_type.TEXT)
        allure.attach(f"Response: {response.status_code}", response.text, allure.attachment_type.TEXT)

        return response
