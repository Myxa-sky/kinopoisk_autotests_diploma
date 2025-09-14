# Автотесты для Кинопоиска

Дипломный проект по автоматизации тестирования веб-приложения Кинопоиск.

## Стек технологий
- Python
- Pytest
- Selenium
- WebDriver Manager
- Allure Framework

## Запуск тестов

1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите тесты: `pytest`
3. Сгенерируйте отчет: `allure serve allure-results`

# UI Autotests for Kinopoisk

Набор автоматизированных тестов для проверки функциональности сайта Кинопоиск.

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt

Запуск всех тестов
python run_all_tests.py
# или
pytest tests/ui/ -v

Запуск всех сьютов
python run_all_suites.py

Структура тестов

1. 🔐 Auth Suite (test_auth_suite.py)
Назначение: Тестирование функциональности авторизации

Тесты:

test_01_login_button_visible - проверка видимости кнопки входа

test_02_auth_form_exists - проверка наличия формы авторизации

test_03_fill_phone_number - заполнение номера телефона

test_04_auth_via_email - авторизация через email

Запуск:

bash
# Весь сьют
pytest tests/ui/test_auth_suite.py -v

# Отдельные тесты
pytest tests/ui/test_auth_suite.py::TestAuthSuite::test_01_login_button_visible -v
pytest tests/ui/test_auth_suite.py::TestAuthSuite::test_04_auth_via_email -v
2. 🧭 Navigation Suite (test_navigation_suite.py)
Назначение: Тестирование навигации по сайту

Тесты:

test_main_page_loads - загрузка главной страницы

test_film_page_loads - загрузка страницы фильма

test_search_page_loads - загрузка страницы поиска

test_navigation_between_pages - навигация между страницами

Запуск:

bash
# Весь сьют
pytest tests/ui/test_navigation_suite.py -v

# Отдельные тесты (пример)
pytest tests/ui/test_navigation_suite.py::TestNavigationSuite::test_film_page_loads -v
3. 🔍 Search Suite (test_search_suite.py)
Назначение: Тестирование поискового функционала

Тесты:

test_search_by_year - поиск по году

test_search_by_genre - поиск по жанру

test_search_specific_movie - поиск конкретного фильма

Запуск:

bash
# Весь сьют
pytest tests/ui/test_search_suite.py -v

# Быстрая проверка поиска
pytest tests/ui/test_search_suite.py::TestSearchSuite::test_search_specific_movie -v
4. ⚠️ Negative Suite (test_negative_suite.py)
Назначение: Тестирование негативных сценариев

Тесты:

test_search_with_invalid_year - поиск с невалидным годом

test_search_empty_parameters - поиск с пустыми параметрами

Запуск:

bash
# Весь сьют
pytest tests/ui/test_negative_suite.py -v
5. ✅ Smoke Suite (test_smoke_suite.py)
Назначение: Смоук-тестирование основных функций

Тесты:

test_main_search - основной поиск

test_navigate_to_film_from_search - навигация к фильму из поиска

Запуск:

bash
# Смоук-тестирование
pytest tests/ui/test_smoke_suite.py -v

# Быстрая проверка
pytest tests/ui/test_smoke_suite.py::TestSmokeSuite::test_main_search -v
6. 🎯 Find & Sort Test (test_find_sort.py)
Назначение: Поиск элементов сортировки

Тесты:

test_find_sort_element - поиск элементов сортировки на странице

Запуск:

bash
pytest tests/ui/test_find_sort.py -v
7. 🏗️ Page Object Tests (test_with_page_object.py)
Назначение: Тестирование с использованием Page Object Pattern

Тесты:

test_search_drama_2020_with_po - поиск драмы 2020 через PO

test_search_specific_movie - поиск фильма через PO

Запуск:

bash
pytest tests/ui/test_with_page_object.py -v

Дополнительные опции
Запуск с пропуском капчи
bash
pytest tests/ui/ --skip-captcha -v
Генерация Allure отчетов
bash
pytest tests/ui/ --alluredir=allure-results
allure serve allure-results
Параллельный запуск
bash
pytest tests/ui/ -n 4 -v

🐛 Troubleshooting
При проблемах с капчей тесты помечаются как skipped - это нормальное поведение.

Для дебага используйте:

bash
pytest tests/ui/ -v --tb=long