import sqlite3

from lexer import Lexer, LexicalError
from parser import Parser, ParseError
from tokens import TokenType
from ast_nodes import format_ast
from schema import Schema, create_sample_database
from semantic import SemanticAnalyzer, SemanticError
from ir import build_ir, render_ir
from optimizer import optimize
from execution_plan import render_execution_plan, render_execution_summary


def print_header(title):
    print(title)
    print()


def format_tokens(tokens):
    lines = []
    for token in tokens:
        if token.type == TokenType.EOF:
            continue
        lines.append(f"{token.value:<12} {token.type.name}")
    return "\n".join(lines)


def format_optimization_steps(steps):
    blocks = []
    for step in steps:
        status = "applied" if step.applied else "not applied"
        lines = [f"Rule: {step.rule}", f"Status: {status}", f"Reason: {step.reason}"]
        if step.applied:
            lines.append(f"Before: {step.before}")
            lines.append(f"After: {step.after}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def format_result_rows(columns, rows):
    if not rows:
        return "No matching rows in the sample dataset."
    widths = [len(column) for column in columns]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))
    header = "  ".join(column.ljust(widths[index]) for index, column in enumerate(columns))
    lines = [header]
    for row in rows:
        lines.append("  ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)))
    return "\n".join(lines)


def analyze(query, schema):
    print_header("SQL QUERY ANALYZER")

    print("INPUT")
    print(query)
    print()

    print("LEXICAL ANALYSIS")
    try:
        tokens = Lexer(query).tokenize()
    except LexicalError as error:
        print(f"Lexical Error: {error.message} at line {error.line}, column {error.column}.")
        return
    print(format_tokens(tokens))
    print()

    print("SYNTAX ANALYSIS")
    try:
        statement = Parser(tokens).parse()
    except ParseError as error:
        print(f"Syntax Error: {error.message} at line {error.line}, column {error.column}.")
        return
    print("Valid SELECT statement")
    print()

    print("AST")
    print(format_ast(statement))
    print()

    print("SEMANTIC ANALYSIS")
    try:
        checks = SemanticAnalyzer(schema).analyze(statement)
    except SemanticError as error:
        print(f"Semantic Error: {error.message}.")
        return
    for check in checks:
        label = "Table" if check.category == "table" else "Column"
        print(f"{label}: {check.name} - valid")
    print()

    print("INTERMEDIATE REPRESENTATION")
    print(render_ir(build_ir(statement)))
    print()

    print("OPTIMIZATION")
    optimized_ir, steps = optimize(statement)
    print(format_optimization_steps(steps))
    print()

    print("EXECUTION PLAN")
    print(render_execution_plan(optimized_ir))
    print(f"Flow: {render_execution_summary(optimized_ir)}")
    print()

    print("RESULT")
    connection = create_sample_database(schema)
    try:
        cursor = connection.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        print(format_result_rows(columns, rows))
    except sqlite3.Error as error:
        print(f"Query could not be executed against the sample dataset: {error}")
    finally:
        connection.close()


def main():
    schema = Schema()
    print("SQL Query Analyzer and Optimizer - Phase 2 Prototype")
    print("Enter a SQL query (or 'exit' to quit)")
    print()
    while True:
        query = input(">> ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue
        print()
        analyze(query, schema)
        print()


if __name__ == "__main__":
    main()
