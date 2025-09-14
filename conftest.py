# conftest.py
import sys
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Добавляем корень проекта в Python path
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))


@pytest.fixture(scope="session")
def browser():
    """Фикстура для создания и закрытия браузера."""
    print("\nЗапуск браузера для тестовой сессии...")

    chrome_options = Options()

    # Базовые настройки
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Специальные настройки для обхода детекции
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

    # Используем WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Убираем признаки автоматизации
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

    yield driver

    print("\nЗакрытие браузера после тестовой сессии...")
    driver.quit()


@pytest.fixture(autouse=True)
def reset_state(browser):
    """
    Сбрасывает состояние браузера между тестами.
    Выполняется перед каждым тестом автоматически благодаря autouse=True.
    """
    # Действия ДО теста
    browser.delete_all_cookies()  # Очищаем куки - это помогает избежать капчи!

    # Небольшая пауза между тестами для "успокоения" сайта
    time.sleep(2)

    yield

    # Действия ПОСЛЕ теста (если нужны)
    pass
