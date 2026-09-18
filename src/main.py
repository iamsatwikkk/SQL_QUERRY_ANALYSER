from lexer import Lexer, LexicalError
from parser import Parser, ParseError
from tokens import TokenType


def format_tokens(tokens):
    lines = []
    for token in tokens:
        if token.type == TokenType.EOF:
            continue
        lines.append(f"{token.value:<12} {token.type.name}")
    return "\n".join(lines)


def analyze(query):
    print("SQL QUERY ANALYZER")
    print()
    print("INPUT")
    print(query)
    print()

    print("LEXICAL ANALYSIS")
    print("-" * 40)
    try:
        tokens = Lexer(query).tokenize()
    except LexicalError as error:
        print(f"Lexical error: {error.message} (line {error.line}, column {error.column})")
        return
    print(format_tokens(tokens))
    print()

    print("SYNTAX ANALYSIS")
    print("-" * 40)
    try:
        Parser(tokens).parse()
    except ParseError as error:
        print(f"Syntax error: {error.message} (line {error.line}, column {error.column})")
        return
    print("Valid SELECT statement")


def main():
    print("SQL Query Analyzer — Phase 1 Prototype")
    print("Enter a SQL query (or 'exit' to quit)")
    print()
    while True:
        query = input(">> ").strip()
        if query.lower() == "exit":
            break
        if not query:
            continue
        print()
        analyze(query)
        print()


if __name__ == "__main__":
    main()
