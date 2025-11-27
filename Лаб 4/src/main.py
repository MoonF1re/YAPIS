import sys
import os
import glob
from antlr4 import *
from ListLangLexer import ListLangLexer
from ListLangParser import ListLangParser
from SemanticAnalyzer import SemanticAnalyzer


def analyze_file(filepath, description):
    """Анализирует файл с кодом и выводит результат"""
    print(f"\n{'=' * 60}")
    print(f"АНАЛИЗ: {description}")
    print(f"Файл: {os.path.basename(filepath)}")
    print(f"{'=' * 60}")

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            code = file.read()

        print(f"Код:\n{code}")

        input_stream = InputStream(code)
        lexer = ListLangLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = ListLangParser(token_stream)

        tree = parser.program()
        analyzer = SemanticAnalyzer()
        success, errors = analyzer.analyze(tree)

        return success

    except FileNotFoundError:
        print(f"Файл {filepath} не найден")
        return False
    except Exception as e:
        print(f"Ошибка при анализе файла {filepath}: {e}")
        return False


def test_valid_examples():
    """Тестируем правильные примеры (должны пройти без ошибок)"""
    print("ТЕСТИРОВАНИЕ ПРАВИЛЬНЫХ ПРИМЕРОВ")
    print("Ожидаемый результат: все примеры должны пройти семантический анализ")
    print("-" * 60)

    valid_files = glob.glob("../tests/valid/*.listlang")

    if not valid_files:
        print("Нет файлов для тестирования в tests/valid/")
        return False

    print(f"Найдено {len(valid_files)} файлов для тестирования")

    all_passed = True
    for filepath in valid_files:
        filename = os.path.basename(filepath)
        success = analyze_file(filepath, f"Правильный пример: {filename}")

        if not success:
            print(f"Тест не пройден: {filename} - ожидался успешный анализ")
            all_passed = False
        else:
            print(f"Тест пройден: {filename}")

    if all_passed:
        print("\nВсе правильные примеры прошли семантический анализ!")
    else:
        print("\nНекоторые правильные примеры не прошли анализ!")

    return all_passed


def test_semantic_error_examples():
    """Тестируем примеры с семантическими ошибками (должны обнаружить ошибки)"""
    print("\nТЕСТИРОВАНИЕ ПРИМЕРОВ С СЕМАНТИЧЕСКИМИ ОШИБКАМИ")
    print("Ожидаемый результат: все примеры должны обнаружить семантические ошибки")
    print("-" * 60)

    error_files = glob.glob("../tests/semantic_errors/*.listlang")

    if not error_files:
        print("Нет файлов для тестирования в tests/semantic_errors/")
        return False

    print(f"Найдено {len(error_files)} файлов для тестирования")

    all_passed = True
    for filepath in error_files:
        filename = os.path.basename(filepath)
        success = analyze_file(filepath, f"Пример с ошибкой: {filename}")

        # В этих примерах мы ОЖИДАЕМ, что анализ завершится с ошибкой
        if success:
            print(f"❌ Тест не пройден: {filename} - ожидалась семантическая ошибка")
            all_passed = False
        else:
            print(f"✅ Тест пройден: {filename} - корректно обнаружена ошибка")

    if all_passed:
        print("\nВсе семантические ошибки корректно обнаружены!")
    else:
        print("\nНекоторые семантические ошибки не были обнаружены!")

    return all_passed


def main():
    """Основная функция"""
    print(" Семантический анализатор ListLang")

    while True:
        print(f"\n{'=' * 60}")
        print("ГЛАВНОЕ МЕНЮ")
        print(f"{'=' * 60}")
        print("1 - Автоматическое тестирование всех примеров")
        print("2 - Тестирование только правильных примеров")
        print("3 - Тестирование только примеров с ошибками")
        print("4 - Выход")

        choice = input("Ваш выбор (1-6): ").strip()

        if choice == "1":
            valid_passed = test_valid_examples()
            error_passed = test_semantic_error_examples()

            if valid_passed and error_passed:
                print("\n Все тесты пройдены успешно!")
            else:
                print("\n Некоторые тесты не пройдены!")

        elif choice == "2":
            test_valid_examples()

        elif choice == "3":
            test_semantic_error_examples()

        elif choice == "4":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()