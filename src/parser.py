from tokens import TokenType, COMPARISON_OPERATORS


class ParseError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"Line {line}, Column {column}: {message}")


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        self._parse_select_statement()
        return True

    def _current(self):
        return self.tokens[self.position]

    def _advance(self):
        token = self.tokens[self.position]
        if self.position < len(self.tokens) - 1:
            self.position += 1
        return token

    def _expect_keyword(self, keyword, error_message):
        token = self._current()
        if token.type != TokenType.KEYWORD or token.value != keyword:
            raise ParseError(error_message, token.line, token.column)
        return self._advance()

    def _expect_type(self, token_type, error_message):
        token = self._current()
        if token.type != token_type:
            raise ParseError(error_message, token.line, token.column)
        return self._advance()

    def _parse_select_statement(self):
        self._expect_keyword("SELECT", "Expected SELECT at the start of the statement")
        self._parse_column_list()
        self._expect_keyword("FROM", "Expected FROM after column list")
        self._parse_table_name()
        if self._current().type == TokenType.KEYWORD and self._current().value == "WHERE":
            self._advance()
            self._parse_condition()
        self._expect_type(TokenType.SEMICOLON, "Expected ';' at the end of the statement")

    def _parse_column_list(self):
        token = self._current()
        if token.type != TokenType.IDENTIFIER:
            raise ParseError("Expected a column name after SELECT", token.line, token.column)
        self._advance()
        if self._current().type == TokenType.COMMA:
            self._advance()
            self._parse_column_list()

    def _parse_table_name(self):
        token = self._current()
        if token.type != TokenType.IDENTIFIER:
            raise ParseError("Expected a table name after FROM", token.line, token.column)
        self._advance()

    def _parse_condition(self):
        left = self._current()
        if left.type != TokenType.IDENTIFIER:
            raise ParseError("Expected a column name in the WHERE condition", left.line, left.column)
        self._advance()

        operator_token = self._current()
        if operator_token.type != TokenType.OPERATOR or operator_token.value not in COMPARISON_OPERATORS:
            raise ParseError(
                "Expected a comparison operator (=, >, <, >=, <=)",
                operator_token.line,
                operator_token.column,
            )
        self._advance()

        literal_token = self._current()
        if literal_token.type not in (TokenType.NUMBER, TokenType.STRING):
            raise ParseError(
                "Expected a value (number or string) after the operator",
                literal_token.line,
                literal_token.column,
            )
        self._advance()

        next_token = self._current()
        if next_token.type == TokenType.KEYWORD and next_token.value in ("AND", "OR"):
            self._advance()
            self._parse_condition()
