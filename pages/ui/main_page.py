# pages/ui/main_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://www.kinopoisk.ru/")
        return self

    def get_login_button(self):
        """Находит кнопку входа с несколькими вариантами селекторов"""
        selectors = [
            "//button[contains(., 'Войти')]",  # Основной селектор
            "//a[contains(., 'Войти')]",  # Если это ссылка
            "//*[contains(text(), 'Вход')]",  # Альтернативный текст
            "[data-tid='login-button']",  # По data-атрибуту
            ".header-login-button",  # По классу
            "//*[@href*='auth']",  # Ссылка на авторизацию
        ]

        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                if element.is_displayed():
                    print(f"✅ Найдена кнопка входа по селектору: {selector}")
                    return element
            except:
                continue

        # Если ничего не найдено, сделаем скриншот для отладки
        self.driver.save_screenshot("login_button_debug.png")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        raise Exception("Не удалось найти кнопку входа ни по одному из селекторов")
