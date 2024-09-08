import operator
from typing import List


class ExpressionEvaluator:
    """
    Класс для вычисления выражения
    """

    def __init__(self):

        # Поддерживаемые операции
        self.operators = {
            '+': (1, operator.add),
            '-': (1, operator.sub),
            '*': (1, operator.mul),
            '/': (1, operator.truediv),
        }


    def evaluate(self, expression):
        """
        Вычисляет значение переданного математического выражения.
        :param expression: Математическое выражение в виде строки
        :return: Результат решения формулы
        """

        # Убираем пробелы из выражения
        expression = expression.replace(' ', '')

        # Преобразуем выражение в список токенов (числа, операторы, сборки)
        tokens = self.tokenize(expression)

        # Преобразуем токены в постфиксную запись
        postfix = self.to_postfix(tokens)

        # Преобразуем значения выражения в постфиксной записи
        return self.calculate_postfix(postfix)


    def tokenize(self, expression: str) -> List[str]:
        """
        Разбивает строковое выражение на список токенов: числа, операторы и скобки.

        :param expression:  Строка с выражением для разбиения.
        :return:  Список токенов (числа и операторы).

        Пример:
        Для выражения "3+5*(2-1)" результат будет ['3', '+', '5', '*', '(', '2', '-', '1', ')']
        """

        tokens = []
        value = ''


        for char in expression:

            if char.isdigit():
                value += char
            else:
                if value:
                    tokens.append(value)
                    value = ''
                tokens.append(char)

        if value:
            tokens.append(value)

        return tokens

    def to_postfix(self, tokens: List[str]) -> List[str]:
        """
        Преобразует инфиксное выражение в постфиксную запись (обратная польская запись).

        :param tokens : Список токенов (чисел и операторов).
        :return: Список токенов в постфиксной записи.

        Пример:
        Для выражения ['3', '+', '5', '*', '2'] результат будет ['3', '5', '2', '*', '+']
        """

        output = []
        operators = []

        for token in tokens:

            if token.isdigit():
                output.append(token)
            elif token in self.operators:
                # Выводим оператор по приоритету
                while (
                        operators and operators[-1] in self.operators
                        and self.operators[token][0] <= self.operators[operators[-1]][0]
                ):
                    output.append(operators.pop())
                operators.append(token)

            elif token == '(':
                operators.append(token)

            elif token == ')':
                while operators and operators[-1] != '(':

                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        return output

    def calculate_postfix(self, postfix):
        """
        Вычисляет значение выражения, представленного в постфиксной записи.

        :param postfix: Список токенов в постфиксной записи (обратной польской записи).
        :return: Числовой результат вычисления.

        Пример:
        Для постфиксной записи ['3', '5', '2', '*', '+'] результат будет 13.
        """

        stack = []

        for token in postfix:

            if token.isdigit():
                stack.append(int(token))
            elif token in self.operators:
                right = stack.pop()
                left = stack.pop()
                operation = self.operators[token][1]
                stack.append(operation(left, right))

        print(stack)
        return stack[0]


test = ExpressionEvaluator()
# test.to_postfix(['(', '3', '+', '5', ')',  '*', '2'])
print(test.calculate_postfix(['3', '5', '2', '*', '+']))

# print(test.tokenize('8+ 2='.replace(' ', '')))