# run_all_suites.py
import subprocess
import time
import sys
import os


def run_tests():
    """Запускает все сьюты последовательно с паузами"""
    # Получаем абсолютный путь к директории проекта
    project_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"📁 Рабочая директория: {project_dir}")

    suites = [
        "tests/ui/test_smoke_suite.py",
        "tests/ui/test_auth_suite.py",
        "tests/ui/test_search_suite.py",
        "tests/ui/test_navigation_suite.py",
        "tests/ui/test_negative_suite.py"
    ]

    for suite in suites:
        suite_path = os.path.join(project_dir, suite)
        print(f"\n🚀 Запускаем {suite}...")

        # Меняем рабочую директорию на проектную для корректных импортов
        os.chdir(project_dir)

        result = subprocess.run([
            sys.executable, "-m", "pytest",
            suite_path,
            "--alluredir", os.path.join(project_dir, "allure-results"),
            "-v"
        ], capture_output=True, text=True)

        print(f"Код завершения: {result.returncode}")
        if result.stdout:
            print("Вывод:")
            print(result.stdout)
        if result.stderr:
            print("Ошибки:")
            print(result.stderr)

        if result.returncode != 0:
            print(f"⚠️  Сьют {suite} завершился с ошибками")
        else:
            print(f"✅ Сьют {suite} успешно завершен")

        # Пауза между сьютами для избежания капчи
        print("⏳ Ждем 5 секунд...")
        time.sleep(5)

    print("\n🎉 Все сьюты завершены! Генерируем отчет...")
    # Запускаем allure serve
    subprocess.run(["allure", "serve", os.path.join(project_dir, "allure-results")])


if __name__ == "__main__":
    run_tests()
