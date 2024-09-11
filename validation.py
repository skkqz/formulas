import re
from typing import List


class ValidateExpression:
    """Класс для проверки валидности математического выражения"""

    def __init__(self):
        # Разрешенные операторы
        self.allowed_operators = [
            '+',
            '-',
            '*',
            '/',
            '**',
            '//',
        ]
        self.double_operator = ['**', '//']

    def valid_expression(self, expression: str) -> str | SyntaxError:
        """
        Проверка валидности математического выражения.

        @param expression: Математическое выражение в виде строки.
        @return: True or SyntaxError
        """

        expression = expression.replace(' ', '')
        expression = expression.replace(',', '.')

        self.check_two_operators_nearby(expression)
        self.check_opening_and_closing_parentheses(expression)
        self.check_the_beginning_of_expression(expression)
        self.check_float_numbers(expression)

        return expression

    def check_two_operators_nearby(self, expression: str) -> str | SyntaxError:
        """
        Проверка двух операторов подряд.

        @param expression (str): Математическое выражение в виде строки.
        @return: expression or SyntaxError

        Пример:
        3 + 2 - (2 ** + 2) -> SyntaxError
        Если в выражении попадаются подряд два оператора +-, --, ***,
        //+ и т.д. то будет исключение SyntaxError
    """

        pattern_two_operators = r'([\+\-\*/%]{2,})'
        search_two_operators = re.findall(pattern_two_operators, expression)

        if search_two_operators:

            for operators in search_two_operators:
                if operators not in self.double_operator and operators[-1] != '-':
                    raise SyntaxError(f'Ошибка: два оператора подряд не могут быть в выражении.'
                                      f' {expression} - {operators}')

        return expression


    @staticmethod
    def check_opening_and_closing_parentheses(expression: str) -> str | SyntaxError:
        """
        Проверка на открывающиеся и закрывающиеся скобки в
        математическом выражении.

        @param expression (str): Математическое выражение в виде строки.
        @return: expression or SyntaxError

        Привер:
        Если в выражение нет закрытой скобки 3 + 2 / (2 ** 2 , то будет
        вызвано исключение SyntaxError.
        """

        if expression.count('(') != expression.count(')'):
            raise SyntaxError(f'Ошибка: количество открывающихся и закрывающихся скобок не равны. {expression}')

        return expression

    @staticmethod
    def check_the_beginning_of_expression(expression: str) -> str | SyntaxError:
        """
        Проверка начала выражения. Выражение может начинаться с (,-, число.

        @param expression (str): Математическое выражение в виде строки.
        @return: expression or SyntaxError

        Пример:
        Если выражение начинается --3 + 2, то будет исключение SyntaxError
        """

        pattern = re.compile(r'^(-?\d+|\(-?\d+|-?\()')

        if not pattern.search(expression):
            raise SyntaxError(f'Ошибка: в начале выражение есть ошибка. Проверьте правильность выражения: {expression}')

        return expression


    @staticmethod
    def check_float_numbers(expression: str) -> str | SyntaxError:
        """
        Проверка числа с плавающей точной.

        @param expression (str): Математическое выражение в виде строки.
        @return: expression or SyntaxError

        Пример:
        Если float число будет 3.2.3, то будет исключение SyntaxError
        """

        pattern = r'(?<![\d)])(\.\d+|\d+\.\d+)(?![\d(])|(\.\D)|(\D\.)'

        if re.findall(pattern, expression):
            raise SyntaxError(f'Ошибка: не правильное число с плавающей точкой: {expression}')

        return expression
