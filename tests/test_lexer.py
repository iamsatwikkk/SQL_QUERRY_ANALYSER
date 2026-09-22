import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer import Lexer, LexicalError
from tokens import TokenType


class LexerTokenClassificationTests(unittest.TestCase):
    def test_keyword_and_identifier_classification(self):
        tokens = Lexer("SELECT name FROM employee;").tokenize()
        types = [token.type for token in tokens if token.type != TokenType.EOF]
        self.assertEqual(
            types,
            [
                TokenType.KEYWORD,
                TokenType.IDENTIFIER,
                TokenType.KEYWORD,
                TokenType.IDENTIFIER,
                TokenType.SEMICOLON,
            ],
        )

    def test_number_literal(self):
        tokens = Lexer("SELECT name FROM employee WHERE salary > 50000;").tokenize()
        number_token = next(token for token in tokens if token.type == TokenType.NUMBER)
        self.assertEqual(number_token.value, "50000")

    def test_string_literal(self):
        tokens = Lexer("SELECT name FROM employee WHERE department = 'IT';").tokenize()
        string_token = next(token for token in tokens if token.type == TokenType.STRING)
        self.assertEqual(string_token.value, "IT")

    def test_comparison_operators(self):
        for operator in ("=", ">", "<", ">=", "<="):
            tokens = Lexer(f"SELECT name FROM employee WHERE salary {operator} 1;").tokenize()
            operator_token = next(token for token in tokens if token.type == TokenType.OPERATOR)
            self.assertEqual(operator_token.value, operator)

    def test_line_and_column_tracking(self):
        tokens = Lexer("SELECT name\nFROM employee;").tokenize()
        from_token = next(token for token in tokens if token.value == "FROM")
        self.assertEqual(from_token.line, 2)
        self.assertEqual(from_token.column, 1)


class LexicalErrorTests(unittest.TestCase):
    def test_unexpected_character(self):
        with self.assertRaises(LexicalError):
            Lexer("SELECT name FROM employee WHERE salary @ 50000;").tokenize()

    def test_unterminated_string(self):
        with self.assertRaises(LexicalError):
            Lexer("SELECT name FROM employee WHERE department = 'IT;").tokenize()

    def test_error_reports_position(self):
        try:
            Lexer("SELECT name FROM employee WHERE salary @ 50000;").tokenize()
            self.fail("Expected a LexicalError to be raised")
        except LexicalError as error:
            self.assertEqual(error.line, 1)
            self.assertEqual(error.column, 40)


if __name__ == "__main__":
    unittest.main()
