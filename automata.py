from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    KEYWORD = auto()
    THEN = auto()
    SYMBOL = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    position: int

    def __str__(self) -> str:
        return f"{self.position:>3}  {self.type.name:<10}  {self.lexeme!r}"

KEYWORDS = {"if", "else", "while", "do", "begin", "end"}


class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source
        self.pos = 0
        self.symbol_table: dict[str, int] = {}
        self._next_id = 1

    @staticmethod
    def _is_letter(ch: str) -> bool:
        return ch.isalpha()

    @staticmethod
    def _is_letter_or_digit(ch: str) -> bool:
        return ch.isalnum()

    def instalarID(self, lexeme: str) -> int:
        if lexeme not in self.symbol_table:
            self.symbol_table[lexeme] = self._next_id
            self._next_id += 1
        return self.symbol_table[lexeme]

    def obtenerToken(self, lexeme: str) -> TokenType:
        if lexeme in KEYWORDS:
            return TokenType.KEYWORD
        self.instalarID(lexeme)
        return TokenType.IDENTIFIER

    def _skip_whitespace(self) -> None:
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            self.pos += 1

    def _automaton_2_then(self) -> Token | None:
        start = self.pos
        i = start

        for expected in "then":
            if i >= len(self.source) or self.source[i] != expected:
                return None
            i += 1

        if i < len(self.source) and self._is_letter_or_digit(self.source[i]):
            return None

        self.pos = i
        return Token(TokenType.THEN, "then", start)

    def _automaton_1_identifier(self) -> Token | None:
        start = self.pos
        i = start

        if i >= len(self.source) or not self._is_letter(self.source[i]):
            return None
        i += 1

        while i < len(self.source) and self._is_letter_or_digit(self.source[i]):
            i += 1

        lexeme = self.source[start:i]
        token_type = self.obtenerToken(lexeme)
        self.pos = i
        return Token(token_type, lexeme, start)

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self.pos >= len(self.source):
            return Token(TokenType.EOF, "", self.pos)

        if self.source[self.pos] == "t":
            tok = self._automaton_2_then()
            if tok is not None:
                return tok

        tok = self._automaton_1_identifier()
        if tok is not None:
            return tok

        pos = self.pos
        ch = self.source[self.pos]
        self.pos += 1
        return Token(TokenType.SYMBOL, ch, pos)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                return tokens


def print_tokens(tokens: list[Token]) -> None:
    print("\nTokens:")
    print(f"  {'pos':>3}  {'type':<10}  lexeme")
    print("  " + "-" * 32)
    for tok in tokens:
        print(f"  {tok}")


def print_symbol_table(table: dict[str, int]) -> None:
    print("\nSymbol table (identifiers):")
    if not table:
        print("  (empty)")
        return
    for lexeme, slot in table.items():
        print(f"  {slot:>3}  {lexeme}")


def main() -> None:
    if len(sys.argv) > 1:
        source = " ".join(sys.argv[1:])
        scanner = Scanner(source)
        tokens = scanner.tokenize()
        print_tokens(tokens)
        print_symbol_table(scanner.symbol_table)
        return

    print("Enter a word or line to scan (empty line to quit):")
    while True:
        try:
            line = input("> ").rstrip("\n")
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            break
        scanner = Scanner(line)
        tokens = scanner.tokenize()
        print_tokens(tokens)
        print_symbol_table(scanner.symbol_table)
        print()


if __name__ == "__main__":
    main()