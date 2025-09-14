# tests/ui/test_search_suite.py
import pytest
from pages.ui.advanced_search_page import AdvancedSearchPage  # Новый импорт!


class TestSearchSuite:
    """Suite тестов для расширенного поиска"""

    def test_search_by_year(self, browser):
        """Поиск по году"""
        search_page = AdvancedSearchPage(browser)  # Используем AdvancedSearchPage
        results_count = (
            search_page.open()
            .set_name("")
            .set_year(2020)
            .submit()
            .get_results_count()
        )
        assert results_count > 0, f"Ожидались результаты по году, найдено: {results_count}"

    def test_search_by_genre(self, browser):
        """Поиск по жанру"""
        search_page = AdvancedSearchPage(browser)  # Используем AdvancedSearchPage
        results_count = (
            search_page.open()
            .set_name("")
            .set_year(2020)
            .set_genre(8)  # драма
            .submit()
            .get_results_count()
        )
        assert results_count > 0, f"Ожидались результаты по жанру, найдено: {results_count}"

    def test_search_specific_movie(self, browser):
        """Поиск конкретного фильма"""
        search_page = AdvancedSearchPage(browser)  # Используем AdvancedSearchPage
        results_count = (
            search_page.open()
            .set_name("Холоп")
            .set_year(2019)
            .submit()
            .get_results_count()
        )
        assert results_count > 0, f"Ожидались результаты по фильму, найдено: {results_count}"
