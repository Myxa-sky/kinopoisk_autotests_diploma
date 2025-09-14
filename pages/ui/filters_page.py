# pages/filters_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class FiltersPage:
    def __init__(self, driver):
        self.driver = driver

    def open_filters_section(self):
        """Открывает раздел с фильтрами"""
        try:
            # Открываем раздел "Фильмы" где есть фильтры
            self.driver.get("https://www.kinopoisk.ru/lists/movies/")

            # Или главную страницу с фильтрами
            # self.driver.get("https://www.kinopoisk.ru/chance/")

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".filters, .filter-section"))
            )
            return True
        except:
            return False

    def find_and_click_filter(self, filter_name):
        """Находит и кликает на фильтр по названию"""
        try:
            # Пробуем разные селекторы для фильтров
            filter_selectors = [
                f"//button[contains(text(), '{filter_name}')]",
                f"//label[contains(text(), '{filter_name}')]",
                f"//span[contains(text(), '{filter_name}')]",
                f"[title*='{filter_name}']",
                f"[data-filter*='{filter_name.lower()}']"
            ]

            for selector in filter_selectors:
                try:
                    if selector.startswith('//'):
                        element = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        element = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )

                    element.click()
                    print(f"Найден и кликнут фильтр: {filter_name}")
                    return True
                except:
                    continue

            return False

        except Exception as e:
            print(f"Ошибка поиска фильтра {filter_name}: {e}")
            return False

    def apply_text_filter(self, field_name, value):
        """Применяет текстовый фильтр (год, рейтинг и т.д.)"""
        try:
            field_selectors = [
                f"input[name='{field_name}']",
                f"input[placeholder*='{field_name}']",
                f"#{field_name}",
                f".{field_name}-input"
            ]

            for selector in field_selectors:
                try:
                    field = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    field.clear()
                    field.send_keys(str(value))
                    print(f"Заполнено поле {field_name}: {value}")
                    return True
                except:
                    continue

            return False

        except Exception as e:
            print(f"Ошибка заполнения поля {field_name}: {e}")
            return False
