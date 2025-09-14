# run_all_tests.py
import pytest
import time
import os


def run_all_tests():
    """Запускает ВСЕ тесты в одной сессии pytest"""
    print("🚀 Запуск всех тестов в одной сессии...")

    # Список всех наших сьютов
    test_files = [
        "tests/ui/test_smoke_suite.py",
        "tests/ui/test_auth_suite.py",
        "tests/ui/test_search_suite.py",
        "tests/ui/test_navigation_suite.py",
        "tests/ui/test_negative_suite.py"
    ]

    # Проверяем какие файлы существуют
    existing_files = []
    for file in test_files:
        if os.path.exists(file):
            existing_files.append(file)
            print(f"✅ Найден: {file}")
        else:
            print(f"❌ Отсутствует: {file}")

    if not existing_files:
        print("⚠️  Нет тестовых файлов для запуска!")
        return

    # Запускаем ВСЕ тесты в одной сессии pytest
    print(f"\n🎯 Запускаем {len(existing_files)} файлов...")

    try:
        # Запускаем pytest напрямую, а не через subprocess
        exit_code = pytest.main([
            *existing_files,
            "--alluredir", "allure-results",
            "-v",
            "--tb=short"  # Короткие tracebacks
        ])

        if exit_code == 0:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        else:
            print(f"\n⚠️  Некоторые тесты упали. Код завершения: {exit_code}")

    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")


if __name__ == "__main__":
    run_all_tests()
