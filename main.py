# import re
# from abc import ABC, abstractmethod
#
#
# # Класс ExpressionEvaluator - основной класс для вычисления выражения
# class ExpressionEvaluator:
#     def __init__(self, tokenizer, parser):
#         self.tokenizer = tokenizer  # Отвечает за разбиение выражения на токены
#         self.parser = parser  # Отвечает за вычисление выражения
#
#     def evaluate(self, expression):
#         tokens = self.tokenizer.tokenize(expression)
#         result = self.parser.parse(tokens)
#         return result
#
#
# # Интерфейс для работы с токенизацией
# class Tokenizer(ABC):
#     @abstractmethod
#     def tokenize(self, expression):
#         pass
#
#
# # Интерфейс для работы с парсингом
# class Parser(ABC):
#     @abstractmethod
#     def parse(self, tokens):
#         pass
#
#
# # Реализация Tokenizer для математических выражений
# class MathTokenizer(Tokenizer):
#     def tokenize(self, expression):
#         # Убираем пробелы и возвращаем выражение как список символов/операндов
#         return [char for char in expression if char != ' ']
#
#
# # Реализация Parser для математических выражений
# class MathParser(Parser):
#     def precedence(self, op):
#         # Определение приоритета операторов
#         if op in ('+', '-'):
#             return 1
#         if op in ('*', '/'):
#             return 2
#         return 0
#
#     def apply_operator(self, operators, values):
#         # Применение операции с двумя операндами
#         operator = operators.pop()
#         right = values.pop()
#         left = values.pop()
#
#         if operator == '+':
#             values.append(left + right)
#         elif operator == '-':
#             values.append(left - right)
#         elif operator == '*':
#             values.append(left * right)
#         elif operator == '/':
#             values.append(left / right)
#
#     def greater_precedence(self, op1, op2):
#         # Проверка приоритета операторов
#         return self.precedence(op1) > self.precedence(op2)
#
#     def parse(self, tokens):
#         values = []
#         operators = []
#         i = 0
#         while i < len(tokens):
#             if tokens[i] == '(':
#                 operators.append(tokens[i])
#             elif tokens[i] == ')':
#                 while operators and operators[-1] != '(':
#                     self.apply_operator(operators, values)
#                 operators.pop()  # Убираем '('
#             elif tokens[i].isdigit():
#                 # Работа с многоразрядными числами
#                 j = i
#                 while j < len(tokens) and tokens[j].isdigit():
#                     j += 1
#                 values.append(int(''.join(tokens[i:j])))
#                 i = j - 1
#             elif tokens[i] in '+-*/':
#                 while (operators and operators[-1] in '+-*/' and
#                        self.greater_precedence(operators[-1], tokens[i])):
#                     self.apply_operator(operators, values)
#                 operators.append(tokens[i])
#             i += 1
#
#         while operators:
#             self.apply_operator(operators, values)
#
#         return values[0]
#
#
# # Пример использования
# if __name__ == "__main__":
#     expression = "(7 + 3) * 9 + ((10 + 10) * 2)"
#     tokenizer = MathTokenizer()
#     parser = MathParser()
#
#     evaluator = ExpressionEvaluator(tokenizer, parser)
#     test = input('Введите формулу: ')
#     result = evaluator.evaluate(test)
#     print(f"Результат: {result}")

import operator


# Основной класс для вычисления выражений
class ExpressionEvaluator:
    def __init__(self):
        # Поддерживаемые операции
        self.operators = {
            '+': (1, operator.add),
            '-': (1, operator.sub),
            '*': (2, operator.mul),
            '/': (2, operator.truediv)
        }

    def evaluate(self, expression):
        # Убираем пробелы из выражения
        expression = expression.replace(' ', '')
        # Преобразуем выражение в список токенов (числа, операторы, скобки)
        tokens = self.tokenize(expression)
        # Преобразуем токены в постфиксную запись
        postfix = self.to_postfix(tokens)
        # Вычисляем значение выражения в постфиксной записи
        return self.calculate_postfix(postfix)

    def tokenize(self, expression):
        """Разделяем строку на числа, операторы и скобки"""
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

    def to_postfix(self, tokens):
        """Преобразуем выражение в постфиксную запись (Обратная польская запись - RPN)"""
        output = []
        operators = []

        for token in tokens:
            if token.isdigit():
                output.append(token)
            elif token in self.operators:
                # Выводим операторы по приоритету
                while (operators and operators[-1] in self.operators and
                       self.operators[token][0] <= self.operators[operators[-1]][0]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Убираем '('

        # Переносим оставшиеся операторы в выходную строку
        while operators:
            output.append(operators.pop())

        return output

    def calculate_postfix(self, postfix):
        """Вычисляем значение выражения в постфиксной записи"""
        stack = []

        for token in postfix:
            if token.isdigit():
                stack.append(int(token))
            elif token in self.operators:
                right = stack.pop()
                left = stack.pop()
                operation = self.operators[token][1]
                stack.append(operation(left, right))

        return stack[0]


# Пример использования
if __name__ == "__main__":
    # expression = "(7 + 3) * 9 + ((10 + 10) * 2)"

    evaluator = ExpressionEvaluator()
    expression = input('Введите формулу: ')
    result = evaluator.evaluate(expression)

    print(f"Результат: {result}")
