class Symbol:
    """Представляет символ в программе"""

    def __init__(self, name, symbol_type, value=None, scope_level=0):
        self.name = name
        self.type = symbol_type  # 'int', 'list', 'tree', 'function' и т.д.
        self.value = value
        self.scope_level = scope_level
        self.is_initialized = value is not None

    def __str__(self):
        return f"Symbol({self.name}, {self.type}, scope={self.scope_level})"


class SymbolTable:
    """Таблица символов с поддержкой областей видимости"""

    def __init__(self):
        self.scope_level = 0
        self.scope_stack = [{}]  # Стек областей видимости

    def enter_scope(self):
        """Вход в новую область видимости"""
        self.scope_level += 1
        self.scope_stack.append({})
        print(f"Вход в область видимости уровня {self.scope_level}")

    def exit_scope(self):
        """Выход из текущей области видимости"""
        if len(self.scope_stack) > 1:
            self.scope_level -= 1
            removed_scope = self.scope_stack.pop()
            print(f"Выход из области видимости, удалено символов: {len(removed_scope)}")
            return removed_scope
        return {}

    def declare(self, name, symbol_type, value=None):
        """Объявление нового символа"""
        current_scope = self.scope_stack[-1]

        if name in current_scope:
            return False, f"Переменная '{name}' уже объявлена в текущей области видимости"

        symbol = Symbol(name, symbol_type, value, self.scope_level)
        current_scope[name] = symbol

        print(f" Объявлена переменная: {symbol}")
        return True, symbol

    def lookup(self, name):
        """Поиск символа по имени (от текущей области к глобальной)"""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        return None

    def assign(self, name, value=None):
        """Присваивание значения переменной"""
        symbol = self.lookup(name)
        if symbol:
            symbol.value = value
            symbol.is_initialized = True
            print(f" Присвоено значение переменной '{name}'")
            return True, symbol
        return False, f"Переменная '{name}' не объявлена"

    def get_current_scope_symbols(self):
        """Получить все символы текущей области видимости"""
        return list(self.scope_stack[-1].values())