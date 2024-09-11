import operator
from typing import List

class ExpressionEvaluator:
    """
    Класс для вычисления математических выражений с поддержкой операций +, -, *, / и скобок.
    """

    def __init__(self):
        """
        Инициализирует поддерживаемые операции и их приоритеты.
        Операторы представлены в виде словаря, где ключ - это оператор,
        а значение - кортеж с приоритетом и функцией из модуля operator.
        """

        # Поддерживаемые операции и их приоритеты.
        # Приоритет операций: '+' и '-' имеют одинаковый приоритет, '*' и '/' также имеют одинаковый.
        self.operators = {
            '+': (1, operator.add),
            '-': (1, operator.sub),
            '*': (2, operator.mul),
            '/': (2, operator.truediv)
        }

    def evaluate(self, expression: str) -> float:
        """
        Вычисляет значение переданного математического выражения.

        :param expression: Математическое выражение в виде строки
        :return: Результат решения формулы
        """

        # Убираем пробелы из выражения для корректной работы токенизатора.
        expression = expression.replace(' ', '')

        # Преобразуем выражение в список токенов (числа, операторы, скобки).
        tokens = self.tokenize(expression)

        # Преобразуем токены в постфиксную запись (обратную польскую запись, RPN).
        postfix = self.to_postfix(tokens)

        # Вычисляем значение выражения в постфиксной записи.
        return self.calculate_postfix(postfix)

    def tokenize(self, expression: str) -> List[str]:
        """
        Разбивает строковое выражение на список токенов: числа, операторы и скобки.

        :param expression: Строка с выражением для разбиения.
        :return: Список токенов (числа и операторы).

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
        Преобразует инфиксное выражение в постфиксную запись (обратную польскую запись).

        'Постфиксная запись (обратная польская запись) — это способ записи математических выражений,
         при котором операторы располагаются после операндов, в отличие от традиционной инфиксной записи,
          где операторы размещаются между операндами. Преимущество постфиксной записи в том,
          что она не требует скобок для обозначения приоритета операций
           — приоритет определяется порядком появления операторов и операндов.'

        :param tokens: Список токенов (чисел и операторов).
        :return: Список токенов в постфиксной записи.

        Пример:
        Для выражения ['3', '+', '5', '*', '2'] результат будет ['3', '5', '2', '*', '+']
        """

        output = []
        operators = []

        for token in tokens:
            if token.isdigit():
                # Если токен — число, добавляем его в результат.
                output.append(token)
            elif token in self.operators:
                # Если токен — оператор, обрабатываем его по приоритету.
                while (
                    operators and operators[-1] in self.operators
                    and self.operators[token][0] <= self.operators[operators[-1]][0]
                ):
                    # Пока в стеке есть операторы с таким же или большим приоритетом,
                    # перемещаем их в выходную строку.
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                # Закрывающая скобка: выталкиваем все операторы до открывающей скобки.
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                # Убираем '(' из стека.
                operators.pop()

        # Перемещаем оставшиеся операторы из стека в выходную строку.
        while operators:
            output.append(operators.pop())
        print(output)
        return output

    def calculate_postfix(self, postfix: List[str]) -> float:
        """
        Вычисляет значение выражения, представленного в постфиксной записи.

        :param postfix: Список токенов в постфиксной записи (обратной польской записи).
        :return: Числовой результат вычисления.

        Пример:
        Для постфиксной записи ['3', '5', '2', '*', '+'] результат будет 13.
        """

        stack = []  # Стек для промежуточных вычислений

        for token in postfix:
            if token.isdigit():
                stack.append(int(token))
            elif token in self.operators:
                # Если токен — оператор, извлекаем два числа из стека.
                right = stack.pop()  # Второй операнд
                left = stack.pop()  # Первый операнд
                # Выполняем операцию и кладем результат обратно в стек.
                operation = self.operators[token][1]
                stack.append(operation(left, right))
        # Окончательный результат будет единственным элементом в стеке.
        return stack[0]

