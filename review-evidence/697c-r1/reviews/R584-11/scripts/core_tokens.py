#!/usr/bin/env python3
"""Compare two C sources token for token and code line for code line.

Usage: core_tokens.py A B   (prints a verdict line; exit 0 iff identical tokens)
Comments and whitespace are dropped; string and character literals are kept whole.
"Line-identical" means every token sits on the same line number in both files.
"""
import re
import sys

TOKEN = re.compile(r"""
    (?P<ws>[ \t\r\f\v]+|\\\n) |
    (?P<nl>\n) |
    (?P<lc>//[^\n]*) |
    (?P<bc>/\*.*?\*/) |
    (?P<str>(?:u8|u|U|L)?"(?:\\.|[^"\\\n])*") |
    (?P<chr>(?:u8|u|U|L)?'(?:\\.|[^'\\\n])*') |
    (?P<num>\.?[0-9](?:[eEpP][+-]|[0-9A-Za-z_.'])*) |
    (?P<id>[A-Za-z_][A-Za-z_0-9]*) |
    (?P<op>%:%:|\.\.\.|<<=|>>=|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^]=|\#\#|<:|:>|<%|%>|%:|[][(){}.&*+\-~!/%<>^|?:;=,\#])
""", re.S | re.X)


def lex(path):
    text = open(path, encoding="utf-8").read()
    out, line, pos = [], 1, 0
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise SystemExit(f"{path}:{line}: cannot lex {text[pos:pos+20]!r}")
        kind, val = m.lastgroup, m.group()
        if kind not in ("ws", "nl", "lc", "bc"):
            out.append((line, val))
        line += val.count("\n")
        pos = m.end()
    return out


def main():
    a, b = lex(sys.argv[1]), lex(sys.argv[2])
    tok_eq = [t for _, t in a] == [t for _, t in b]
    line_eq = a == b
    print(f"{'IDENTICAL' if tok_eq else 'DIFFERENT'} tokens={len(a)}/{len(b)} "
          f"lines={'same' if line_eq else 'moved'} {sys.argv[1]} {sys.argv[2]}")
    if not tok_eq:
        for i, (x, y) in enumerate(zip(a, b)):
            if x[1] != y[1]:
                print(f"  first difference at token {i}: {x} vs {y}")
                break
    return 0 if tok_eq and line_eq else 1


if __name__ == "__main__":
    sys.exit(main())
