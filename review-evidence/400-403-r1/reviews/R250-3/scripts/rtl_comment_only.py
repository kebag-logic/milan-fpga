#!/usr/bin/env python3
"""Prove that the RTL files changed between two revisions differ only in
comments and whitespace.

Usage: rtl_comment_only.py <checkout> <old-rev> <new-rev>

Each changed .sv/.svh file is read at both revisions, `//` line comments and
`/* */` block comments are removed (string literals are respected), all
whitespace is collapsed, and the two token streams are compared.
Exit 0 when every file is comment-only, 1 otherwise.
"""
import re
import subprocess
import sys


def strip(src: str) -> str:
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith("//", i):
            i = src.find("\n", i)
            i = n if i < 0 else i
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return re.sub(r"\s+", " ", "".join(out)).strip()


def main() -> int:
    repo, old, new = sys.argv[1:4]
    names = subprocess.check_output(
        ["git", "-C", repo, "diff", "--name-only", old, new, "--", "*.sv", "*.svh"],
        text=True).split()
    bad = 0
    for name in names:
        a = subprocess.check_output(["git", "-C", repo, "show", f"{old}:{name}"], text=True)
        b = subprocess.check_output(["git", "-C", repo, "show", f"{new}:{name}"], text=True)
        same = strip(a) == strip(b)
        bad += not same
        print(f"{'COMMENT-ONLY' if same else 'CODE-CHANGED'} {name}")
    print(f"{len(names)} RTL file(s) changed, {bad} with code changes")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
