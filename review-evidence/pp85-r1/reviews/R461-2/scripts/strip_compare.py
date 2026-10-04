#!/usr/bin/env python3
"""Compare SystemVerilog sources with comments removed, independently of any tool.

usage: strip_compare.py A.sv B.sv
Removes // line comments and /* */ block comments (outside string literals),
then trailing whitespace and blank lines, and reports whether the token text is
identical. Also prints raw line counts and sha256 of each stripped text.
"""
import hashlib
import sys


def strip(text: str) -> str:
    out = []
    i = 0
    n = len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if c == '"':
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
            continue
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        out.append(c)
        i += 1
    lines = [ln.rstrip() for ln in "".join(out).splitlines()]
    return "\n".join(ln for ln in lines if ln) + "\n"


def main() -> int:
    a, b = sys.argv[1], sys.argv[2]
    ta, tb = open(a).read(), open(b).read()
    sa, sb = strip(ta), strip(tb)
    for name, raw, s in ((a, ta, sa), (b, tb, sb)):
        print(f"{name}: raw lines {raw.count(chr(10))}, stripped sha256 "
              f"{hashlib.sha256(s.encode()).hexdigest()}")
    same = sa == sb
    print("comment-stripped IDENTICAL" if same else "comment-stripped DIFFERENT")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
