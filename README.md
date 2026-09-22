# SQL Query Analyzer and Optimizer Using Compiler Design Techniques

**Student:** Satwik Som
**Register Number:** 24BCE2822
**Course:** Compiler Design Laboratory
**Milestone:** Review 2 — Phase 2 Prototype

## 1. Overview

This project applies compiler design techniques to a restricted subset of SQL,
building a front-to-back analysis pipeline: lexical analysis, syntax analysis,
AST construction, semantic analysis against a schema, translation into a
relational intermediate representation, rule-based optimization, and generation
of a logical execution plan. It is an educational SQL compiler-style analyzer,
not a production database engine.

## 2. Problem Statement

Database engines report SQL mistakes using engine-specific, often opaque error
messages, and their query optimizers are opaque black boxes. This project
explores how classical compiler front-end and middle-end techniques —
tokenization, grammar-based parsing, AST construction, semantic checking against
a symbol table, intermediate representation, and transparent rule-based
rewriting — can be applied to a SQL subset to produce clear diagnostics and an
explainable optimization process.

## 3. Compiler Design Relevance

| Stage | Compiler concept |
|---|---|
| Lexer | Finite-automaton-style scanning, tokenization, lexical error detection |
| Parser | Recursive-descent parsing, grammar validation, syntax error reporting |
| AST | Abstract syntax tree construction and traversal |
| Semantic Analyzer | Symbol-table (schema) lookups, semantic error detection |
| IR | Translation from AST to a relational intermediate representation |
| Optimizer | Rule-based rewriting of the IR, analogous to peephole/logical optimization |
| Execution Plan | Code-generation-style lowering of the optimized IR into an ordered plan |

## 4. Phase 1 Implementation (Review 1)

- Character-by-character lexical analysis with line/column tracking
- Token classification: keywords, identifiers, numbers, strings, operators, punctuation
- Recursive-descent syntax validation for `SELECT ... FROM ... [WHERE ...]`
- Lexical and syntax error reporting with position information

## 5. Phase 2 Implementation (Review 2)

Built on top of the Phase 1 front end:

- **AST construction** — the parser now returns a structured Abstract Syntax
  Tree (`SelectStatement`, `Identifier`, `Literal`, `Comparison`,
  `LogicalCondition`, `TableReference`, `WhereClause`) instead of a boolean,
  along with a tree-style display renderer.
- **Trailing-token detection** — the parser now rejects unexpected tokens after
  the terminating semicolon.
- **Schema / symbol table** — a simple in-memory schema (`employee`,
  `department`) with table and column lookups.
- **Semantic analyzer** — walks the AST and validates table existence and
  column existence (both in the `SELECT` list and the `WHERE` condition)
  against the schema.
- **Intermediate representation (IR)** — a relational-style IR with `Scan`,
  `Filter`, and `Project` nodes, built directly from the validated AST.
- **Rule-based optimizer** — three explainable, individually-applied rules
  (see Section 8).
- **Execution plan** — a readable, always-correctly-ordered `SCAN → FILTER →
  PROJECT` plan derived from the optimized IR.
- **Sample result execution** — the validated query is additionally run
  against a small in-memory SQLite database seeded with sample rows, so the
  CLI can show an actual result set.

## 6. Supported SQL Subset

```
select_stmt   → SELECT column_list FROM table_name [WHERE condition] SEMICOLON
column_list   → identifier | identifier COMMA column_list
condition     → identifier operator literal
              | condition logical_operator condition
logical_operator → AND | OR
operator      → = | > | < | >= | <=
literal       → NUMBER | STRING
```

Single table only. No joins, subqueries, `SELECT *`, `GROUP BY`, `ORDER BY`,
aggregate functions, or `INSERT`/`UPDATE`/`DELETE`. These remain out of scope
for this phase (see Section 16).

## 7. Architecture / Pipeline

```
SQL Query
   → Lexical Analysis      (lexer.py)
   → Syntax Analysis        (parser.py)
   → AST                     (ast_nodes.py)
   → Semantic Analysis        (semantic.py, schema.py)
   → Intermediate Representation (ir.py)
   → Query Optimization           (optimizer.py)
   → Execution Plan                 (execution_plan.py)
   → Result                          (schema.py — sample SQLite execution)
```

## 8. Query Optimizer — Rules

The optimizer is rule-based and deliberately not cost-based. Each rule reports
whether it applied, and why.

**Rule 1 — Predicate Pushdown.**
When a `WHERE` clause is present, the filter is moved ahead of the projection
in the plan so it conceptually runs closer to the scan. This is a simplified,
single-table illustration of the classical pushdown idea; it becomes most
meaningful once joins are introduced in a later phase, since there is currently
only one relation to filter.

