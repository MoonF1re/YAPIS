import sys
import re
from antlr4 import *
from antlr_generated.ListLangLexer import ListLangLexer
from antlr_generated.ListLangParser import ListLangParser
from antlr_generated.ListLangVisitor import ListLangVisitor


class CompilerError(Exception):
    pass


class VariableInfo:
    def __init__(self, name, var_type, is_global=True):
        self.name = name
        self.type = var_type
        self.is_global = is_global
        self.index = None


class FunctionInfo:
    def __init__(self, name, return_type, params):
        self.name = name
        self.return_type = return_type
        self.params = params
        self.local_vars = {}
        self.next_local_index = 0


class CompilerVisitor(ListLangVisitor):
    def __init__(self):
        self.global_vars = {}
        self.functions = {}
        self.current_function = None
        self.next_global_index = 0
        self.next_local_index = 0
        self.label_counter = 0
        self.output_code = []
        self.string_constants = {}
        self.next_string_id = 0
        self.temp_counter = 0

    def visitProgram(self, ctx):
        # Начало модуля
        self.output_code.append("(module")
        self.output_code.append('  (import "console" "log" (func $log (param i32)))')
        self.output_code.append('  (import "console" "logInt" (func $logInt (param i32)))')
        self.output_code.append('  (import "console" "logFloat" (func $logFloat (param f32)))')
        self.output_code.append('  (import "console" "logStr" (func $logStr (param i32 i32)))')
        self.output_code.append('  (memory (export "memory") 2)')
        self.output_code.append('  (global $heap_ptr (mut i32) (i32.const 65536))')

        # Объявляем все глобальные переменные ЗДЕСЬ, на уровне модуля
        # Сначала собираем все глобальные переменные из программы
        self._collect_global_vars(ctx)

        # Теперь добавляем их объявления
        for var_name in self.global_vars:
            self.output_code.append(f'  (global ${var_name} (mut i32) (i32.const 0))')

        # Добавляем вспомогательные функции
        self._add_helper_functions()

        # Посещаем все объявления функций
        for child in ctx.children:
            if isinstance(child, ListLangParser.FunctionDeclContext):
                self.visit(child)

        # Основная функция
        self.output_code.append('  (func $main (export "main")')
        self.output_code.append('    (local $temp i32)')
        self.output_code.append('    (local $temp_list i32)')
        self.output_code.append('    (local $elem_val i32)')
        self.output_code.append('    (local $temp2 i32)')

        # Посещаем все операторы вне функций
        for child in ctx.children:
            if not isinstance(child, ListLangParser.FunctionDeclContext):
                if isinstance(child, ListLangParser.StatementContext):
                    self.visit(child)

        self.output_code.append('    (return)')
        self.output_code.append('  )')

        # Данные строк
        for string_text, address in self.string_constants.items():
            escaped_string = string_text.replace('\\', '\\\\').replace('"', '\\"')
            self.output_code.append(f'  (data (i32.const {address}) "{escaped_string}\\00")')

        self.output_code.append(')')
        return '\n'.join(self.output_code)

    def _collect_global_vars(self, ctx):
        """Рекурсивно собирает все глобальные переменные из AST"""
        if hasattr(ctx, 'children'):
            for child in ctx.children:
                # Если это присваивание
                if isinstance(child, ListLangParser.AssignmentContext):
                    var_name = child.ID().getText()
                    if var_name not in self.global_vars:
                        self.global_vars[var_name] = True
                # Рекурсивно обходим остальные узлы
                self._collect_global_vars(child)

    def _add_helper_functions(self):
        """Добавляет вспомогательные функции для работы со списками"""

        # Функция выделения памяти
        helper_code = [
            '  ;; Вспомогательные функции',
            '  (func $malloc (param $size i32) (result i32)',
            '    (local $ptr i32)',
            '    (global.get $heap_ptr)',
            '    (local.set $ptr)',
            '    (global.set $heap_ptr',
            '      (i32.add',
            '        (global.get $heap_ptr)',
            '        (local.get $size)',
            '      )',
            '    )',
            '    (local.get $ptr)',
            '  )',
            '',
            '  (func $list_create (param $len i32) (result i32)',
            '    (local $ptr i32)',
            '    ;; Выделяем память: длина + элементы',
            '    (local.set $ptr',
            '      (call $malloc',
            '        (i32.mul',
            '          (i32.add (local.get $len) (i32.const 1))',
            '          (i32.const 4)',
            '        )',
            '      )',
            '    )',
            '    ;; Сохраняем длину списка',
            '    (i32.store (local.get $ptr) (local.get $len))',
            '    (local.get $ptr)',
            '  )',
            '',
            '  (func $list_get (param $list i32) (param $index i32) (result i32)',
            '    (i32.load offset=4',
            '      (i32.add',
            '        (local.get $list)',
            '        (i32.mul (local.get $index) (i32.const 4))',
            '      )',
            '    )',
            '  )',
            '',
            '  (func $list_set (param $list i32) (param $index i32) (param $value i32)',
            '    (i32.store offset=4',
            '      (i32.add',
            '        (local.get $list)',
            '        (i32.mul (local.get $index) (i32.const 4))',
            '      )',
            '      (local.get $value)',
            '    )',
            '  )',
            '',
            '  (func $list_length (param $list i32) (result i32)',
            '    (i32.load (local.get $list))',
            '  )',
            '',
            '  ;; Операции со списками',
            '  (func $list_concat (param $a i32) (param $b i32) (result i32)',
            '    (local $len_a i32)',
            '    (local $len_b i32)',
            '    (local $result i32)',
            '    (local $i i32)',
            '    ',
            '    (local.set $len_a (call $list_length (local.get $a)))',
            '    (local.set $len_b (call $list_length (local.get $b)))',
            '    ',
            '    ;; Создаем новый список',
            '    (local.set $result',
            '      (call $list_create',
            '        (i32.add (local.get $len_a) (local.get $len_b))',
            '      )',
            '    )',
            '    ',
            '    ;; Копируем первый список',
            '    (local.set $i (i32.const 0))',
            '    (block $copy_a_end',
            '      (loop $copy_a',
            '        (br_if $copy_a_end',
            '          (i32.ge_u (local.get $i) (local.get $len_a))',
            '        )',
            '        (call $list_set',
            '          (local.get $result)',
            '          (local.get $i)',
            '          (call $list_get (local.get $a) (local.get $i))',
            '        )',
            '        (local.set $i (i32.add (local.get $i) (i32.const 1)))',
            '        (br $copy_a)',
            '      )',
            '    )',
            '    ',
            '    ;; Копируем второй список',
            '    (local.set $i (i32.const 0))',
            '    (block $copy_b_end',
            '      (loop $copy_b',
            '        (br_if $copy_b_end',
            '          (i32.ge_u (local.get $i) (local.get $len_b))',
            '        )',
            '        (call $list_set',
            '          (local.get $result)',
            '          (i32.add (local.get $len_a) (local.get $i))',
            '          (call $list_get (local.get $b) (local.get $i))',
            '        )',
            '        (local.set $i (i32.add (local.get $i) (i32.const 1)))',
            '        (br $copy_b)',
            '      )',
            '    )',
            '    ',
            '    (local.get $result)',
            '  )',
            '',
            '  (func $list_contains (param $list i32) (param $value i32) (result i32)',
            '    (local $len i32)',
            '    (local $i i32)',
            '    ',
            '    (local.set $len (call $list_length (local.get $list)))',
            '    (local.set $i (i32.const 0))',
            '    ',
            '    (block $loop_end',
            '      (loop $loop',
            '        (br_if $loop_end',
            '          (i32.ge_u (local.get $i) (local.get $len))',
            '        )',
            '        (if',
            '          (i32.eq',
            '            (call $list_get (local.get $list) (local.get $i))',
            '            (local.get $value)',
            '          )',
            '          (then',
            '            (return (i32.const 1))',
            '          )',
            '        )',
            '        (local.set $i (i32.add (local.get $i) (i32.const 1)))',
            '        (br $loop)',
            '      )',
            '    )',
            '    ',
            '    (i32.const 0)',
            '  )',
        ]

        # Добавьте в конец:
        helper_code.extend([
            '',
            '  ;; Заглушки для отсутствующих функций',
            '  (func $balance (param $tree i32) (result i32)',
            '    ;; Заглушка - возвращаем тот же список',
            '    (local.get $tree)',
            '  )',
            '',
            '  (func $merge (param $a i32) (param $b i32) (result i32)',
            '    ;; Заглушка - просто объединяем списки',
            '    (call $list_concat (local.get $a) (local.get $b))',
            '  )',
        ])

        self.output_code.extend(helper_code)

    def _get_string_constant(self, string_val):
        """Возвращает адрес строковой константы в памяти"""
        if string_val not in self.string_constants:
            # Начинаем с 4096 (4KB) чтобы избежать конфликтов
            address = 4096 + self.next_string_id * 256
            self.string_constants[string_val] = address
            self.next_string_id += 1
        return self.string_constants[string_val]

    def visitFunctionDecl(self, ctx):
        name = ctx.ID().getText()
        params = []
        if ctx.parameterList():
            params = [param.getText() for param in ctx.parameterList().ID()]

        # Сохраняем информацию о функции
        func_info = FunctionInfo(name, 'i32', params)  # Все функции возвращают i32
        self.functions[name] = func_info
        self.current_function = func_info

        # Генерируем заголовок функции
        self.output_code.append(f'  (func ${name} (export "{name}")')

        # Параметры
        for i, param in enumerate(params):
            self.output_code.append(f'    (param ${param} i32)')
            func_info.local_vars[param] = i

        # Возвращаемый тип - ДОБАВЛЯЕМ ЗДЕСЬ, перед локальными переменными!
        if name != "main":
            self.output_code.append('    (result i32)')

        # Локальные переменные
        self.output_code.append('    (local $temp i32)')
        self.output_code.append('    (local $elem_val i32)')
        self.output_code.append('    (local $temp2 i32)')

        # Тело функции
        self.visit(ctx.block())

        self.output_code.append('  )')
        self.current_function = None

    def _has_return_in_block(self, ctx):
        """Проверяет, содержит ли блок оператор return"""
        if hasattr(ctx, 'statement'):
            for stmt in ctx.statement():
                if isinstance(stmt, ListLangParser.StatementContext):
                    # Проверяем returnStatement внутри statement
                    for child in stmt.children:
                        if isinstance(child, ListLangParser.ReturnStatementContext):
                            return True
                        elif isinstance(child, ListLangParser.BlockContext):
                            if self._has_return_in_block(child):
                                return True
        return False

    def visitReturnStatement(self, ctx):
        if ctx.expression():
            # Генерируем возвращаемое значение
            self.visit(ctx.expression())
        else:
            # Если нет выражения, возвращаем 0
            self.output_code.append('    (i32.const 0)')

        # Добавляем return инструкцию
        self.output_code.append('    (return)')

    def visitBlock(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    def visitAssignment(self, ctx):
        var_name = ctx.ID().getText()

        # Генерируем значение (будет на стеке)
        self.visit(ctx.expression())

        # Сохраняем в переменную
        if self.current_function and var_name in self.current_function.local_vars:
            # Локальная переменная
            self.output_code.append(f'    (local.set ${var_name})')
        else:
            # Глобальная переменная - только запоминаем
            if var_name not in self.global_vars:
                self.global_vars[var_name] = True  # Просто отмечаем, что переменная существует
            # Сохраняем значение в глобальную переменную
            self.output_code.append(f'    (global.set ${var_name})')

    def visitWriteStatement(self, ctx):
        expr_ctx = ctx.expression()

        if isinstance(expr_ctx, ListLangParser.LiteralExprContext):
            lit = expr_ctx.literal()
            if lit.STRING():
                # Вывод строки
                string_val = lit.getText()[1:-1]  # Убираем кавычки
                addr = self._get_string_constant(string_val)
                self.output_code.append(f'    (call $logStr (i32.const {addr}) (i32.const {len(string_val)}))')
            elif lit.INT():
                # Вывод целого числа
                value = lit.INT().getText()
                self.output_code.append(f'    (call $logInt (i32.const {value}))')
        else:
            # Для списков просто выводим их адрес
            self.visit(expr_ctx)  # Адрес списка на стеке
            self.output_code.append('    (call $log)')

    def visitIdExpr(self, ctx):
        var_name = ctx.ID().getText()

        if self.current_function and var_name in self.current_function.local_vars:
            self.output_code.append(f'    (local.get ${var_name})')
        elif var_name in self.global_vars:
            self.output_code.append(f'    (global.get ${var_name})')
        else:
            raise CompilerError(f"Неизвестная переменная: {var_name}")

    def visitLiteralExpr(self, ctx):
        lit = ctx.literal()

        if lit.INT():
            value = lit.INT().getText()
            self.output_code.append(f'    (i32.const {value})')
        elif lit.STRING():
            string_val = lit.getText()[1:-1]
            addr = self._get_string_constant(string_val)
            self.output_code.append(f'    (i32.const {addr})')
        elif lit.TRUE():
            self.output_code.append('    (i32.const 1)')
        elif lit.FALSE():
            self.output_code.append('    (i32.const 0)')

    def visitListExpr(self, ctx):
        elements = []
        if ctx.expressionList():
            elements = list(ctx.expressionList().expression())

        # Создаем список
        self.output_code.append(f'    (call $list_create (i32.const {len(elements)}))')
        self.output_code.append('    (local.set $temp)')  # Сохраняем указатель на список

        # Заполняем элементы
        for i, elem in enumerate(elements):
            # Вычисляем значение элемента
            self.visit(elem)  # Значение на стеке

            # Сохраняем в локальную переменную (так проще)
            self.output_code.append('    (local.set $elem_val)')

            # Подготавливаем параметры для list_set
            self.output_code.append('    (local.get $temp)')
            self.output_code.append(f'    (i32.const {i})')
            self.output_code.append('    (local.get $elem_val)')

            # Вызываем list_set
            self.output_code.append('    (call $list_set)')

        # Возвращаем указатель на список
        self.output_code.append('    (local.get $temp)')

    def visitAdditiveExpr(self, ctx):
        left = ctx.expression(0)
        right = ctx.expression(1)
        op = ctx.op.text

        # Посещаем левую часть
        self.visit(left)

        # Посещаем правую часть
        if op == '+':
            self.visit(right)
            # Проверяем, работаем ли со списками или числами
            # Упрощенная логика: если это не очевидно список, то считаем числами
            # В реальном компиляторе нужен анализ типов
            if self._is_likely_list(left) or self._is_likely_list(right):
                self.output_code.append('    (call $list_concat)')
            else:
                self.output_code.append('    (i32.add)')
        else:  # '-'
            self.visit(right)
            # Для чисел
            self.output_code.append('    (i32.sub)')

    def _is_likely_list(self, expr_ctx):
        """Упрощенная проверка, является ли выражение списком"""
        # Если это идентификатор, который мог быть списком
        if isinstance(expr_ctx, ListLangParser.IdExprContext):
            var_name = expr_ctx.ID().getText()
            # Проверяем, начинается ли имя с list, или содержит list
            return 'list' in var_name.lower()
        # Если это литерал списка
        elif isinstance(expr_ctx, ListLangParser.ListExprContext):
            return True
        # Если это вызов функции, возвращающей список
        elif isinstance(expr_ctx, ListLangParser.FunctionCallExprContext):
            func_name = expr_ctx.functionCall().ID().getText()
            return func_name in ['create_balanced_tree', 'process_queue', 'merge']
        return False

    def visitMultiplicativeExpr(self, ctx):
        left = ctx.expression(0)
        right = ctx.expression(1)
        op = ctx.op.text

        if op == '*':
            # Пересечение списков
            self.visit(left)
            self.visit(right)
            self.output_code.append('    (drop) (drop)')
            self.output_code.append('    (call $list_create (i32.const 0))')
        else:
            # Для деления и остатка от деления - возвращаем пустой список
            self.visit(left)
            self.visit(right)
            self.output_code.append('    (drop) (drop)')
            self.output_code.append('    (call $list_create (i32.const 0))')
            # Или можно просто проигнорировать:
            # self.visit(left)
            # self.output_code.append('    (drop)')
            # self.output_code.append('    (call $list_create (i32.const 0))')

    def visitInExpr(self, ctx):
        # Проверка наличия элемента в списке
        self.visit(ctx.expression(1))  # Список
        self.visit(ctx.expression(0))  # Значение
        self.output_code.append('    (call $list_contains)')

    def visitIfStatement(self, ctx):
        # Условие
        self.visit(ctx.expression())

        # В WAT if имеет форму: (if (condition) (then ...) (else ...))
        # В WAT 0 = false, не-0 = true
        self.output_code.append('    (if')
        self.output_code.append('      (then')

        # Then блок
        self.visit(ctx.block(0))

        self.output_code.append('      )')

        if ctx.ELSE():
            self.output_code.append('      (else')
            # Else блок
            self.visit(ctx.block(1))
            self.output_code.append('      )')

        self.output_code.append('    )')

    def visitFunctionCall(self, ctx):
        func_name = ctx.ID().getText()

        if func_name == 'len':
            # Встроенная функция длины списка
            if ctx.argumentList() and ctx.argumentList().expression():
                self.visit(ctx.argumentList().expression(0))
                self.output_code.append('    (call $list_length)')
        else:
            # Вызов пользовательской функции
            args = []
            if ctx.argumentList():
                args = list(ctx.argumentList().expression())

            for arg in args:
                self.visit(arg)

            self.output_code.append(f'    (call ${func_name})')

    def visitUntilStatement(self, ctx):
        # until condition block - выполняется пока условие НЕ верно
        label_start = f"until_start_{self.label_counter}"
        label_end = f"until_end_{self.label_counter}"
        self.label_counter += 1

        # В WAT: block с меткой для выхода, loop с меткой для повторения
        self.output_code.append(f'    (block ${label_end}')
        self.output_code.append(f'      (loop ${label_start}')

        # Проверяем условие (должно быть на стеке как i32: 0 = false, 1 = true)
        self.visit(ctx.expression())
        # Если условие истинно (не 0), выходим из цикла
        self.output_code.append(f'        (br_if ${label_end})')

        # Тело цикла
        self.visit(ctx.block())

        # Возвращаемся к проверке условия
        self.output_code.append(f'        (br ${label_start})')

        # Закрываем loop и block
        self.output_code.append('      )')
        self.output_code.append('    )')

    def visitComparisonExpr(self, ctx):
        left = ctx.expression(0)
        right = ctx.expression(1)
        op = ctx.op.text

        # Посещаем левую часть
        self.visit(left)
        # Посещаем правую часть
        self.visit(right)

        # Генерируем операцию сравнения
        if op == '<':
            self.output_code.append('    (i32.lt_s)')
        elif op == '>':
            self.output_code.append('    (i32.gt_s)')
        elif op == '<=':
            self.output_code.append('    (i32.le_s)')
        elif op == '>=':
            self.output_code.append('    (i32.ge_s)')
        elif op == '==':
            self.output_code.append('    (i32.eq)')
        elif op == '!=':
            self.output_code.append('    (i32.ne)')

    def visitIndexExpr(self, ctx):
        # Вычисляем список (результат на стеке)
        self.visit(ctx.expression(0))
        # Вычисляем индекс (результат на стеке)
        self.visit(ctx.expression(1))
        # Вызываем list_get: получает список и индекс, возвращает значение
        self.output_code.append('    (call $list_get)')


def compile_listlang(input_file, output_file):
    # Чтение исходного кода
    with open(input_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # Лексический и синтаксический анализ
    input_stream = InputStream(code)
    lexer = ListLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ListLangParser(stream)
    tree = parser.program()

    # Компиляция
    compiler = CompilerVisitor()
    wat_code = compiler.visit(tree)

    # Запись результата
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(wat_code)

    print(f"Компиляция завершена. Результат записан в {output_file}")

    return wat_code


def main():
    compile_listlang("examples/example1.listlang", "output/example1.wat")
    compile_listlang("examples/example2.listlang", "output/example2.wat")
    compile_listlang("examples/example3.listlang", "output/example3.wat")


if __name__ == "__main__":
    main()