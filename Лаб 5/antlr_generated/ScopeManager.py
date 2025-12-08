from SymbolTable import SymbolTable

class ScopeManager:
    """Менеджер областей видимости для семантического анализа"""

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.functions = {}  # Храним объявления функций

    def add_error(self, message, line=None):
        """Добавление ошибки"""
        if line:
            error_msg = f"Строка {line}: {message}"
        else:
            error_msg = message
        self.errors.append(error_msg)
        print(f"СЕМАНТИЧЕСКАЯ ОШИБКА: {error_msg}")

    def enter_scope(self):
        """Вход в новую область видимости"""
        self.symbol_table.enter_scope()

    def exit_scope(self):
        """Выход из текущей области видимости"""
        self.symbol_table.exit_scope()

    def declare_variable(self, name, var_type, line=None, is_parameter=False):
        """Объявление переменной"""
        # Для параметров функций используем тип 'unknown' вместо 'element'
        if is_parameter:
            var_type = 'unknown'  # Тип определится из использования

        success, result = self.symbol_table.declare(name, var_type)
        if not success:
            self.add_error(result, line)
        return success

    def assign_variable(self, name, line=None):
        """Присваивание значения переменной"""
        success, result = self.symbol_table.assign(name)
        if not success:
            self.add_error(result, line)
        return success

    def check_variable_exists(self, name, line=None):
        """Проверка существования переменной"""
        symbol = self.symbol_table.lookup(name)
        if not symbol:
            self.add_error(f"Использование необъявленной переменной '{name}'", line)
            return False
        return True

    def declare_function(self, name, parameters, return_type='void', line=None):
        """Объявление функции"""
        if name in self.functions:
            self.add_error(f"Функция '{name}' уже объявлена", line)
            return False

        function_info = {
            'name': name,
            'parameters': parameters,
            'return_type': return_type,
            'line': line
        }
        self.functions[name] = function_info

        print(f" Объявлена функция: {name}({', '.join(parameters)})")
        return True

    def check_function_exists(self, name, line=None):
        """Проверка существования функции"""
        if name not in self.functions:
            self.add_error(f"Вызов необъявленной функции '{name}'", line)
            return False
        return True

    def check_function_arguments(self, name, arg_count, line=None):
        """Проверка количества аргументов функции"""
        if not self.check_function_exists(name, line):
            return False

        expected_count = len(self.functions[name]['parameters'])
        if arg_count != expected_count:
            self.add_error(
                f"Функция '{name}' ожидает {expected_count} аргументов, но получено {arg_count}",
                line
            )
            return False
        return True

    def has_errors(self):
        """Проверка наличия ошибок"""
        return len(self.errors) > 0

    def get_errors(self):
        """Получить список ошибок"""
        return self.errors