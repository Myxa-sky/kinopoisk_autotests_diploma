from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class AuthPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def debug_current_url(self):
        """Выводим текущий URL для отладки"""
        print(f"Current URL: {self.driver.current_url}")
        return self.driver.current_url

    def debug_page_source(self):
        """Сохраняем HTML страницы для отладки"""
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        print("Page source saved to debug_page.html")

    def wait_for_auth_page(self):
        """Ждем загрузки страницы авторизации"""
        # Даем время для полной загрузки
        time.sleep(3)

        # Выводим отладочную информацию
        self.debug_current_url()
        self.debug_page_source()

        # Ждем появления любого элемента Яндекс.Паспорта
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@id, 'passp')]"))
            )
            return True
        except:
            return False

    def get_phone_field(self):
        """Находим поле для телефона с разными вариантами"""
        try:
            # Вариант 1: По ID
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "passp-field-phone"))
            )
        except:
            # Вариант 2: По классу
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "Textinput-Control_phone"))
            )

    def get_more_options_button(self):
        """Находим кнопку 'Ещё' для других способов входа"""
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "passp:exp-register"))
        )

    def enter_phone(self, phone: str):
        """Вводим номер телефона"""
        phone_field = self.get_phone_field()
        phone_field.clear()
        phone_field.send_keys(phone)
        print(f"Введен номер телефона: {phone}")

    def click_more_options(self):
        """Кликаем на кнопку 'Ещё'"""
        more_button = self.get_more_options_button()
        more_button.click()
        print("Кнопка 'Ещё' нажата")

    def get_email_option(self):
        """Находим опцию входа по email (после нажатия 'Ещё')"""
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Почта')]"))
        )

    def click_email_option(self):
        """Кликаем на опцию входа по email"""
        email_option = self.get_email_option()
        email_option.click()
        print("Выбрана опция входа по почте")

    def get_login_by_username_option(self):
        """Находим опцию 'Войти по логину' в popup"""
        # Сначала ждем появления popup
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "RegistrationButtonPopup-itemButton"))
        )

        # Ищем все кнопки в popup
        buttons = self.driver.find_elements(By.CLASS_NAME, "RegistrationButtonPopup-itemButton")

        # Ищем кнопку с текстом про логин
        for button in buttons:
            if "логину" in button.text or "Войти" in button.text:
                return button

        # Если не нашли, возвращаем последнюю кнопку (обычно это нужная)
        return buttons[-1]

    def click_login_by_username(self):
        """Кликаем на опцию 'Войти по логину'"""
        login_option = self.get_login_by_username_option()
        login_option.click()
        print("Выбрана опция 'Войти по логину'")

    def get_email_field(self):
        """Находим поле для email/логина"""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "passp-field-login"))
        )

    def enter_email(self, email: str):
        """Вводим email/логин"""
        email_field = self.get_email_field()
        email_field.clear()
        email_field.send_keys(email)
        print(f"Введен email: {email}")

    def get_password_field(self):
        """Находим поле для пароля"""
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "passp-field-passwd"))
        )

    def enter_password(self, password: str):
        """Вводим пароль"""
        password_field = self.get_password_field()
        password_field.clear()
        password_field.send_keys(password)
        print("Введен пароль")

    def get_submit_button(self):
        """Находим кнопку 'Войти'"""
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "passp:sign-in"))
        )

    def click_submit(self):
        """Нажимаем кнопку 'Войти'"""
        submit_button = self.get_submit_button()
        submit_button.click()
        print("Кнопка 'Войти' нажата")
