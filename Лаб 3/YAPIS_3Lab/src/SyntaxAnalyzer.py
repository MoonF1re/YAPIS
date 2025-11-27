from antlr4 import *
from src.ListLangLexer import ListLangLexer
from src.ListLangParser import ListLangParser
from antlr4.error.ErrorListener import ErrorListener


class SyntaxErrorException(Exception):
    """Исключение для синтаксических ошибок"""
    pass


class CustomErrorListener(ErrorListener):
    """Кастомный обработчик ошибок"""

    def __init__(self, source_code = None):
        self.errors = []
        self.source_code = source_code
        super().__init__()

    def set_source_code(self, source_code):
        self.source_code = source_code

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        """ recognizer - кто нашел ошибку (лексер или парсер)
            offendingSymbol - проблемный токен
            line, column - позиция ошибки
            msg - сообщение об ошибке от ANTLR
            """
        error_msg = f"Строка {line}:{column} - {msg}"
        self.errors.append(error_msg)

        print(f"СИНТАКСИЧЕСКАЯ ОШИБКА: {error_msg}")

        # Показываем контекст ошибки
        if self.source_code:
            try:
                lines = self.source_code.split('\n')
                if 0 <= line - 1 < len(lines):
                    error_line = lines[line - 1].rstrip()
                    print(f"{error_line}")

                    # Рисуем стрелку на позиции ошибки
                    # Учитываем, что column может быть больше длины строки
                    arrow_pos = min(column, len(error_line))
                    arrow_line = ' ' * arrow_pos + '^'
                    print(f"{arrow_line}")
            except Exception as ex:
                print(f" - Не удалось показать контекст строки")
        else:
            print(f" - Контекст недоступен")

        print()  # Пустая строка для разделения

    def has_errors(self):
        return len(self.errors) > 0


class SyntaxAnalyzer:
    """Синтаксический анализатор для ListLang"""

    def __init__(self):
        self.error_listener = CustomErrorListener()

    def analyze(self, code):
        """Анализирует код на синтаксические ошибки"""
        print("Начинаю синтаксический анализ...")
        self.error_listener.errors = []
        self.error_listener.set_source_code(code)

        input_stream = InputStream(code)  # Преобразует строку кода в поток символов

        lexer = ListLangLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener) #Удаляем и меняем лексер на наш

        token_stream = CommonTokenStream(lexer)

        parser = ListLangParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)

        try:
            tree = parser.program()

            if self.error_listener.has_errors():
                print(f"Обнаружено {len(self.error_listener.errors)} ошибок.")
            else:
                print("Синтаксический анализ завершен успешно!")
                return True

        except Exception as e:
            print(f"Критическая ошибка при анализе: {e}")
            return False

    def analyze_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                code = file.read()
            print(f"Анализирую файл: {filename}")
            return self.analyze(code)
        except FileNotFoundError:
            print(f"Файл {filename} не найден")
            return False