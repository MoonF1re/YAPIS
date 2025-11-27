from SyntaxAnalyzer import SyntaxAnalyzer
import os
import glob


def test_valid_examples():
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ПРАВИЛЬНЫХ ПРИМЕРОВ")
    print("=" * 50)

    analyzer = SyntaxAnalyzer()
    valid_files = glob.glob("../tests/valid/*.listlang")

    for filepath in valid_files:
        print(f"\n Тестируем: {os.path.basename(filepath)}")
        success = analyzer.analyze_file(filepath)

        if not success:
            print(f"Неожиданная ошибка в правильном примере!")
            return False

    print("\n Все правильные примеры прошли проверку!")
    return True


def test_invalid_examples():
    """Тестируем на примерах с ошибками"""
    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ ОШИБОЧНЫХ ПРИМЕРОВ")
    print("=" * 50)

    analyzer = SyntaxAnalyzer()
    invalid_files = glob.glob("../tests/invalid/*.listlang")

    for filepath in invalid_files:
        print(f"\n Тестируем: {os.path.basename(filepath)}")
        success = analyzer.analyze_file(filepath)

        if success:
            print(f"Ожидалась ошибка, но анализ прошел успешно!")
            return False
        else:
            print(f"Корректно обнаружена ошибка (как и ожидалось)")

    print("\nВсе ошибки корректно обнаружены!")
    return True


def interactive_mode():
    """Интерактивный режим для ввода кода"""
    print("\n" + "=" * 50)
    print("ИНТЕРАКТИВНЫЙ РЕЖИМ")
    print("=" * 50)
    print("Введите код на ListLang (Ctrl+D для завершения):")

    code_lines = []
    try:
        while True:
            line = input()
            code_lines.append(line)
    except EOFError:
        pass

    code = '\n'.join(code_lines)
    analyzer = SyntaxAnalyzer()
    analyzer.analyze(code)



if __name__ == "__main__":

    # if test_valid_examples() and test_invalid_examples():
    #     print("\nВсе тесты пройдены успешно!")
    # else:
    #     print("\nНекоторые тесты не пройдены!")

    # Интерактивный режим
    interactive_mode()