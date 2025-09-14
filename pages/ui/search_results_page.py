# pages/search_results_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver

    def apply_genre_filter(self, genre_name):
        """Применяет фильтр по жанру"""
        try:
            # Открываем фильтр жанров
            genre_filter = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".filter-genre, [data-filter='genre']"))
            )
            genre_filter.click()

            # Выбираем конкретный жанр
            genre_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//label[contains(text(), '{genre_name}')]"))
            )
            genre_option.click()

            # Ждем применения фильтра
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".results-loaded"))
            )
            print(f"Применен фильтр жанра: {genre_name}")
            return True

        except Exception as e:
            print(f"Ошибка применения фильтра жанра: {e}")
            return False

    def apply_year_filter(self, year_from, year_to=None):
        """Применяет фильтр по году"""
        try:
            # Заполняем поле "год от"
            year_from_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[name='year_from'], #year_from"))
            )
            year_from_field.clear()
            year_from_field.send_keys(str(year_from))

            if year_to:
                # Заполняем поле "год до"
                year_to_field = self.driver.find_element(By.CSS_SELECTOR, "[name='year_to'], #year_to")
                year_to_field.clear()
                year_to_field.send_keys(str(year_to))

            # Ждем применения фильтра
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".results-loaded"))
            )
            print(f"Применен фильтр года: {year_from}-{year_to if year_to else 'н.в.'}")
            return True

        except Exception as e:
            print(f"Ошибка применения фильтра года: {e}")
            return False

    def sort_by(self, sort_option):
        """Сортирует результаты"""
        try:
            sort_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='sort'], .sort-select"))
            )
            select = Select(sort_dropdown)
            select.select_by_visible_text(sort_option)

            # Ждем пересортировки
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".results-loaded"))
            )
            print(f"Применена сортировка: {sort_option}")
            return True

        except Exception as e:
            print(f"Ошибка сортировки: {e}")
            return False

    def get_result_count(self):
        """Возвращает количество результатов"""
        try:
            # Сначала попробуем найти счетчик
            count_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".results-count, .search-result-count"))
            )
            count = int(count_element.text.replace(' ', ''))
            print(f"Найдено через счетчик: {count}")
            return count
        except:
            # Если счетчик не найден, считаем элементы
            results = self.driver.find_elements(By.CSS_SELECTOR, ".element, .film-item, .movie")
            print(f"Найдено через элементы: {len(results)}")

            # Отладочная информация: посмотрим что вообще есть на странице
            elements = self.driver.find_elements(By.CSS_SELECTOR, "*")
            print(f"Всего элементов на странице: {len(elements)}")

            return len(results)
