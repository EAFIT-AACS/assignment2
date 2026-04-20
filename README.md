# Assignment 2 — Finite Automata (Figure 3.14)
Formal Languages · EAFIT 2026

---

## Video

https://youtu.be/IeamEP_RjPA
---

## Environment

| | |
|---|---|
| OS | macOS 15
| Language | Python 3.9
| Dependencies | None |

---

## How to run

    python3 automata.py

---

## What it does

The program reads a line of text and breaks it into tokens using two finite automata from Figure 3.14 of the Dragon Book.

### Automaton 1 — identifiers and keywords

Starts at state 9. If the first character is a letter, it moves to state 10 and keeps reading letters or digits. When it hits anything else, it stops and accepts (state 11).

    state 9  --letter--> state 10
    state 10 --letter or digit--> state 10
    state 10 --other--> state 11 (accept)

obtenerToken() then checks whether the result is a reserved word (if, else, while, do, begin, end). If it is, the token type is KEYWORD. If not, instalarID() stores it in the symbol table and returns IDENTIFIER.

### Automaton 2 — keyword "then"

Reads exactly t -> h -> e -> n, then checks that the next character is not a letter or digit. That last check matters: thenX and then1 are not matched here — they fall through to Automaton 1, which treats them as identifiers.

    0 --t--> 1 --h--> 2 --e--> 3 --n--> 4 --[not letter/digit]--> accept

### How the scanner decides

1. Skip whitespace.
2. If the current character is t, try Automaton 2.
3. If that fails, try Automaton 1.
4. If neither matches, return the character as a SYMBOL token.
5. Repeat until end of input.

---

## Project structure

    automata.py   — the scanner and both automata
    README.md     — this file

---

## References

Aho, Alfred V. et al. Compilers: Principles, Techniques, & Tools. 2nd ed. Pearson/Addison Wesley, 2007. Section 3.4.2, Figure 3.14.