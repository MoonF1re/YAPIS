class TypeChecker:
    """Проверка типов для ListLang"""

    def __init__(self, scope_manager):
        self.scope_manager = scope_manager
        self.errors = []

    def add_error(self, message, line=None):
        """Добавление ошибки типа"""
        if line:
            error_msg = f"Строка {line}: {message}"
        else:
            error_msg = message
        self.errors.append(error_msg)
        print(f" ОШИБКА ТИПА: {error_msg}")

    def is_numeric_type(self, type_str):
        """Проверяет, является ли тип числовым"""
        return type_str in ['int', 'float', 'element']

    def is_list_type(self, type_str):
        """Проверяет, является ли тип списком или деревом"""
        return type_str in ['list', 'tree', 'queue', 'element']

    def check_operation_types(self, operator, left_type, right_type, line=None):
        """Проверка совместимости типов для операции"""
        # Операция 'in' - разрешаем для element и любых списков
        if operator == 'in':
            # Правая часть должна быть коллекцией (list, tree, queue) или unknown
            if (self.is_list_type(right_type) or
                    right_type in ['unknown', 'element']):
                return True
            else:
                self.add_error(
                    f"Операция 'in' требует список, дерево или очередь справа, получен {right_type}",
                    line
                )
                return False

        # Если один из типов unknown/element - пропускаем проверку
        if left_type in ['unknown', 'element'] or right_type in ['unknown', 'element']:
            return True

        # Операции для списков (конкатенация, разность, пересечение)
        list_operations = ['+', '-', '*']
        if operator in list_operations:
            if self.is_list_type(left_type) and self.is_list_type(right_type):
                return True
            elif self.is_numeric_type(left_type) and self.is_numeric_type(right_type):
                return True
            else:
                self.add_error(
                    f"Операция '{operator}' допустима для списков ИЛИ чисел, получено {left_type} и {right_type}",
                    line
                )
                return False

        # Арифметические операции только для чисел
        arithmetic_operations = ['/', '%']
        if operator in arithmetic_operations:
            if self.is_numeric_type(left_type) and self.is_numeric_type(right_type):
                return True
            else:
                self.add_error(
                    f"Арифметическая операция '{operator}' требует числовые типы, получено {left_type} и {right_type}",
                    line
                )
                return False

        # Операции сравнения
        comparison_operations = ['<', '>', '<=', '>=', '==', '!=']
        if operator in comparison_operations:
            # Разрешаем сравнение чисел, булевых значений и элементов
            if (self.is_numeric_type(left_type) and self.is_numeric_type(right_type)) or \
                    (left_type == 'bool' and right_type == 'bool') or \
                    (left_type in ['unknown', 'element'] and right_type in ['unknown', 'element']):
                return True
            else:
                self.add_error(
                    f"Сравнение '{operator}' требует сравнимые типы, получено {left_type} и {right_type}",
                    line
                )
                return False

        return True

    def get_operation_result_type(self, operator, left_type, right_type):
        """Определяет тип результата операции"""
        # Для element и numeric типов возвращаем numeric
        if (self.is_numeric_type(left_type) or left_type in ['unknown', 'element']) and \
                (self.is_numeric_type(right_type) or right_type in ['unknown', 'element']):
            if operator in ['+', '-', '*', '/', '%']:
                return 'int'

        # Если один из типов unknown/element - возвращаем unknown
        if left_type in ['unknown', 'element'] or right_type in ['unknown', 'element']:
            return 'unknown'

        if operator in ['+', '-', '*']:
            if self.is_list_type(left_type) and self.is_list_type(right_type):
                return 'list'
            elif self.is_numeric_type(left_type) and self.is_numeric_type(right_type):
                if 'float' in [left_type, right_type]:
                    return 'float'
                return 'int'

        elif operator in ['/', '%']:
            if self.is_numeric_type(left_type) and self.is_numeric_type(right_type):
                if 'float' in [left_type, right_type]:
                    return 'float'
                return 'int'

        elif operator in ['<', '>', '<=', '>=', '==', '!=', 'in']:
            return 'bool'

        return 'unknown'

    def check_builtin_function(self, func_name, arg_types, line=None):
        """Проверка встроенных функций - более либеральная версия"""
        builtin_functions = {
            'len': {
                'args': [['list', 'tree', 'queue', 'element', 'unknown']],  # Добавили element и unknown
                'return_type': 'int'
            },
            'balance': {
                'args': [['tree', 'list', 'queue', 'element', 'unknown']],
                'return_type': 'tree'
            },
            'merge': {
                'args': [['list', 'tree', 'queue', 'element', 'unknown'], ['list', 'tree', 'queue', 'element', 'unknown']],
                'return_type': 'list'
            },
            'write': {
                'args': [['int', 'float', 'string', 'list', 'tree', 'queue', 'bool', 'element', 'unknown']],
                'return_type': 'void'
            },
            'read': {
                'args': [],
                'return_type': 'string'
            }
        }

        if func_name not in builtin_functions:
            self.add_error(f"Неизвестная встроенная функция '{func_name}'", line)
            return None

        func_info = builtin_functions[func_name]
        expected_args = func_info['args']

        if len(arg_types) != len(expected_args):
            self.add_error(
                f"Функция '{func_name}' ожидает {len(expected_args)} аргументов, получено {len(arg_types)}",
                line
            )
            return None

        # Более проверка типов аргументов
        for i, (arg_type, expected_types) in enumerate(zip(arg_types, expected_args)):
            if arg_type not in expected_types and arg_type != 'unknown':
                self.add_error(
                    f"Аргумент {i + 1} функции '{func_name}' должен быть {expected_types}, получен {arg_type}",
                    line
                )
                return None

        return func_info['return_type']