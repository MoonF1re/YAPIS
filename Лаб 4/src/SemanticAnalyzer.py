from antlr4 import *
from ListLangParser import ListLangParser
from ListLangVisitor import ListLangVisitor
from ScopeManager import ScopeManager
from TypeChecker import TypeChecker


class SemanticAnalyzer(ListLangVisitor):
    """Семантический анализатор для ListLang"""

    def __init__(self):
        self.scope_manager = ScopeManager()
        self.type_checker = TypeChecker(self.scope_manager)
        self.current_line = 0

    def analyze(self, tree):
        """Запуск семантического анализа"""
        print("\nНачинаю семантический анализ... \n")

        self.visit(tree)

        if self.scope_manager.has_errors() or self.type_checker.errors:
            all_errors = self.scope_manager.get_errors() + self.type_checker.errors

            print(f"\nОбнаружено {len(all_errors)} семантических ошибок:")
            for error in all_errors:
                print(f"   - {error}")
            return False, all_errors
        else:
            print("Семантический анализ завершен успешно!")

            return True, []

    def set_current_line(self, ctx):
        """Установка текущей строки для сообщений об ошибках"""
        if hasattr(ctx, 'start') and ctx.start:
            self.current_line = ctx.start.line

    def visitProgram(self, ctx: ListLangParser.ProgramContext):
        """Обработка всей программы"""
        for child in ctx.children:
            self.visit(child) #Рекурсивно обходит каждый дочерний узел дерева
        return None

    def visitFunctionDecl(self, ctx: ListLangParser.FunctionDeclContext):
        """Обработка объявления функции"""
        self.set_current_line(ctx)

        func_name = ctx.ID().getText()
        parameters = []

        param_list = ctx.parameterList()
        if param_list:
            for param in param_list.ID():
                param_name = param.getText()
                parameters.append(param_name)

        # Определяем тип возврата по имени (временно, пока не реализован анализ return)
        return_type = 'list'
        if 'tree' in func_name.lower():
            return_type = 'tree'
        elif 'queue' in func_name.lower():
            return_type = 'queue'

        # Объявляем функцию
        self.scope_manager.declare_function(func_name, parameters, return_type, self.current_line)

        # Входим в область видимости функции
        self.scope_manager.enter_scope()

        # Объявляем параметры с типом 'unknown'
        for param in parameters:
            self.scope_manager.declare_variable(param, 'unknown', self.current_line, is_parameter=True)

        # Анализируем тело функции (это объявит все переменные и проверит типы)
        self.visit(ctx.block())

        self.scope_manager.exit_scope()
        return None

    def visitReturnStatement(self, ctx: ListLangParser.ReturnStatementContext):
        """Обработка оператора return"""
        if ctx.expression():
            return self.visit(ctx.expression())
        return 'void' # return без значения

    def visitBlock(self, ctx: ListLangParser.BlockContext):
        """Обработка блока кода"""
        self.scope_manager.enter_scope()

        for statement in ctx.statement():
            self.visit(statement) # Анализируем каждый оператор в блоке

        self.scope_manager.exit_scope()
        return None

    def visitAssignment(self, ctx: ListLangParser.AssignmentContext):
        """Обработка присваивания"""
        self.set_current_line(ctx)

        var_name = ctx.ID().getText()
        expr_type = self.visit(ctx.expression()) # Определяем выражения справа

        existing_symbol = self.scope_manager.symbol_table.lookup(var_name)
        if existing_symbol:
            self.scope_manager.assign_variable(var_name, self.current_line)
        else:
            var_type = expr_type if expr_type else 'unknown'
            self.scope_manager.declare_variable(var_name, var_type, self.current_line)

        return expr_type

    def visitIdExpr(self, ctx: ListLangParser.IdExprContext):
        """Обработка идентификатора"""
        self.set_current_line(ctx)

        var_name = ctx.ID().getText()
        symbol = self.scope_manager.symbol_table.lookup(var_name)

        if symbol:
            return symbol.type
        else:
            # Добавляем ошибку (раньше это делал check_variable_exists)
            self.scope_manager.add_error(f"Использование необъявленной переменной '{var_name}'", self.current_line)
            return 'unknown'

    def visitFunctionCallExpr(self, ctx: ListLangParser.FunctionCallExprContext):
        """Обработка вызова функции"""
        self.set_current_line(ctx)

        func_name = ctx.functionCall().ID().getText()
        arg_list = ctx.functionCall().argumentList()


        # Проверяем аргументы
        arg_types = []
        if arg_list:
            for arg in arg_list.expression():
                arg_type = self.visit(arg)
                arg_types.append(arg_type)

        # Проверяем встроенные функции
        builtin_functions = ['len', 'balance', 'merge', 'write', 'read']
        if func_name in builtin_functions:
            return_type = self.type_checker.check_builtin_function(func_name, arg_types, self.current_line)
            return return_type if return_type else 'unknown'

        # Проверяем пользовательские функции
        if self.scope_manager.check_function_exists(func_name, self.current_line):
            self.scope_manager.check_function_arguments(func_name, len(arg_types), self.current_line)
            # Возвращаем тип функции из объявления
            func_info = self.scope_manager.functions[func_name]
            return func_info['return_type']

        return 'unknown'

    def visitLiteralExpr(self, ctx: ListLangParser.LiteralExprContext):
        """Обработка литералов"""
        literal = ctx.literal()

        if literal.INT():
            return 'int'
        elif literal.FLOAT():
            return 'float'
        elif literal.STRING():
            return 'string'
        elif literal.TRUE() or literal.FALSE():
            return 'bool'
        elif literal.NULL():
            return 'null'

        return 'unknown'

    def visitAdditiveExpr(self, ctx: ListLangParser.AdditiveExprContext):
        """Обработка аддитивных выражений"""
        self.set_current_line(ctx)

        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))
        operator = ctx.op.text

        if self.type_checker.check_operation_types(operator, left_type, right_type, self.current_line):
            result_type = self.type_checker.get_operation_result_type(operator, left_type, right_type)
            return result_type

        return 'unknown'

    def visitMultiplicativeExpr(self, ctx: ListLangParser.MultiplicativeExprContext):
        """Обработка мультипликативных выражений"""
        self.set_current_line(ctx)

        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))
        operator = ctx.op.text

        if self.type_checker.check_operation_types(operator, left_type, right_type, self.current_line):
            result_type = self.type_checker.get_operation_result_type(operator, left_type, right_type)
            return result_type

        return 'unknown'

    def visitComparisonExpr(self, ctx: ListLangParser.ComparisonExprContext):
        """Обработка выражений сравнения"""
        self.set_current_line(ctx)

        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))
        operator = ctx.op.text

        if self.type_checker.check_operation_types(operator, left_type, right_type, self.current_line):
            return 'bool'

        return 'unknown'

    def visitInExpr(self, ctx: ListLangParser.InExprContext):
        """Обработка операции 'in'"""
        self.set_current_line(ctx)

        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))

        # Используем TypeChecker для проверки типов
        if not self.type_checker.check_operation_types('in', left_type, right_type, self.current_line):
            return 'bool'  # Все равно возвращаем bool, чтобы продолжить анализ

        return 'bool'

    def visitListExpr(self, ctx: ListLangParser.ListExprContext):
        """Обработка списков"""
        expr_list = ctx.expressionList()

        if expr_list:
            # Проверяем типы всех элементов, но не блокируем анализ
            for expr in expr_list.expression():
                element_type = self.visit(expr)
                # Если все элементы числовые, можно считать список числовым
                # но пока возвращаем просто 'list'

        return 'list'

    def visitCastExpr(self, ctx: ListLangParser.CastExprContext):
        """Обработка преобразования типов"""
        self.set_current_line(ctx)

        target_type = ctx.type_().getText()
        expr_type = self.visit(ctx.expression())

        # Проверяем допустимость преобразования
        valid_casts = {
            'int': ['float', 'string'],
            'float': ['int', 'string'],
            'string': ['int', 'float'],
            'list': ['tree'],
            'tree': ['list']
        }

        if expr_type in valid_casts and target_type in valid_casts[expr_type]:
            return target_type
        else:
            self.type_checker.add_error(
                f"Недопустимое преобразование из {expr_type} в {target_type}",
                self.current_line
            )
            return 'unknown'

    def visitIndexExpr(self, ctx: ListLangParser.IndexExprContext):
        """Обработка индексации (list[index])"""
        self.set_current_line(ctx)

        # Проверяем коллекцию
        collection_type = self.visit(ctx.expression(0))
        # Проверяем индекс
        index_type = self.visit(ctx.expression(1))

        # Для индексации возвращаем тип элемента
        if self.type_checker.is_list_type(collection_type) or collection_type in ['unknown', 'element']:
            return 'element'
        else:
            self.type_checker.add_error(
                f"Индексация применима только к спискам, деревьям и очередям, получен {collection_type}",
                self.current_line
            )
            return 'unknown'

    def visitRangeExpr(self, ctx: ListLangParser.RangeExprContext):
        """Обработка диапазона (start..end)"""
        self.set_current_line(ctx)

        start_type = self.visit(ctx.expression(0))
        end_type = self.visit(ctx.expression(1))

        # Диапазон всегда создает список чисел
        return 'list'

    def visitParenExpr(self, ctx: ListLangParser.ParenExprContext):
        """Обработка выражений в скобках"""
        return self.visit(ctx.expression())

    def visitAndExpr(self, ctx: ListLangParser.AndExprContext):
        """Обработка логического И"""
        self.set_current_line(ctx)

        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))

        # Для логических операций возвращаем bool
        return 'bool'

    def visitOrExpr(self, ctx: ListLangParser.OrExprContext):
        """Обработка логического ИЛИ"""
        self.set_current_line(ctx)

        left_type = self.visit(ctx.expression(0))
        right_type = self.visit(ctx.expression(1))

        # Для логических операций возвращаем bool
        return 'bool'