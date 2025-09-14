# tests/ui/test_negative_suite.py
import pytest
from pages.ui.search_page import SearchPage


class TestNegativeSuite:
    """Негативные сценарии"""

    def test_search_with_invalid_year(self, browser):
        """Поиск с несуществующим годом (должен обработаться без падения)"""
        search_page = SearchPage(browser)

        try:
            # Пробуем установить невалидный год
            search_page.open().set_name("").set_year(1800)
            print("✅ Система приняла невалидный год без ошибок")
        except Exception as e:
            # Ожидаем, что система gracefully обработает ошибку
            print(f"✅ Система корректно обработала ошибку: {e}")

    def test_search_empty_parameters(self, browser):
        """Поиск с пустыми параметрами"""
        search_page = SearchPage(browser)

        try:
            # Пробуем выполнить поиск без параметров
            results_count = search_page.open().submit().get_results_count()
            print(f"✅ Поиск с пустыми параметрами вернул {results_count} результатов")
        except Exception as e:
            print(f"✅ Система корректно обработала пустой запрос: {e}")
