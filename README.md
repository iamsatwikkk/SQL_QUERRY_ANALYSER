# SQL Query Analyzer and Optimizer Using Compiler Design Techniques

**Student:** Satwik Som
**Register Number:** 24BCE2822
**Course:** Compiler Design Laboratory
**Milestone:** Review 1 — Phase 1 Prototype

## Overview

This project applies core compiler design techniques — lexical analysis and syntax
analysis — to a restricted subset of SQL. The long-term goal is to build a small
pipeline that takes a raw SQL `SELECT` query and analyzes it the way a compiler
front-end analyzes source code, eventually extending into semantic analysis and
query optimization in later phases.

## Problem Being Addressed

SQL queries are frequently written with subtle syntax mistakes that database
engines report using opaque, engine-specific error messages. This project explores
how classical compiler front-end techniques (tokenization, grammar-based parsing)
can be used to validate SQL structure and produce clear, position-aware error
messages before a query ever reaches a database engine.

## Phase 1 Scope (Review 1)

This submission implements only the compiler front-end for a limited `SELECT`
grammar:

- Character-by-character lexical analysis
- Token classification (keywords, identifiers, numbers, strings, operators,
  punctuation)
- Recursive-descent syntax validation for `SELECT ... FROM ... [WHERE ...]`
- Lexical and syntax error reporting with line and column information
- A command-line demonstration tool
- A unit test suite covering valid and invalid queries

## Compiler Concepts Demonstrated

- **Lexical analysis**: scanning source text into a token stream, whitespace
  handling, line/column tracking, lexical error detection
- **Token classification**: keyword recognition vs. identifiers, literal typing
  (number vs. string), operator recognition
- **Syntax analysis**: recursive-descent parsing against an explicit grammar,
  structural validation, syntax error recovery with descriptive messages

## Project Structure

```
sql-query-analyzer-optimizer/
│
├── src/
│   ├── main.py
│   ├── lexer.py
│   ├── parser.py
│   └── tokens.py
│
├── tests/
│   └── test_parser.py
│
├── README.md
└── requirements.txt
```

## How to Run

No external dependencies are required — only the Python 3 standard library.

```bash
cd src
python3 main.py
```

Enter a query at the prompt, or type `exit` to quit.

To run the test suite:

```bash
python3 -m unittest discover -s tests
```

## Example Input

```sql
SELECT name FROM employee WHERE salary > 50000;
```

## Example Output

```
========================================
SQL QUERY ANALYZER
========================================

INPUT
SELECT name FROM employee WHERE salary > 50000;

LEXICAL ANALYSIS
----------------------------------------
SELECT       KEYWORD
name         IDENTIFIER
FROM         KEYWORD
employee     IDENTIFIER
WHERE        KEYWORD
salary       IDENTIFIER
>            OPERATOR
50000        NUMBER
;            SEMICOLON

SYNTAX ANALYSIS
----------------------------------------
✓ Valid SELECT statement
```

## Current Implementation

- Lexical analysis
- Token generation
- Basic syntax validation for the supported `SELECT` grammar
- Lexical and syntax error reporting

## Planned for Later Phases

- Abstract Syntax Tree (AST) construction
- Semantic analysis and schema/symbol-table integration
- Intermediate representation
- Query optimization (rule-based and cost-based)
- Execution plan generation
