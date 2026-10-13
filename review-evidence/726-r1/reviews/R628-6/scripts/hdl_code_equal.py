#!/usr/bin/env python3
"""Compare SystemVerilog sources between two commits with comments removed.

Usage: hdl_code_equal.py REPO OLD_COMMIT NEW_COMMIT PATH...
Strips // line comments and /* */ block comments (string literals are kept
intact), collapses whitespace, and reports per file whether the remaining
token stream is identical. Exit 0 only when every file is code-equal.
"""
import re
import subprocess
import sys


def strip(text: str) -> str:
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1]); i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i); i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2); i = n if j < 0 else j + 2
            out.append(" ")
        else:
            out.append(c); i += 1
    return re.sub(r"\s+", " ", "".join(out)).strip()


repo, old, new, *paths = sys.argv[1:]
bad = 0
for p in paths:
    a = subprocess.run(["git", "-C", repo, "show", f"{old}:{p}"], capture_output=True, text=True).stdout
    b = subprocess.run(["git", "-C", repo, "show", f"{new}:{p}"], capture_output=True, text=True).stdout
    same = strip(a) == strip(b)
    bad += not same
    print(f"{'CODE-EQUAL' if same else 'CODE-DIFFERS'}\t{old[:8]}..{new[:8]}\t{p}")
sys.exit(1 if bad else 0)
