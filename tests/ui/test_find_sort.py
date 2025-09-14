import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class TestFindSort:

    def test_find_sort_element(self, browser):
        """Тест поиска и проверки элементов сортировки на странице поиска"""
        browser.get("https://www.kinopoisk.ru/s/")

        # Проверяем капчу
        if "вы не робот" in browser.title.lower():
            pytest.skip("Капча заблокировала доступ к странице поиска")

        print("=== ПОИСК ЭЛЕМЕНТА СОРТИРОВКИ ===")

        # Ждем загрузки страницы
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except TimeoutException:
            pytest.fail("Страница поиска не загрузилась")

        # Ищем по разным селекторам
        sort_selectors = [
            "select[name*='sort']",
            "select[name*='order']",
            ".sort-select",
            "[data-sort]",
            "[data-testid*='sort']",
            "select option[value*='rating']",
            "select option[value*='year']",
            "select option[value*='popular']"
        ]

        found_elements = []
        for selector in sort_selectors:
            try:
                elements = browser.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Найдено по '{selector}': {len(elements)}")
                    for element in elements:
                        element_info = self._get_element_info(element)
                        found_elements.append(element_info)
            except Exception as e:
                print(f"Ошибка с селектором {selector}: {e}")

        # Минимальная проверка что страница функциональна
        assert "поиск" in browser.title.lower() or "search" in browser.title.lower(), \
            f"Это не страница поиска: {browser.title}"

        print(f"\nНайдено возможных элементов сортировки: {len(found_elements)}")
        for i, info in enumerate(found_elements[:10]):
            print(f"{i + 1}. {info}")

    def _get_element_info(self, element):
        """Вспомогательный метод для получения информации об элементе"""
        info = f"tag: {element.tag_name}"

        if element.tag_name == 'select':
            info += f", name: {element.get_attribute('name') or 'N/A'}"
            info += f", id: {element.get_attribute('id') or 'N/A'}"
        elif element.tag_name == 'option':
            info += f", value: {element.get_attribute('value') or 'N/A'}"
            info += f", text: {element.text[:30]}..." if element.text else ", text: None"
        else:
            info += f", class: {element.get_attribute('class') or 'N/A'}"
            info += f", data-sort: {element.get_attribute('data-sort') or 'N/A'}"

        return info
