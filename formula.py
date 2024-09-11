import operator
import re
from typing import List

from validation import ValidateExpression


class CalculationOfMathematicalExpression:
    """Класс для расчёта математических формул"""

    def __init__(self):
        self.operators = {
            '+': (1, operator.add),
            '-': (1, operator.sub),
            '*': (2, operator.mul),
            '/': (2, operator.truediv),
            '**': (2, operator.pow),
            '//': (2, operator.floordiv),
        }
        self.validate = ValidateExpression()

    def evaluate(self, expression: str) -> float:
        """
        Вычисление значений мат. выражения.

        @param expression (str): Математическое выражение в виде строки.
        @return (float): Результат решения формулы.
        """

        expression = self.validate.valid_expression(expression)
        tokens = self._tokenize(expression)
        postfix = self._to_postfix(tokens)
        result = self._calculate_postfix(postfix, expression)

        return result

    @staticmethod
    def is_number(string: str):
        """
        Проверка является строка числом.

        @param string (str): Число в виде строки
        @return:
        """

        pattern_int_float = r'^-?\d+(\.\d+)?$'

        return bool(re.match(pattern_int_float, string))


    @staticmethod
    def _tokenize(expression: str) -> List[str]:
        """
        Разбиваем строковое выражение на список токенов: числа, операторы, скобки.

        @param expression (str): Строка с мат. выражением.
        @return (list): Список токенов (чиста, операторы и т.д.)

        Привер:
        Для выражения "3+5*(2-1)" результат будет ['3', '+', '5', '*', '(', '2', '-', '1', ')']
        """

        tokens = []
        value = []
        prev_item = None

        for item in expression:
            if item.isdigit() or item == '.':
                value.append(item)
            elif item.isalpha():
                continue
            else:
                if value:
                    tokens.append(''.join(value))
                    value.clear()

                # Обрабатываем унарный минус и скобки
                if item == '-' and (prev_item is None or prev_item in '*/+-('):
                    # Если минус идёт после оператора или скобки, начинаем формировать отрицательное число.
                    value.append(item)
                elif item == '(' and tokens and tokens[-1] == '-':
                    # Унарный минус перед скобкой
                    tokens.pop()
                    tokens.append('(-')
                elif tokens and tokens[-1] == '*' and item == '*':
                    tokens.pop()
                    tokens.append('**')
                elif tokens and tokens[-1] == '/' and item == '/':
                    tokens.pop()
                    tokens.append('//')
                else:
                    tokens.append(item)

            prev_item = item

        if value:
            tokens.append(''.join(value))

        print(tokens)
        return tokens


    def _to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Преобразует инфиксное выражение в постфиксную запись (обратная польская запить).

        "Постфиксная запись (обратная польская запись) - это способ записи математических выражения,
        при котором операторы располагаются после операндов, в отличие от традиционной инфиксной записи,
        где операторы размещаются между операндами. Преимущество
        постфиксной записи в том, что она не требует скобок для обозначения приоритета операций - приоритет определяется
        порядком появления операторов и операндов."

        @param tokens (list): Список токенов (чисел, операторов и т.д.).
        @return (list): Список токенов в постфиксной записи.

        Пример:
        Для выражения ['3', '+', '5', '*', '2'] результат будет ['3','5', '2', '*', '+']
        """

        output = []
        operators = []

        for token in tokens:
            if self.is_number(token):

                # Если токен - число, добавляем его в результат.
                output.append(token)

            elif token in self.operators:

                # Если токен - оператор, обрабатываем его по приоритету.
                while (
                        operators and operators[-1] in self.operators
                        and self.operators[token][0] <=
                        self.operators[operators[-1]][0]
                ):

                    # Пока в стеке есть операторы с таким же или большим приоритетом, перемещаем их в выходную строку
                    output.append(operators.pop())
                operators.append(token)

            elif token == '(':
                operators.append(token)

            elif token == '(-':
                # Обработка унарного минуса перед скобкой
                output.append('-1')
                operators.append('*')
                operators.append('(')

            elif token == ')':
                # Закрывающая скобка: выталкиваем все операторы до открывающей скобки.
                while operators and operators[-1] != '(':
                    output.append(operators.pop())

                # Убираем '(' из стека.
                operators.pop()

        # Перемещаем оставшиеся операторы из стека в выходную строку.
        while operators:
            output.append(operators.pop())

        return output


    def _calculate_postfix(self, postfix: List[str], e) -> float:
        """
        Вычисляет значение выражения, представленного в постфиксной записи.

        @param postfix (list): Список токенов в постфиксной записи (обратной польской записи).
        @return: Числовой результат вычисления.
        """

        stack = []  # Стек для промежуточных вычислений

        for token in postfix:

            if self.is_number(token):
                stack.append(float(token))

            elif token in self.operators and len(stack) > 1:

                # Если торен - оператор, извлекаем два числа из стека.
                right = stack.pop()
                left = stack.pop()

                # выполняем операцию и кладём результат обратно в стек.
                operation = self.operators[token][1]
                stack.append(operation(left, right))

        # Окончательный результат будет единственным элементом в стеке.
        return stack[0]


test = CalculationOfMathematicalExpression()
# print(test.evaluate('3.5 + 3 - 6'))

# data = [
#     ('3 + 3 - 6', True),
#     ('6.5 // 2', True),
#     ('3 +2 ** 6', True),
#     ('3 +- 3', True),
    # ('(2**4) + 3.4 // 6', True),
    # ('2 + (3 * 5 + (2 -8)) // 2 * 6', True),
    # ('(2 + 3 + ((23 + 7)))', True),
    # ('-3 + -2 - 4', True),
    # ('-(3 + -2) - 4', True),
    # ('-(3 + -(2+2) // -2) - 4', True),
    # ('(-(3 + -(2+2)) // -2) - 4', True),
    # ('3.5 + 3,4', True),
    # ('3.7 + 3,4 - 23 ** 8.8', True),
    # ('3.5 + (-3 + 2.3)', True),

    # ('2.54 + 2223.6 + 322.23.344 - .5 - -4.5 + .3.3 - ..33', False),
    # ('-*(3 + -2) - 4', False),
    # ('3.5 + (-3 + 23.4 - .3.2.3)', False),
    # ('(.0 - 2)', False),
    # ('3.5 + (-5. + 23.4 - .3.2)', False),
    # ('--(3 + -2) - 4', False),
    # ('+(3 + -2) - 4', False),
    # ('(////)', False),
    # ('.2.54 + 2223.6 + 322.23.344 - .5 - -4.5 + .3.3 - ..33', False),
    # ('3 ** / 3 + 6', False),
    # ('--3 + -2 - 4', False),
    # ('+3 + -2 - 4', False),
    # ('3 -+ 3 - 6', False),
    # ('3 /// 3 ** 6', False),
    # ('(2 + 3 + ((23 + 7))', False),
    # ('(2+1 ** 3) + (2 +3', False),
# ]


expressions_with_answers = [
    ("3 + 5 * 2", 13),                     # 3 + 5 * 2 = 13
    ("(4 - 2) * 6 / 2", 6.0),               # (4 - 2) * 6 / 2 = 6.0
    ("10 / 2 + 3 * (2 + 1)", 14.0),         # 10 / 2 + 3 * (2 + 1) = 14.0 (ранее было неверно)
    ("5 + (3 * 2) - 8", 3),                 # 5 + (3 * 2) - 8 = 3
    ("-5 + 3 * 2", 1),                      # -5 + 3 * 2 = 1
    ("4 * (3 + 2) - (6 / 3)", 18.0),        # 4 * (3 + 2) - (6 / 3) = 18.0
    ("2 ** 3 + 5", 13),                     # 2 ** 3 + 5 = 13
    ("6 // 4 * 3 + 1", 4),                  # 6 // 4 * 3 + 1 = 4
    ("(3 + 5) * (2 + 1)", 24),              # (3 + 5) * (2 + 1) = 24
    ("7 + -(3 - 4)", 8),                    # 7 + -(3 - 4) = 8
    ("10 / (2 + 3)", 2.0),                  # 10 / (2 + 3) = 2.0
    ("-4 + 6 * 2", 8),                      # -4 + 6 * 2 = 8
    ("(2 ** 3) * 2 + 5", 21),               # (2 ** 3) * 2 + 5 = 21
    ("100 // 3 * 2", 66),                   # 100 // 3 * 2 = 66
    ("(7 - 5) * (3 + 4)", 14),              # (7 - 5) * (3 + 4) = 14
    ("5 + 5 * 5 - 10", 20),                 # 5 + 5 * 5 - 10 = 20
    ("(9 / 3) + (2 * 3)", 9.0),             # (9 / 3) + (2 * 3) = 9.0
    ("-10 + 4 * 2", -2),                    # -10 + 4 * 2 = -2
    ("8 ** 2 / 4", 16.0),                   # 8 ** 2 / 4 = 16.0
    ("(5 + 3) ** 2", 64),                   # (5 + 3) ** 2 = 64
]

for i in expressions_with_answers:

    try:
        x = test.evaluate(i[0])
        print(f'Выражение верное: {i} ----> result: {x} | {i[1]}')
    except SyntaxError as ex:
        print(f'Ошибка: Выражение не верное: {i} - {ex}')
