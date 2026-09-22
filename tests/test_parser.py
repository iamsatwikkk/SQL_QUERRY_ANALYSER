import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from lexer import Lexer
from parser import Parser, ParseError
from ast_nodes import SelectStatement, Comparison, LogicalCondition, format_ast


def parse_query(query):
    tokens = Lexer(query).tokenize()
    return Parser(tokens).parse()


class ValidQueryParsingTests(unittest.TestCase):
    def test_simple_select_returns_ast(self):
        statement = parse_query("SELECT name FROM employee;")
        self.assertIsInstance(statement, SelectStatement)
        self.assertEqual([column.name for column in statement.columns], ["name"])
        self.assertEqual(statement.table.name, "employee")
        self.assertIsNone(statement.where)

    def test_multiple_columns(self):
        statement = parse_query("SELECT name, salary FROM employee;")
        self.assertEqual([column.name for column in statement.columns], ["name", "salary"])

    def test_where_with_comparison(self):
        statement = parse_query("SELECT name FROM employee WHERE salary > 50000;")
        self.assertIsInstance(statement.where.condition, Comparison)
        self.assertEqual(statement.where.condition.column.name, "salary")
        self.assertEqual(statement.where.condition.operator, ">")
        self.assertEqual(statement.where.condition.value.value, "50000")

    def test_where_with_logical_operator(self):
        statement = parse_query(
            "SELECT name FROM employee WHERE salary >= 50000 AND department = 'IT';"
        )
        self.assertIsInstance(statement.where.condition, LogicalCondition)
        self.assertEqual(statement.where.condition.operator, "AND")

    def test_ast_display_structure(self):
        statement = parse_query("SELECT name FROM employee WHERE salary > 50000;")
        tree_text = format_ast(statement)
        self.assertIn("SELECT", tree_text)
        self.assertIn("COLUMNS", tree_text)
        self.assertIn("WHERE", tree_text)
        self.assertIn("salary", tree_text)


class InvalidQuerySyntaxTests(unittest.TestCase):
    def test_missing_column(self):
        with self.assertRaises(ParseError):
            parse_query("SELECT FROM employee;")

    def test_missing_from(self):
        with self.assertRaises(ParseError):
            parse_query("SELECT name employee;")

    def test_missing_table_name(self):
        with self.assertRaises(ParseError):
            parse_query("SELECT name FROM;")

    def test_incomplete_where(self):
        with self.assertRaises(ParseError):
            parse_query("SELECT name FROM employee WHERE;")

    def test_malformed_operator(self):
        with self.assertRaises(ParseError):
            parse_query("SELECT name FROM employee WHERE salary >;")

    def test_trailing_tokens_after_semicolon(self):
        with self.assertRaises(ParseError):
            parse_query("SELECT name FROM employee; EXTRA")


if __name__ == "__main__":
    unittest.main()