**Rule 2 — Projection Reduction.**
Removes duplicate columns from the `SELECT` list (for example,
`SELECT name, name FROM employee` is reduced to `SELECT name`). Does not apply
when the column list has no redundancy.

**Rule 3 — Constant Expression Simplification.**
Normalizes non-canonical numeric literals in the `WHERE` condition (leading
zeros or redundant decimal places, e.g. `050000` → `50000`). Does not apply
when literals are already canonical or when there is no condition.

## 9. Project Structure

```
sql-query-analyzer-optimizer/
│
├── src/
│   ├── main.py             CLI entry point, wires the full pipeline
│   ├── tokens.py            Token and TokenType definitions
│   ├── lexer.py              Lexical analyzer
│   ├── parser.py              Recursive-descent parser, returns an AST
│   ├── ast_nodes.py            AST node classes and tree display
│   ├── schema.py                 Sample schema and in-memory sample database
│   ├── semantic.py                Semantic analyzer
│   ├── ir.py                       Relational intermediate representation
│   ├── optimizer.py                 Rule-based optimizer
│   └── execution_plan.py             Execution plan generation
│
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   ├── test_semantic.py
│   ├── test_ir.py
│   └── test_optimizer.py
│
├── README.md
└── requirements.txt
```

Note: the AST module is named `ast_nodes.py` rather than `ast.py` to avoid
shadowing Python's built-in `ast` standard library module.

## 10. Compiler Concepts Used

Lexical analysis and tokenization, recursive-descent parsing, grammar-driven
syntax validation, abstract syntax trees, symbol tables, semantic analysis,
intermediate representation design, rule-based program transformation, and
logical-plan generation.

## 11. How to Run

No external dependencies are required beyond the Python 3 standard library
(`sqlite3`, used only for the optional sample-result execution, ships with
Python).

```bash
cd src
python3 main.py
```

Enter a query at the prompt, or type `exit` to quit.

## 12. Example Queries

```sql
SELECT name FROM employee;
SELECT name, salary FROM employee;
SELECT name FROM employee WHERE salary > 50000;
SELECT name, salary FROM employee WHERE salary >= 50000 AND department = 'IT';
SELECT age FROM employee;
```

## 13. Example Output

```
SQL QUERY ANALYZER

INPUT
SELECT name FROM employee WHERE salary > 50000;

LEXICAL ANALYSIS
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
Valid SELECT statement

AST
SELECT
├── COLUMNS
│   └── name
├── FROM
│   └── employee
└── WHERE
    └── >
        ├── salary
        └── 50000

SEMANTIC ANALYSIS
Table: employee - valid
Column: name - valid
Column: salary - valid

INTERMEDIATE REPRESENTATION
PROJECT(name)
    ↓
FILTER(salary > 50000)
    ↓
SCAN(employee)

OPTIMIZATION
Rule: Predicate Pushdown
Status: applied
Reason: The filter is moved ahead of the projection so it runs closer to the scan.
Before: PROJECT(name) ↓ FILTER(salary > 50000) ↓ SCAN(employee)
After: FILTER(salary > 50000) ↓ PROJECT(name) ↓ SCAN(employee)

Rule: Constant Expression Simplification
Status: not applied
Reason: Numeric literals in the condition are already in canonical form.

Rule: Projection Reduction
Status: not applied
Reason: The column list has no redundant or duplicate columns.

EXECUTION PLAN
SCAN employee
    ↓
FILTER salary > 50000
    ↓
PROJECT name
Flow: SCAN → FILTER → PROJECT

RESULT
name
Charlie
```

## 14. Testing

```bash
python3 -m unittest discover -s tests
```

The suite (41 tests) covers:

- Lexer token classification, position tracking, and lexical errors
- Parser AST construction for valid queries, and syntax errors for invalid ones
- Semantic analyzer validation of tables and columns, valid and invalid
- IR construction from the AST
- Each optimizer rule, verifying both when it applies and when it correctly
  does not
- Execution plan ordering, including after optimization has restructured the IR

## 15. Current Implementation

- Lexical Analysis
- Syntax Analysis
- AST
- Semantic Analysis
- Schema / Symbol Table
- Intermediate Representation
- Rule-based Optimization
- Execution Plan
- Sample result execution against an in-memory SQLite database

## 16. Future Enhancements

- Support for joins across multiple tables (where predicate pushdown becomes
  meaningful in the way described in Section 8)
- Subquery support
- `GROUP BY`, `ORDER BY`, and aggregate functions
- Cost-based optimization using estimated row counts or table statistics
- A larger, configurable schema and sample dataset
