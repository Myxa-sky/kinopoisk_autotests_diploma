# tests/ui/test_with_page_object.py
import pytest
from pages.ui.advanced_search_page import AdvancedSearchPage  # Импорт прямо в тесте

class TestSearchWithPageObject:
    def test_search_drama_2020_with_po(self, browser):  # используем фикстуру browser
        """Тест поиска драм 2020 года с использованием Page Object."""
        search_page = AdvancedSearchPage(browser)
        results_count = (
            search_page.open()
            .set_name("")
            .set_year(2020)
            .set_genre(8)
            .submit()
            .get_results_count()
        )
        assert results_count > 0
        print(f"✅ Найдено {results_count} драматических фильмов 2020 года!")

    def test_search_specific_movie(self, browser):  # используем фикстуру browser
        """Тест поиска конкретного фильма."""
        search_page = AdvancedSearchPage(browser)
        results_count = (
            search_page.open()
            .set_name("Холоп")
            .set_year(2019)
            .submit()
            .get_results_count()
        )
        assert results_count > 0
        print(f"✅ Найдено результатов для 'Холоп': {results_count}")
