# pages/search_filters_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


class SearchFiltersPage:
    def __init__(self, driver):
        self.driver = driver

    def open_search_filters(self):
        """Открывает страницу расширенного поиска с фильтрами"""
        self.driver.get("https://www.kinopoisk.ru/s/")
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "select[name]"))
        )
        return True

    def set_genre_filter(self, genre_value):
        """Устанавливает фильтр по жанру"""
        try:
            select = self.driver.find_element(By.CSS_SELECTOR, "select[name='m_act[genre][]']")
            select_obj = Select(select)
            select_obj.select_by_value(genre_value)
            print(f"Установлен жанр: {genre_value}")
            return True
        except Exception as e:
            print(f"Ошибка установки жанра: {e}")
            return False

    def set_year_filter(self, year_from, year_to=None):
        """Устанавливает фильтр по году"""
        try:
            # Год от
            select_from = self.driver.find_element(By.CSS_SELECTOR, "select[name='m_act[from_year]']")
            select_obj_from = Select(select_from)
            select_obj_from.select_by_value(str(year_from))

            # Год до (если указан)
            if year_to:
                select_to = self.driver.find_element(By.CSS_SELECTOR, "select[name='m_act[to_year]']")
                select_obj_to = Select(select_to)
                select_obj_to.select_by_value(str(year_to))

            print(f"Установлены годы: {year_from}-{year_to if year_to else 'н.в.'}")
            return True
        except Exception as e:
            print(f"Ошибка установки года: {e}")
            return False

    def apply_filters(self):
        """Применяет фильтры (нажимает кнопку поиска)"""
        try:
            print("Поиск кнопки применения фильтров...")

            # Ищем кнопку по разным селекторам
            button_selectors = [
                "input[type='submit']",
                "input[value*='Найти']",
                "input[value*='Поиск']",
                "button[type='submit']",
                ".search-btn",
                "input[value=' найти ']",  # с пробелами
                "input[value=' поиск ']",
            ]

            for selector in button_selectors:
                try:
                    print(f"Пробуем селектор: {selector}")
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    print(f"Найдено кнопок: {len(buttons)}")

                    if buttons:
                        button = buttons[0]
                        print(f"Найдена кнопка: {button.get_attribute('outerHTML')[:100]}...")
                        print(f"Кликабельная: {button.is_enabled()} и {button.is_displayed()}")

                        # Кликаем через JavaScript для надежности
                        self.driver.execute_script("arguments[0].click();", button)
                        print("Клик через JavaScript выполнен")

                        # Ждем изменения URL или загрузки результатов
                        try:
                            WebDriverWait(self.driver, 15).until(
                                lambda driver: "m_act" in driver.current_url or
                                               driver.current_url != "https://www.kinopoisk.ru/s/"
                            )
                            print(f"URL после клика: {self.driver.current_url}")
                            return True
                        except:
                            print("URL не изменился после клика")
                            continue

                except Exception as e:
                    print(f"Ошибка с селектором {selector}: {e}")
                    continue

            print("Ни один селектор не сработал")
            return False

        except Exception as e:
            print(f"Общая ошибка применения фильтров: {e}")
            return False

    def get_results_count(self):
        """Возвращает количество результатов"""
        try:
            # Сначала пробуем найти счетчик результатов
            try:
                count_element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results-count, .results-count"))
                )
                return int(count_element.text.replace(' ', ''))
            except:
                # Если счетчика нет, считаем элементы
                results = self.driver.find_elements(By.CSS_SELECTOR, ".element, .film-item")
                return len(results)
        except:
            return 0

    def are_filters_applied(self):
        """Проверяет, что фильтры применились (URL изменился)"""
        return "m_act" in self.driver.current_url

    def find_sort_filter(self):
        """Пытается найти элемент сортировки"""
        try:
            # Ищем по разным возможным селекторам
            sort_selectors = [
                "select[name*='sort']",
                "select[name*='order']",
                ".sort-select",
                "[data-sort]"
            ]

            for selector in sort_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        print(f"Найден возможный элемент сортировки: {selector}")
                        return elements[0]
                except:
                    continue

            print("Элемент сортировки не найден")
            return None

        except Exception as e:
            print(f"Ошибка поиска сортировки: {e}")
            return None
