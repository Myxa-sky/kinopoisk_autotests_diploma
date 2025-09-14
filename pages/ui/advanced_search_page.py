# pages/ui/advanced_search_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class AdvancedSearchPage:
    """Page Object для расширенного поиска (/s/ страница)"""

    # Старые селекторы для расширенного поиска
    FORM = (By.CSS_SELECTOR, "form[name='film_search']")
    NAME_FIELD = (By.CSS_SELECTOR, "input[name='m_act[find]']")
    YEAR_FROM_DROPDOWN = (By.CSS_SELECTOR, "select[name='m_act[from_year]']")
    GENRE_DROPDOWN = (By.CSS_SELECTOR, "select[name='m_act[genre][]']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[type='button'][value='поиск']")
    RESULTS = (By.CSS_SELECTOR, ".element, .search_item, .movie")

    def __init__(self, browser):
        self.browser = browser

    def open(self):
        self.browser.get("https://www.kinopoisk.ru/s/")
        WebDriverWait(self.browser, 15).until(EC.presence_of_element_located(self.FORM))
        return self

    def set_name(self, name):
        field = self.browser.find_element(*self.NAME_FIELD)
        field.clear()
        field.send_keys(name)
        sleep(1)
        return self

    def set_year(self, year):
        dropdown = self.browser.find_element(*self.YEAR_FROM_DROPDOWN)
        Select(dropdown).select_by_value(str(year))
        sleep(1)
        return self

    def set_genre(self, genre_value):
        dropdown = self.browser.find_element(*self.GENRE_DROPDOWN)
        Select(dropdown).select_by_value(str(genre_value))
        sleep(2)
        return self

    def submit(self):
        """Нажимает кнопку поиска"""
        try:
            button = self.browser.find_element(*self.SUBMIT_BUTTON)
            WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(button))

            url_before = self.browser.current_url
            print(f"URL до submit: {url_before}")

            button.click()

            WebDriverWait(self.browser, 15).until(EC.url_changes(url_before))
            print(f"URL после submit: {self.browser.current_url}")

            # Добавим дополнительную паузу для результатов
            sleep(5)
            return self
        except Exception as e:
            print(f"Ошибка при submit: {e}")
            return self

    def get_results_count(self):
        results = self.browser.find_elements(*self.RESULTS)
        return len(results)

    def set_genre(self, genre_value):
        """Выбирает жанр по значению"""
        try:
            dropdown = self.browser.find_element(*self.GENRE_DROPDOWN)

            # Посмотрим какие опции есть в dropdown
            options = dropdown.find_elements(By.TAG_NAME, "option")
            print(f"Доступные жанры в dropdown:")
            for option in options:
                print(f"  Value: {option.get_attribute('value')}, Text: {option.text}")

            Select(dropdown).select_by_value(str(genre_value))
            sleep(2)
            return self
        except Exception as e:
            print(f"Ошибка выбора жанра {genre_value}: {e}")
            return self
