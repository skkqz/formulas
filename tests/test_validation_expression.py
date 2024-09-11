from unittest import TestCase
from validation import ValidateExpression


class TestValidateExpression(TestCase):
    """
    Класс для тестирования ValidateExpression.
    """

    def setUp(self):
        """
        Создаём объект ValidateExpression перед каждым тестом.
        """
        self.validator = ValidateExpression()

    def test_valid_expression(self):
        """
        Тестирование корректных выражений
        :return:
        """

        valid_expression = [
            '3 + 2',
            '3 + 2 - 1',
            '3 + 2 + (2 * 15)',
            '(10 / 2) + 5 * 5',
            '(3 + 2) - (2 * (8 + 2))',
            '3 + 2 ** 2',
            '-3 + 2 ** 2',
            '3 + -(2 ** 2)',
        ]

        for exper in valid_expression:
            with self.subTest(exper=exper):
                self.assertEqual(
                    self.validator.valid_expression(exper),
                    exper.replace(' ', '').replace(',', '.')
                )

    def test_invalid_two_operators_nearby(self):
        """
        Тестирование выражений с некорректными операторами подряд
        """

        invalid_expressions = [
            "3 + 5 ** + 2",
            "4 // * 2",
            "2 *** 3",
            "5 -+ 3",
            "--5 -+ 3",
            "+5 -+ 3",
        ]

        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(SyntaxError):
                    self.validator.valid_expression(expr)

    def test_invalid_parentheses(self):
        """
        Тестирование выражений с некорректными скобками
        """

        invalid_expressions = [
            "3 + (2 * 3",
            "2 * 3)",
            "((5 + 3)",
        ]

        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(SyntaxError):
                    self.validator.valid_expression(expr)

    def test_invalid_beginning_of_expression(self):
        """
        Тестирование выражений с ошибкой в начале
        """

        invalid_expressions = [
            "++3 + 5",
            "*3 + 5",
            "/2 * 3",
            "--2 * 3",
            ".2 * 3",
        ]
        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(SyntaxError):
                    self.validator.valid_expression(expr)

    def test_invalid_float_numbers(self):
        """
        Тестирование выражений с некорректными числами с плавающей точкой
        """

        invalid_expressions = [
            "3.2.3 + 5",
            "5 + 2..5",
            "5 + .",
            ".5 + .",
            "..2 + .",
        ]
        for expr in invalid_expressions:
            with self.subTest(expr=expr):
                with self.assertRaises(SyntaxError):
                    self.validator.valid_expression(expr)