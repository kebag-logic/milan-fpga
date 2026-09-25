#!/usr/bin/env python3
"""Compare comment-stripped SystemVerilog at two commits.

Usage: strip_compare.py <repo> <base> <head> <path>
A small scanner removes // and /* */ comments while keeping string
literals intact, then drops trailing whitespace and blank lines. Prints
the sha256 of each stripped form and IDENTICAL or DIFFERENT.
"""
import hashlib
import subprocess
import sys


def strip_comments(text: str) -> str:
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            if j < 0:
                raise SystemExit("unterminated block comment")
            i = j + 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def stripped(repo: str, rev: str, path: str) -> str:
    text = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          capture_output=True, text=True, check=True).stdout
    lines = [ln.rstrip() for ln in strip_comments(text).splitlines()]
    return "\n".join(ln for ln in lines if ln) + "\n"


def main() -> int:
    repo, base, head, path = sys.argv[1:5]
    a, b = stripped(repo, base, path), stripped(repo, head, path)
    for rev, s in ((base, a), (head, b)):
        print(f"{rev} {hashlib.sha256(s.encode()).hexdigest()} lines={s.count(chr(10))}")
    print("IDENTICAL" if a == b else "DIFFERENT")
    return 0 if a == b else 1


if __name__ == "__main__":
    raise SystemExit(main())
