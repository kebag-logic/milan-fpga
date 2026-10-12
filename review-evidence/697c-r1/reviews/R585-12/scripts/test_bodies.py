#!/usr/bin/env python3
"""List GoogleTest TEST/TEST_F names in two files and compare bodies by tokens.
Usage: test_bodies.py DEV STACK"""
import re, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from token_compare import lex
def tests(path):
    toks = [t for t, _ in lex(path)]
    out = {}
    i = 0
    while i < len(toks):
        if toks[i] in ("TEST", "TEST_F") and toks[i+1] == "(":
            name = toks[i+2] + "." + toks[i+4]
            j = toks.index("{", i)
            depth, k = 0, j
            while True:
                depth += toks[k] == "{"
                depth -= toks[k] == "}"
                k += 1
                if depth == 0: break
            out[name] = toks[j:k]
            i = k
        else:
            i += 1
    return out
d, s = tests(sys.argv[1]), tests(sys.argv[2])
missing = [n for n in d if n not in s]
differ = [n for n in d if n in s and d[n] != s[n]]
print(f"dev tests {len(d)}, stack tests {len(s)}, dev-not-in-stack {len(missing)}, same-name-different-body {len(differ)}")
for n in missing: print("  MISSING", n)
for n in differ: print("  BODY-DIFFERS", n)
for n in s:
    if n not in d: print("  STACK-ONLY", n)
