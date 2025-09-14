from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = (By.NAME, "kp_query")
        self.search_button = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_search_query(self, query):
        search_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.search_input)
        )
        search_field.clear()
        search_field.send_keys(query)
        print(f"Введен поисковый запрос: {query}")

    def click_search_button(self):
        try:
            # Сохраняем текущий URL перед нажатием
            current_url = self.driver.current_url

            # Нажимаем кнопку поиска
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            button.click()
            print("Кнопка поиска нажата")

            # Ждем изменения URL
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.current_url != current_url
            )

            print(f"URL после поиска: {self.driver.current_url}")

        except Exception as e:
            print(f"Ошибка при нажатии кнопки поиска: {e}")
            raise

    def get_search_results(self):
        """Получает результаты поиска с правильными селекторами для Кинопоиска"""
        try:
            # Ждем появления контейнера результатов
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".element, .most_wanted, .search_results"))
            )

            # Пробуем разные селекторы для результатов поиска на Кинопоиске
            result_selectors = [
                ".element",  # Основной селектор
                ".most_wanted .element",
                ".search_results .element",
                ".js-serp-metrika",
                "[data-type='film']",
                ".name a"
            ]

            for selector in result_selectors:
                try:
                    results = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                    )
                    if results:
                        print(f"Найдено {len(results)} результатов по селектору: {selector}")
                        return results
                except:
                    continue

            # Если ничего не найдено, сохраняем отладочную информацию
            self._save_debug_info()
            return []

        except Exception as e:
            print(f"Ошибка при получении результатов: {e}")
            self._save_debug_info()
            return []

    def check_movie_in_results(self, results, movie_name):
        """Проверяет, что указанный фильм есть в результатах"""
        movie_name_lower = movie_name.lower()

        for i, result in enumerate(results):
            result_text = result.text.lower()
            if movie_name_lower in result_text:
                print(f"Найден искомый фильм '{movie_name}' в результате #{i + 1}: {result.text[:50]}...")
                return True

        # Если не нашли, выводим все результаты для отладки
        print("Все найденные результаты:")
        for i, result in enumerate(results):
            print(f"{i + 1}. {result.text}")

        return False

    def _save_debug_info(self):
        """Сохраняет отладочную информацию"""
        try:
            # Скриншот
            self.driver.save_screenshot("search_debug.png")
            print("Скриншот сохранен: search_debug.png")

            # HTML страницы
            with open("search_debug.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print("HTML сохранен: search_debug.html")

            # Текущий URL
            print(f"Текущий URL: {self.driver.current_url}")

        except Exception as e:
            print(f"Ошибка при сохранении отладочной информации: {e}")

    def wait_for_suggest_list(self):
        """Явно ждет появления выпадающего списка предложений"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".suggest-container, .suggest-list, .autocomplete-list"))
            )
            print("Выпадающий список предложений появился")
            return True
        except:
            print("Выпадающий список не появился")
            return False

    def click_first_result(self, results):
        """Кликает на первую ссылку с фильмом в результате поиска"""
        if results:
            first_result = results[0]
            print(f"Кликаем на первый результат: {first_result.text[:50]}...")

            # Сохраняем текущий URL перед кликом
            current_url = self.driver.current_url
            print(f"URL до клика: {current_url}")

            try:
                # Ищем ссылку на фильм (которая ведет на /film/)
                film_links = first_result.find_elements(By.CSS_SELECTOR, "a[href*='/film/']")
                print(f"Найдено ссылок на фильмы: {len(film_links)}")

                if film_links:
                    # Берем первую ссылку, которая ведет на страницу фильма
                    film_link = None
                    for link in film_links:
                        href = link.get_attribute('href')
                        if href and '/film/' in href and '/sr/' in href:
                            film_link = link
                            break

                    if film_link is None and film_links:
                        film_link = film_links[0]  # Берем первую, если не нашли с /sr/

                    print(f"Кликаем на ссылку фильма: {film_link.get_attribute('href')}")

                    # Кликаем через JavaScript для надежности
                    self.driver.execute_script("arguments[0].click();", film_link)
                    print("Клик через JavaScript выполнен")

                    # Ждем изменения URL
                    WebDriverWait(self.driver, 15).until(
                        lambda driver: driver.current_url != current_url
                    )

                    new_url = self.driver.current_url
                    print(f"URL после клика: {new_url}")
                    return True
                else:
                    print("Ссылки на фильм не найдены")
                    return False

            except Exception as e:
                print(f"Ошибка при клике: {e}")
                return False
        return False
