#!/usr/bin/env python3
"""Compare two C sources token for token and line for line.

Independent of any lexer the lane used: a small C lexer that drops comments
and whitespace (line splices honoured), then compares the token sequences
and, separately, each token's line number. Usage:
  token_compare.py LEFT RIGHT   (LEFT/RIGHT are file paths)
Prints one line: tokens, equal-tokens verdict, equal-lines verdict, and the
first difference if any. Exit 0 only when both are equal.
"""
import re
import sys

TOKEN = re.compile(r"""
  (?P<ws>[ \t\f\v\r]+|\n)
 |(?P<lc>//[^\n]*)
 |(?P<bc>/\*.*?\*/)
 |(?P<str>[LuU8]*"(?:\\.|[^"\\\n])*")
 |(?P<chr>[LuU8]*'(?:\\.|[^'\\\n])*')
 |(?P<num>\.?[0-9](?:[eEpP][+-]|[0-9A-Za-z_.])*)
 |(?P<id>[A-Za-z_][A-Za-z_0-9]*)
 |(?P<punct>%:%:|\.\.\.|<<=|>>=|->|\+\+|--|<<|>>|<=|>=|==|!=|&&|\|\||[-+*/%&|^]=|\#\#|<:|:>|<%|%>|%:|[][(){}.&*+\-~!/%<>^|?:;=,\#])
 |(?P<other>.)
""", re.X | re.S)


def lex(path):
    text = open(path, "rb").read().decode("utf-8")
    # Phase 2: delete backslash-newline, but keep a map back to lines.
    out, line, lines = [], 1, []
    i = 0
    while i < len(text):
        if text[i] == "\\" and text[i + 1:i + 2] == "\n":
            i += 2
            line += 1
            continue
        out.append(text[i])
        lines.append(line)
        if text[i] == "\n":
            line += 1
        i += 1
    s = "".join(out)
    toks = []
    for m in TOKEN.finditer(s):
        kind = m.lastgroup
        if kind in ("ws", "lc", "bc"):
            continue
        if kind == "other":
            raise SystemExit(f"{path}: unlexable {m.group()!r} at line {lines[m.start()]}")
        toks.append((m.group(), lines[m.start()]))
    return toks


def main():
    left, right = lex(sys.argv[1]), lex(sys.argv[2])
    ltext = [t for t, _ in left]
    rtext = [t for t, _ in right]
    same_tokens = ltext == rtext
    same_lines = same_tokens and [n for _, n in left] == [n for _, n in right]
    first = ""
    if not same_tokens:
        for k, (a, b) in enumerate(zip(ltext, rtext)):
            if a != b:
                first = f" first-token-diff #{k}: {a!r}@{left[k][1]} vs {b!r}@{right[k][1]}"
                break
        else:
            first = f" length {len(ltext)} vs {len(rtext)}"
    elif not same_lines:
        for k, ((_, a), (_, b)) in enumerate(zip(left, right)):
            if a != b:
                first = f" first-line-diff #{k}: {left[k][0]!r} line {a} vs {b}"
                break
    print(f"tokens {len(ltext)}/{len(rtext)} tokens-equal={same_tokens} "
          f"lines-equal={same_lines}{first}")
    return 0 if same_tokens and same_lines else 1


if __name__ == "__main__":
    sys.exit(main())
