# pages/ui/search_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class SearchPage:
    """Page Object для страницы поиска Кинопоиска (актуальная версия)"""

    # Селекторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='kp_query']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_RESULTS = [
        (By.CSS_SELECTOR, ".film"),
        (By.CSS_SELECTOR, ".movie"),
        (By.CSS_SELECTOR, "[data-testid*='film']"),
        (By.CSS_SELECTOR, "div > h3"),
        (By.CSS_SELECTOR, "a[href*='/film/']")
    ]

    def __init__(self, browser):  # Добавляем конструктор!
        self.browser = browser

    def open(self):
        """Открывает главную страницу"""
        self.browser.get("https://www.kinopoisk.ru/")
        WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        return self

    def set_name(self, name):
        """Заполняет поле поиска"""
        field = self.browser.find_element(*self.SEARCH_INPUT)
        field.clear()
        field.send_keys(name)
        sleep(1)
        return self

    def submit(self):
        """Нажимает кнопку поиска"""
        button = self.browser.find_element(*self.SEARCH_BUTTON)
        WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable(button))

        url_before = self.browser.current_url
        button.click()

        WebDriverWait(self.browser, 15).until(EC.url_changes(url_before))
        sleep(3)
        return self

    def get_results_count(self):
        """Возвращает количество найденных результатов"""
        for selector in self.SEARCH_RESULTS:
            try:
                results = self.browser.find_elements(*selector)
                if results:
                    print(f"Найдено результатов по селектору {selector}: {len(results)}")
                    return len(results)
            except:
                continue
        return 0
