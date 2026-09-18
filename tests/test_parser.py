import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer import Lexer, LexicalError
from parser import Parser, ParseError


def run_pipeline(query):
    tokens = Lexer(query).tokenize()
    return Parser(tokens).parse()


class ValidQueryTests(unittest.TestCase):
    def test_simple_select(self):
        self.assertTrue(run_pipeline("SELECT name FROM employee;"))

    def test_multiple_columns(self):
        self.assertTrue(run_pipeline("SELECT name, salary FROM employee;"))

    def test_where_with_comparison(self):
        self.assertTrue(run_pipeline("SELECT name FROM employee WHERE salary > 50000;"))

    def test_where_with_logical_operator(self):
        self.assertTrue(
            run_pipeline(
                "SELECT name FROM employee WHERE salary >= 50000 AND department = 'IT';"
            )
        )


class InvalidQueryTests(unittest.TestCase):
    def test_missing_column(self):
        with self.assertRaises(ParseError):
            run_pipeline("SELECT FROM employee;")

    def test_missing_from(self):
        with self.assertRaises(ParseError):
            run_pipeline("SELECT name employee;")

    def test_missing_table_name(self):
        with self.assertRaises(ParseError):
            run_pipeline("SELECT name FROM;")

    def test_incomplete_where(self):
        with self.assertRaises(ParseError):
            run_pipeline("SELECT name FROM employee WHERE;")

    def test_malformed_operator(self):
        with self.assertRaises(ParseError):
            run_pipeline("SELECT name FROM employee WHERE salary >;")


class LexicalErrorTests(unittest.TestCase):
    def test_unsupported_character(self):
        with self.assertRaises(LexicalError):
            run_pipeline("SELECT name FROM employee WHERE salary @ 50000;")


if __name__ == "__main__":
    unittest.main()
