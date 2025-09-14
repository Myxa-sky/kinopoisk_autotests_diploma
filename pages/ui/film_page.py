# pages/film_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FilmPage:
    def __init__(self, driver):
        self.driver = driver

    def get_film_title(self):
        """Получает название фильма"""
        try:
            title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1, .moviename-title, .film-title"))
            )
            return title.text
        except:
            return "Название не найдено"

    def get_film_rating(self):
        """Получает рейтинг фильма"""
        try:
            rating = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".rating, .kinopoisk-rating, [itemprop='ratingValue']"))
            )
            return rating.text
        except:
            return "Рейтинг не найден"

    def is_film_page_loaded(self):
        """Проверяет, что страница фильма загрузилась"""
        current_url = self.driver.current_url
        print(f"Текущий URL для проверки: {current_url}")

        # Проверяем различные признаки страницы фильма
        film_indicators = [
            "/film/",
            "movie",
            "фильм",
            "кинопоиск.ru/film"
        ]

        page_text = self.driver.page_source.lower()
        is_film_page = any(indicator in current_url.lower() for indicator in film_indicators)

        if not is_film_page:
            # Дополнительная проверка по содержимому страницы
            content_indicators = [
                "рейтинг",
                "год выпуска",
                "продолжительность",
                "смотреть онлайн",
                "актеры",
                "режиссер"
            ]
            is_film_page = any(indicator in page_text for indicator in content_indicators)

        print(f"Это страница фильма: {is_film_page}")
        return is_film_page
